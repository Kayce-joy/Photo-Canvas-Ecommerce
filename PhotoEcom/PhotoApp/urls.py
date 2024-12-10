
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from . import views
from .views import custom_admin_view, delete_photo, update_cart  # Ensure these views are imported
from .views import book_photoshoot

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', views.home, name='home'),
    path('photo/<int:photo_id>/', views.photo_details, name='photo_details'),
    path('add-to-cart/<int:photo_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart, name='cart'),
    path('remove-from-cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    #path('checkout/', views.checkout, name='checkout'),
    #path('transactions/', views.transactions, name='transactions'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.register, name='register'),
    path('custom_admin/', custom_admin_view, name='custom_admin'),
    path('photo/delete/<int:photo_id>/', delete_photo, name='delete_photo'),
    path('update_cart/<int:item_id>/', update_cart, name='update_cart'),

    path('pay/', views.pay, name='pay'),
    path('stk/', views.stk, name='stk'),
    path('token/', views.token, name='token'),

    path('book-photoshoot/', book_photoshoot, name='book_photoshoot'),

    path('about/', views.about, name='about'),
    path('profile/', views.profile, name='profile'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
