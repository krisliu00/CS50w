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
        fields = ['images', 'image_url', 'category','title', 'short_description', 'details', 'price']
        help_texts = {
            'group': 'helptext',
        }
    
    images = MultipleFileField(label='Upload Images', required=True, help_text='Please upload at least 1 image')
    image_url = forms.URLField(label='Image URL', required=False, help_text="Enter the URL of your image")
    category = forms.ChoiceField(choices=AuctionList.category_choices)
    short_description = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'No more than 30 characters'}))

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
        
        if bid > Decimal('9999'):
            raise forms.ValidationError('Invalid bid value')
        
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