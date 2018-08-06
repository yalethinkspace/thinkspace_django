from django import forms
from django.contrib.auth.forms import UserCreationForm
from tinymce import TinyMCE
from client.models import User

class TinyMCEWidget(TinyMCE):
    def use_required_attribute(self, *args):
        return False

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Enter a valid email address.')

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']

class DashboardBasicInfoForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']

class DashboardAboutForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['about']

class DashboardPhotoForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['photo']

class DashboardResumeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['resume']
