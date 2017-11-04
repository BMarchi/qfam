from django import forms
import datetime
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile
from django.forms import extras
from PIL import Image
from question.models import Category


class ProfileForm(UserCreationForm):
    birthdate = forms.DateField(required=True,
                                widget=extras.SelectDateWidget(
                                    years=range(1920,
                                                datetime.date.today().year)))
    hobbies = forms.CharField(required=False)
    avatar = forms.FileField(required=False)
    favorites_categories = forms.MultipleChoiceField(choices=(),
                                                     widget=forms.CheckboxSelectMultiple,
                                                     required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1',
                  'password2', 'first_name', 'last_name')

    def clean_email(self):
        data = self.cleaned_data['email']
        if User.objects.filter(email=data).exists():
            raise forms.ValidationError("This email already used")
        return data

    def clean_hobbies(self):
        return self.cleaned_data['hobbies'].lower()

    def clean_avatar(self):
        DEFAULT_IMAGE_DIR = '/useravatars/default.jpg'
        im_file = self.cleaned_data['avatar']
        try:
            im = Image.open(im_file)
        except IOError:
            raise forms.ValidationError("Upload a valid image please")
        except AttributeError:
            im_file = DEFAULT_IMAGE_DIR
        return im_file

    def clean_favorites_categories(self):
        name_categories = self.cleaned_data['favorites_categories']
        return ','.join(name_categories)

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.fields['favorites_categories'].choices = [(choice.category_name,
                                                        choice) for choice in
                                                       Category.objects.all()]
        for fieldname in ['username']:
            self.fields[fieldname].help_text = None


class EditForm(forms.Form):
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField()
    hobbies = forms.CharField()
    favorites_categories = forms.MultipleChoiceField(choices=(),
                                                     widget=forms.CheckboxSelectMultiple,
                                                     required=False)
    birthdate = forms.DateField(widget=extras.SelectDateWidget(years=range(1920,
                                                                           datetime.date.today().year)))
    avatar = forms.FileField(required=False)

    def clean_avatar(self):
        im_file = self.cleaned_data['avatar']
        try:
            im = Image.open(im_file)
        except IOError:
            raise forms.ValidationError("Upload a valid image please")
        except AttributeError:
            return None
        return im_file

    def clean_hobbies(self):
        return self.cleaned_data['hobbies'].lower()

    def clean_favorites_categories(self):
        name_categories = self.cleaned_data['favorites_categories']
        return ','.join(name_categories)

    def __init__(self, *args, **kwargs):
        super(EditForm, self).__init__(*args, **kwargs)
        self.fields['favorites_categories'].choices = [(choice.category_name,
                                                        choice) for choice
                                                       in Category.objects.all()]
