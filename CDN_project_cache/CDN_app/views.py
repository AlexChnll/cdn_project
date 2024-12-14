from django.shortcuts import render
from django.http import FileResponse, HttpResponseNotFound, HttpResponseServerError
import os
import requests
import socket
from requests.adapters import HTTPAdapter
from urllib3.poolmanager import PoolManager
from django.conf import settings
from collections import OrderedDict
import json

class LRUCache:
    def __init__(self, capacity, cache_file='cache.json'):
        self.cache = OrderedDict()
        self.capacity = capacity
        self.cache_file = cache_file
        self._load_cache() 
    
    def _load_cache(self):
        # Charger le cache existant depuis le fichier, s'il existe
        if os.path.exists(self.cache_file):
            with open(self.cache_file, 'r') as f:
                self.cache = OrderedDict(json.load(f))

    def get(self, key):
        # Récupérer l'image si elle existe
        if key in self.cache:
            self.cache.move_to_end(key, last=False)
            return self.cache[key]
        return None

    def put(self, key, value):
        # Ajoute une nouvelle image au cache
        # Si le cache est plein, l'image utilisée la moins récemment est supprimée
        if key in self.cache:
            self.cache.move_to_end(key, last=False)
        elif len(self.cache) >= self.capacity:
            removed_key, removed_value = self.cache.popitem(last=True)
            if os.path.isfile(removed_value):
                os.remove(removed_value)
        self.cache[key] = value
        self._save_cache()

    def delete(self, key):
        if key in self.cache:
            file_path = self.cache.pop(key)
            if os.path.isfile(file_path):
                os.remove(file_path)
            self._save_cache()

    def _save_cache(self):
        with open(self.cache_file, 'w') as f:
            json.dump(self.cache, f)

# Initialisation du cache
cache = LRUCache(capacity=2)

# Adresse privée utilisée pour interagir avec le serveur central
CENTRAL_SERVER_PRIVATE_IP = "10.0.0.11"
CENTRAL_SERVER_PORT = 8080

# Interface réseau à utiliser pour les requêtes sortantes vers le serveur central
OUTBOUND_INTERFACE_IP = "10.0.0.10"     # A modifier pour chaque serveur cache

# HTTPAdapter pour forcer une adresse source
class SourceAddressAdapter(HTTPAdapter):
    def __init__(self, source_address, **kwargs):
        self.source_address = source_address
        super().__init__(**kwargs)

    def init_poolmanager(self, *args, **kwargs):
        kwargs['source_address'] = (self.source_address, 0)
        self.poolmanager = PoolManager(*args, **kwargs)

# Initialisation de la session
session = requests.Session()
session.mount('http://', SourceAddressAdapter(OUTBOUND_INTERFACE_IP))

def index(request):
    return render(request, 'CDN_app/index.html')

def get_image(request, image_name):

    # Vérifier si l'image est dans le cache
    cached_path = cache.get(image_name)
    if cached_path and os.path.exists(cached_path):
        print(f"Cache hit for {image_name} and exist")
        try:
            return FileResponse(open(cached_path,'rb'), content_type='image/jpeg')
        except Exception as e:
            cache.delete(image_name)
            return HttpResponseNotFound('Error serving cached image')
    
    print(f"Cache miss for {image_name}, fetching from central server...")
        
    # Si le fichier n'est pas en cache, contacter le serveur central
    central_server_url = f"http://{CENTRAL_SERVER_PRIVATE_IP}:{CENTRAL_SERVER_PORT}/get_image/{image_name}"
        
    try:
        response = requests.get(central_server_url, stream=True)
        if response.status_code == 200:
            local_path = os.path.join(settings.BASE_DIR, 'static', 'images', f"{image_name}.jpg")
            with open(local_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)                     
            cache.put(image_name, local_path)
            return FileResponse(open(local_path, 'rb'), content_type='image/jpeg')
        elif response.status_code == 404:
            return HttpResponseNotFound('Image not found on central server')
    except requests.RequestException as e:
        return HttpResponseServerError('Error communicating with central server')