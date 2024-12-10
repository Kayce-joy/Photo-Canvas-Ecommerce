import json

import requests
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponse
#from django.contrib.sites import requests
#from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from requests.auth import HTTPBasicAuth

from .credentials import MpesaAccessToken, LipanaMpesaPpassword
from .models import (Photo, CartItem)
#Transaction)
from django.core.mail import send_mail
from django.conf import settings
from .forms import PhotoForm  # Make sure you have this form defined in forms.py
from .forms import PhotoshootBookingForm
from .forms import EditProfileForm

def home(request):
    photos = Photo.objects.all()
    return render(request, 'home.html', {'photos': photos})

def photo_details(request, photo_id):
    photo = get_object_or_404(Photo, id=photo_id)
    return render(request, 'photo_details.html', {'photo': photo})

@login_required
def add_to_cart(request, photo_id):
    photo = get_object_or_404(Photo, id=photo_id)
    cart_item, created = CartItem.objects.get_or_create(user=request.user, photo=photo)
    if not created:
        cart_item.quantity += 1
        print(f"Updated quantity for {photo.title}: {cart_item.quantity}")
    else:
        print(f"Added new item to cart: {photo.title}")
    cart_item.save()
    return redirect('cart')

@login_required
def cart(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total = sum(item.total_price() for item in cart_items)
    return render(request, 'cart.html', {'cart_items': cart_items, 'total': total})


@login_required
def remove_from_cart(request, item_id):
    # Get the item to remove from the cart
    cart_item = get_object_or_404(CartItem, id=item_id, user=request.user)

    # Handle the POST request for item removal
    if request.method == "POST":
        # Remove the item from the cart
        cart_item.delete()
        messages.success(request, "Item successfully removed from your cart.")

    # Redirect to the cart page after the action
    return redirect('cart')  # This should redirect back to the cart view

#@login_required
#def checkout(request):
    #if request.method == 'POST':
        #cart_items = CartItem.objects.filter(user=request.user)
        #total = sum(item.total_price() for item in cart_items)
        #transaction = Transaction.objects.create(user=request.user, total_amount=total, status='Completed')
        #cart_items.delete()

        # Send email notification
        #send_mail(
            #'Transaction Completed',
           # f'Thank you for your purchase! Your transaction ID is {transaction.id}.',
            #settings.DEFAULT_FROM_EMAIL,
            #[request.user.email],
        #)

        #return redirect('transactions')
    #return redirect('cart')

#@login_required
#def transactions(request):
    #transactions = Transaction.objects.filter(user=request.user)
    #return render(request, 'transactions.html', {'transactions': transactions})

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        user = User.objects.create_user(username=username, password=password, email=email)
        login(request, user)
        return redirect('login')
    return render(request, 'register.html')

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('about')
    return render(request, 'login.html')

def user_logout(request):
    logout(request)
    return redirect('login')



# views.py



@login_required
def custom_admin_view(request):
    photos = Photo.objects.filter(user=request.user)  # Fetch photos for the authenticated user

    # Handle adding a new photo
    if request.method == 'POST':
        if 'add_photo' in request.POST:
            add_photo_form = PhotoForm(request.POST, request.FILES)
            if add_photo_form.is_valid():
                photo = add_photo_form.save(commit=False)
                photo.user = request.user  # Set the user to the logged-in user
                photo.save()
                return redirect('custom_admin')  # Redirect to the admin page after saving

        # Handle editing existing photos
        for photo in photos:
            if f'edit-{photo.id}' in request.POST:
                form = PhotoForm(request.POST, request.FILES, instance=photo)
                if form.is_valid():
                    form.save()
                    return redirect('custom_admin')  # Redirect to the admin page after saving

    # Create a formset for all photos to use in the template
    formset = [PhotoForm(instance=photo) for photo in photos]
    add_photo_form = PhotoForm()  # Create an empty form for adding new photos

    return render(request, 'custom_admin.html', {
        'photos': photos,
        'formset': formset,
        'add_photo_form': add_photo_form,
    })

@login_required
def delete_photo(request, photo_id):
    photo = get_object_or_404(Photo, id=photo_id, user=request.user)  # Ensure the user is the owner
    photo.delete()
    return redirect('custom_admin')  # Redirect back to the admin page

@login_required
def update_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, user=request.user)
    if request.method == 'POST':
        quantity = request.POST.get('quantity')
        if quantity.isdigit() and int(quantity) > 0:
            cart_item.quantity = int(quantity)
            cart_item.save()
    return redirect('cart')  # Redirect back to the cart page



def token(request):
    consumer_key = 'A3kR4KGcNDjItN0tAMAOq36CU5CnkCJ579KicGchpD5WeEcQ'
    consumer_secret = 'rxseu8Bngkb5kzzx2bYo5aGEoWfRFUzPTDsOB3QKBa5Jh6MIv6HpTFYRmp357RGF'
    api_URL = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'

    r = requests.get(api_URL, auth=HTTPBasicAuth(
        consumer_key, consumer_secret))
    mpesa_access_token = json.loads(r.text)
    validated_mpesa_access_token = mpesa_access_token["access_token"]

    return render(request, 'token.html', {"token":validated_mpesa_access_token})

def pay(request):
   return render(request, 'pay.html')



def stk(request):
    if request.method =="POST":
        phone = request.POST['phone']
        amount = request.POST['amount']
        access_token = MpesaAccessToken.validated_mpesa_access_token
        api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
        headers = {"Authorization": "Bearer %s" % access_token}
        request = {
            "BusinessShortCode": LipanaMpesaPpassword.Business_short_code,
            "Password": LipanaMpesaPpassword.decode_password,
            "Timestamp": LipanaMpesaPpassword.lipa_time,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": amount,
            "PartyA": phone,
            "PartyB": LipanaMpesaPpassword.Business_short_code,
            "PhoneNumber": phone,
            "CallBackURL": "https://sandbox.safaricom.co.ke/mpesa/",
            "AccountReference": "kayce",
            "TransactionDesc": "Web Development Charges"
        }
        response = requests.post(api_url, json=request, headers=headers)
        return HttpResponse("Success")

def book_photoshoot(request):
        if request.method == 'POST':
            form = PhotoshootBookingForm(request.POST)
            if form.is_valid():
                photoshoot = form.save(commit=False)
                photoshoot.user = request.user  # Associate the booking with the logged-in user
                photoshoot.save()
                messages.success(request, 'Your booking has been successfully submitted!')
                form = PhotoshootBookingForm()  # Reset the form after successful submission
        else:
            form = PhotoshootBookingForm()

        return render(request, 'book_photoshoot.html', {'form': form})


def about(request):
    return render(request, 'home2.html')





@login_required
def profile(request):
    if request.method == 'POST':
        if 'edit_profile' in request.POST:
            form = EditProfileForm(request.POST, instance=request.user)
            if form.is_valid():
                form.save()
                return redirect('profile')  # Stay on the same page
        elif 'delete_profile' in request.POST:
            request.user.delete()
            return redirect('about')  # Redirect to home after deletion
    else:
        form = EditProfileForm(instance=request.user)

    return render(request, 'profile.html', {'form': form})
