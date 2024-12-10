from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import (Photo, CartItem)
#Transaction)
from .models import Photoshoot

admin.site.register(Photo)
admin.site.register(CartItem)
#admin.site.register(Transaction)
admin.site.register(Photoshoot)

