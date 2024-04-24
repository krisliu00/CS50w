from django import forms
from .models import CustomUser,UserProfile



class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput())
    password_confirm = forms.CharField(label='Confirm Password', widget=forms.PasswordInput())

    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'age', 'bio', 'profile_picture', 'email']

    def clean_password_confirm(self):
        password = self.cleaned_data.get('password')
        password_confirm = self.cleaned_data.get('password_confirm')
        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Passwords don't match")
        return password_confirm

    def save(self, commit=True):
        
        user = super(UserRegistrationForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()

            # Create a UserProfile instance for the newly registered user
            UserProfile.objects.create(user=user)

        return user

class UserLoginForm(forms.Form):
    username = forms.CharField(label="username", max_length=64)
    password = forms.CharField(label="password", widget=forms.PasswordInput())

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        return cleaned_data
