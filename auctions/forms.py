from decimal import Decimal
from django import forms

from .models import Lot, Bid, Comment


class CreateLotForm(forms.ModelForm):
    class Meta:
        model = Lot
        fields = ['name', 'description',
                  'lot_bid', 'category', 'image']
    # lot_name = forms.CharField(label="Lot Name", max_length=128)
    # description = forms.CharField(label="Description", max_length=512)
    # lot_bid = forms.DecimalField(label="Start Bid", max_digits=7, decimal_places=2)
    # category = forms.ModelMultipleChoiceField(label='Categories for Lot',
    #                                           queryset=Category.objects.all(),
    #                                           widget=forms.SelectMultiple)
    # image = forms.ImageField()


class MakeBidForm(forms.ModelForm):
    user_bid = forms.DecimalField(
        min_value=Decimal('0.01'),
        max_value=Decimal('100000'),
        decimal_places=2,
        required=True,
        label='',
        widget=forms.NumberInput(attrs={'placeholder': 'Your Bid'})
    )

    class Meta:
        model = Bid
        fields = ['user_bid']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']
        widgets = {
            'comment': forms.Textarea(attrs={"placeholder": 'Your comment', 'cols': 80, 'rows': 5}),
        }
        labels = {
            'comment': '',
        }
