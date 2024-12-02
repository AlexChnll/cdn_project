from django.shortcuts import render
from django.http import FileResponse, HttpResponseNotFound, HttpResponseServerError
import os
import requests
from django.conf import settings
from .cache import LRUCache

# Initialisation du cache
cache = LRUCache(capacity=2)

# Adresse privée utilisée pour interagir avec le serveur central
CENTRAL_SERVER_PRIVATE_IP = "10.0.0.11"
CENTRAL_SERVER_PORT = 8080

def index(request):
    return render(request, 'CDN_app/index.html')

def get_image(request, image_name):
   
    print(f"Received request for image: {image_name}")

    # Vérifier si l'image est dans le cache
    cached_path = cache.get(image_name)
    if cached_path and os.path.exists(cached_path):
        print(f"Cache hit for {image_name} and exist")
        try:
            return FileResponse(open(cached_path,'rb'), content_type='image/jpeg')
        except Exception as e:
            print(f"Error serving cached file: {e}")
            return HttpResponseNotFound('Error serving cached image')
    elif cached_path:
        print(f"Cached path for {image_name} is invalid. Removing from cache.")
        cache.delete(image_name) # Remove invalid path from cache
    
    else:
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
                
                # Mettre l'image en cache
                cache.put(image_name, local_path)
                print(f"Image {image_name} stored in cache at {local_path}")
                return FileResponse(open(local_path, 'rb'), content_type='image/jpeg')
            elif response.status_code == 404:
                print(f"Image {image_name} not found on the central server.")
                return HttpResponseNotFound('Image not found on central server')
        except requests.RequestException as e:
            print(f"Error fetching from central server: {e}")
            return HttpResponseServerError('Error communicating with central server')

    # Si rien ne fonctionne, retournez une image par défaut
    default_path = os.path.join(settings.BASE_DIR, 'static', 'images/default.jpg')
    if os.path.exists(default_path):
        try:
            cache.put(image_name, default_path)
            return FileResponse(open(default_path, 'rb'), content_type='image/jpeg')
        except Exception as e:
            print(f"Error opening default image: {e}")
            return HttpResponseNotFound('Error opening default image')
    return HttpResponseNotFound('Default image not found')
