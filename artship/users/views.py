from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required

from .models import UserProfile
from auction.models import Auction
from .forms import UsernameUpdateForm

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.get_or_create(user=user)
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def my_gallary(request):
    purchases = Auction.objects.filter(purchased_by=request.User)
    return render(request, 'auction/gallery.html', {'purchases': purchases})

def gallery_by_user(request, slug):
    profile = get_object_or_404(UserProfile, slug=slug)
    purchases = Auction.objects.filter(purchased_by=profile.user)
    return render(request, 'auction/gallery.html', {
        'purchases': purchases,
        'owner': profile.user
    })

def profile_by_user(request, slug):
    profile = get_object_or_404(UserProfile, slug=slug)

    # Restrict to owner only
    if request.user != profile.user:
        return redirect('auction_index')

    form = UsernameUpdateForm(instance=profile.user)
    if request.method == 'POST':
        form = UsernameUpdateForm(request.POST, instance=profile.user)
        if form.is_valid():
            form.save()
            return redirect('user_profile', slug=profile.slug)

    user_listings = Auction.objects.filter(seller=profile.user)
    user_bids = Auction.objects.filter(bids__user=profile.user).distinct()

    return render(request, 'users/profile.html', {
        'form': form,
        'profile': profile,
        'user_listings': user_listings,
        'user_bids': user_bids
    })