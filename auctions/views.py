from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist

from .models import User, Lot, Category, WatchList, Comment
from .forms import CreateLotForm, MakeBidForm, CommentForm


def index(request, category_id=None):
    active_lots = Lot.objects.filter(is_active=True).order_by('id')
    return render(request, "auctions/index.html", context={
        'lots': active_lots
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


@login_required(redirect_field_name=None, login_url='login')
def new_lot(request):
    if request.method == "POST":
        form = CreateLotForm(request.POST, request.FILES)
        if form.is_valid():

            author = request.user
            lot_name = form.cleaned_data['name'].capitalize()
            lot_description = form.cleaned_data['description']
            start_bid = form.cleaned_data['lot_bid']
            categories = form.cleaned_data['category']
            image_file = form.cleaned_data['image']
            lot = Lot(creator=author,
                      name=lot_name,
                      description=lot_description,
                      lot_bid=start_bid,
                      # category=categories,
                      image=image_file)
            lot.save()
            lot.category.set(categories)
            return HttpResponseRedirect(reverse("index"))
        else:
            print(form)
            return render(request, 'auctions/create_lot.html', {'form': form})
    return render(request, 'auctions/create_lot.html', context={
        'form': CreateLotForm()
    })


def lot_view(request, lot_id):
    try:
        requested_lot = Lot.objects.get(pk=lot_id)
    except ObjectDoesNotExist:
        messages.error(request, "Requested Lot doesn't exist.")
        return HttpResponseRedirect(reverse('index'))

    added_to_watchlist = False
    if request.user.is_authenticated:
        added_to_watchlist = WatchList.objects.filter(user=request.user, item=lot_id).exists()

    if request.method == "POST":
        if not request.user.is_authenticated:
            messages.error(request, 'You have to be logged in to interact with this page.')
            return HttpResponseRedirect(reverse("login"))
        if request.POST.get('make_bid', False):
            form = MakeBidForm(request.POST)
            if request.user != requested_lot.creator:
                if form.is_valid():
                    if form.cleaned_data['user_bid'] > requested_lot.lot_bid:
                        requested_lot.lot_bid = form.cleaned_data['user_bid']
                        requested_lot.save()
                        messages.success(request, 'Your bid has been saved.')
                    else:
                        messages.error(request, 'Your bid must be higher than the current bid.')
            else:
                messages.error(request, "You can't make bid to your own lot.")
        if request.POST.get('close_lot', False):
            if request.POST['close_lot'] == "Close Lot":
                requested_lot.is_active = False
                requested_lot.save()
                messages.success(request, f'You have closed your lot for {requested_lot.lot_bid}$')
                return HttpResponseRedirect(reverse('index'))
        if request.POST.get('leave_comment', False):
            form = CommentForm(request.POST)
            if form.is_valid():
                print(form.cleaned_data['comment'])
                new_comment = form.save(commit=False)
                new_comment.lot = requested_lot
                new_comment.author = request.user
                new_comment.save()
                return redirect(request.META.get('HTTP_REFERER'))
    return render(request, 'auctions/lot_view.html', context={
        'lot': requested_lot,
        'bid_form': MakeBidForm(),
        'comment_form': CommentForm(),
        'comments': Comment.objects.filter(lot=lot_id),
        'added_to_watchlist': added_to_watchlist,
    })


@login_required(redirect_field_name=None, login_url='login')
def toggle_watchlist(request, lot_id: int):
    lot_to_add = Lot.objects.get(pk=lot_id)
    watched = WatchList.objects.filter(user=request.user, item=lot_to_add)
    # Get the user watchlist or create it if it doesn't exist
    user_list, created = WatchList.objects.get_or_create(user=request.user)

    if watched.exists():
        watched.delete()
        messages.success(request, 'Listing removed from watchlist')
    else:
        # Add the item through the ManyToManyField (Watchlist => item)
        user_list.item.add(lot_to_add)
        messages.success(request, 'Listing added to watchlist')
    return redirect(request.META.get('HTTP_REFERER'))


@login_required(redirect_field_name=None, login_url='login')
def watchlist(request):
    try:
        tracked = WatchList.objects.get(user=request.user)
        lots = tracked.item.all()
    except ObjectDoesNotExist:
        lots = []
    return render(request, 'auctions/watchlist.html', context={
        'tracked': lots
    })


def categories(request):
    all_categories = Category.objects.all().order_by('name')
    return render(request, 'auctions/categories.html', context={
        'categories': all_categories,
    })


def category_view(request, category_id):
    lots_by_category = Lot.objects.filter(is_active=True, category=category_id).order_by('name')
    return render(request, "auctions/index.html", context={
        'lots': lots_by_category
    })

