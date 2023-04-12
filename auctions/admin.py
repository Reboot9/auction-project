from django.contrib import admin
from .models import User, Lot, Category, WatchList, Comment

# Register your models here.
admin.site.register(User)
admin.site.register(Lot)
admin.site.register(Category)
admin.site.register(WatchList)
admin.site.register(Comment)
