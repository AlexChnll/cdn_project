import os
from collections import OrderedDict

class LRUCache:
    def __init__(self, capacity):
        # Initialisation du cache avec une capacité maximale
        self.cache = OrderedDict()
        self.capacity = capacity

    def get(self, key):
        # Récupérer l'image si elle existe
        if key in self.cache:
            # Déplace la clé au début de la liste pour montrer qu'elle a été récemment utilisée
            self.cache.move_to_end(key, last=False)
            return self.cache[key]
        return None

    def put(self, key, value):
        # Ajoute une nouvelle image au cache
        # Si le cache est plein, l'image utilisée la moins récemment est supprimée

        if key in self.cache:
            self.cache.move_to_end(key, last=False)
        else: 
            if len(self.cache) >= self.capacity:
                removed_key, removed_value = self.cache.popitem(last=True)
            # Ajoute la nouvelle clé
            self.cache[key] = value
            self.cache.move_to_end(key, last=False)

    def delete(self, key):
        if key in self.cache:
            del self.cache[key]


#if __name__ == "__main__":
    # Test de la capacité du cache
#    print("Test de la classe LRUCache")
#    cache = LRUCache(capacity=2)
#    cache.put('dog', 'dog_image_content')
#    cache.put('cat', 'cat_image_content')
#    cache.put('mouse', 'mouse_image_content')  # Cela devrait supprimer 'dog'

    # Affiche le contenu du cache
#    print("Contenu du cache après ajout de 3 éléments (dog, cat, mouse):")
#    print(cache.cache)  # Devrait afficher uniquement 'cat' et 'mouse'

    # Vérifiez si l'accès à 'dog' renvoie None (car il a été supprimé)
#    print("Accès à 'dog' (devrait être None) :", cache.get('dog')) # devrait être none

    # Vérifiez l'accès aux éléments encore dans le cache
#    print("Accès à 'cat' :", cache.get('cat'))  # Devrait renvoyer 'cat_image_content'
#    print("Accès à 'mouse' :", cache.get('mouse'))  # Devrait renvoyer 'mouse_image_content'
    
    # Ajout d'un nouvel élément pour voir la suppression automatique
#    cache.put('bird', 'bird_image_content')
#    print("Contenu du cache après ajout de 'bird' (devrait supprimer 'cat'):")
#    print(cache.cache)

#    print("Accès à 'cat' après ajout de 'bird' (devrait être None) :", cache.get('cat'))
