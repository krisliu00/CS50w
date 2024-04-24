from django import forms
from django.core.exceptions import ValidationError
from .models import AuctionList,ItemPictures


class SellList(forms.ModelForm):
    class Meta:
        model = AuctionList
        fields = ['image','category','title', 'description', 'price']
    
    image = forms.ImageField(label='Upload Image', required=True) 
    category = forms.ChoiceField(choices=AuctionList.category_choices)
    
    def clean(self):
            cleaned_data = super().clean()
            image = cleaned_data.get('image')
            if not image:
                raise forms.ValidationError('Please upload at least one image.')
            
            if len(self.instance.item_pictures.all()) > 5:
                raise forms.ValidationError('You can upload a maximum of 5 pictures.')
            
            return cleaned_data