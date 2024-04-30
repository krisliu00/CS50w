from decimal import Decimal
from django import forms
from .models import AuctionList, Bidding, Comments

class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True
    
class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = [single_file_clean(data, initial)]
        return result

class SellList(forms.ModelForm):
    class Meta:
        model = AuctionList
        fields = ['images','category','title', 'description', 'price']
    
    images = MultipleFileField(label='Upload Images', required=True)
    category = forms.ChoiceField(choices=AuctionList.category_choices)

    
    def clean_image(self):
        images = self.cleaned_data.get('images')
        if not images:
            raise forms.ValidationError('Please upload at least one image.')
        return images

    def clean(self):
        cleaned_data = super().clean()
        images = cleaned_data.get('images', [])
        if len(images) > 5:
            raise forms.ValidationError('You can upload a maximum of 5 pictures.')
        return cleaned_data
    

class BiddingForm(forms.ModelForm):
    
    class Meta:
        model = Bidding
        fields = ['bid']

    def clean_bid(self):
        bid = self.cleaned_data.get('bid')
        if bid is None:
            
            return None
        
        if bid % Decimal('5') != Decimal('0'):
            raise forms.ValidationError('Bid must be a multiple of 5.')
        if bid > Decimal('500'):
            raise forms.ValidationError('Single bid must not exceed 500.00$')
        
        return bid

class CommentForm(forms.ModelForm):
    
    class Meta:
        model = Comments
        fields = ['comment']

    def clean_comment(self):
        comment = self.cleaned_data.get('comment')

        if comment is None:
            return None
        
        char_count = len(comment)
        if char_count > 200:
            raise forms.ValidationError('Please submit no more than 200 words')

        return comment