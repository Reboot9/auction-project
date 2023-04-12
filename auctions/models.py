from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Category(models.Model):
    name = models.CharField(max_length=64, blank=True)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name_plural = "Categories"


class Lot(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="author_user")
    name = models.CharField(max_length=128)
    description = models.CharField(max_length=512, blank=True)
    lot_bid = models.DecimalField(max_digits=7, decimal_places=2, default=0.0)
    category = models.ManyToManyField(Category, blank=False)
    image = models.ImageField(upload_to='uploads/')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Lot №{self.id} {self.name}"

    @property
    def list_of_categories(self):
        return [cat.name for cat in self.category.all()]


class WatchList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ManyToManyField(Lot)

    def __str__(self):
        return f"{self.user}'s Watchlist"


class Bid(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    lot = models.ForeignKey(Lot, on_delete=models.CASCADE)
    user_bid = models.DecimalField(max_digits=7, decimal_places=2)

    def __str__(self):
        return f"{self.lot}: {self.author} {self.user_bid}"


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.CharField(max_length=512, blank=False)
    lot = models.ForeignKey(Lot, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.id}: {self.author} {self.comment} "
