from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),

    path("create-lot", views.new_lot, name="new_lot"),
    path("lot/<int:lot_id>", views.lot_view, name="lot_view"),
    path("toggle_watchlist/<int:lot_id>/", views.toggle_watchlist, name="toggle_watchlist"),
    path("watchlist", views.watchlist, name="watchlist"),

    path("categories", views.categories, name="categories"),
    path("categories/<int:category_id>", views.category_view, name="category_view"),

]
