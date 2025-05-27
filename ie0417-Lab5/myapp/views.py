from django.http import HttpResponse
from .models import Item

def home(request):
    items = Item.objects.all()
    names = ', '.join([item.name for item in items])
    return HttpResponse(f"Items: {names if names else 'No items yet'}")
