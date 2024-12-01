from django.shortcuts import render
from django.http import FileResponse, HttpResponseNotFound
import os
from django.conf import settings


def serve_image(request, image_name):
    image_paths = {
        'dog': 'images/dog.jpg',
        'cat': 'images/cat.jpg',
        'mouse': 'images/mouse.jpg'
    }

    image_path = image_paths.get(image_name)
    if not image_path:
        return HttpResponseNotFound('Image not found')
    
    full_path = os.path.join(settings.BASE_DIR, 'static', image_path)
    if not os.path.exists(full_path):
        return HttpResponseNotFound('Default image not found')
    
    try:
        return FileResponse(open(full_path, 'rb'), content_type='image/jpeg')
    except Exception as e:
        print(f"Error opening file: {e}")
        return HttpResponseNotFound('Error opening image')