from django import forms
from .models import Auction

DURATION_CHOICES = [
    ('minutes', 'Minutes'),
    ('hours', 'Hours'),
    ('days', 'Days'),
]

class AuctionForm(forms.ModelForm):
    tags = forms.CharField(
        required=False,
        label="Tags",
        help_text="Enter comma-separated tags"
    )

    class Meta:
        model = Auction
        exclude = ['slug', 'is_active', 'highestBid', 'seller', 'purchased_by', 'end_time', 'sold_for']

    duration_value = forms.IntegerField(min_value=1, label="Duration")
    duration_unit = forms.ChoiceField(choices=DURATION_CHOICES, label="Unit")


class AuctionEditForm(forms.ModelForm):
    tags = forms.CharField(
        required=False,
        label="Tags",
        help_text="Enter comma-separated tags"
    )

    duration_value = forms.IntegerField(min_value=1, label="Duration")
    duration_unit = forms.ChoiceField(choices=DURATION_CHOICES, label="Unit")

    class Meta:
        model = Auction
        fields = ['pieceName', 'artistName', 'preview', 'condition', 'description', 'priceBIN', 'startingBid']
    
    

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Convert TaggableManager to a comma-separated string for initial value
        if self.instance.pk:
            self.fields['tags'].initial = ', '.join(t.name for t in self.instance.tags.all())

    def save(self, commit=True):
        instance = super().save(commit=False)
        tags = self.cleaned_data.get('tags', '')

        if commit:
            instance.save()

        # Always update tags after saving
        tag_list = [t.strip() for t in tags.split(',') if t.strip()]
        instance.tags.set(tag_list)

        return instance
