from django.contrib.auth.models import User
from django import forms
from django.core.exceptions import ValidationError
from .models import Book, Chapter, Verse, Annotation
from django.utils.translation import gettext as _


class BookForm(forms.ModelForm):

    class Meta:
        model = Book
        fields = '__all__'


class ChapterForm(forms.ModelForm):

    class Meta:
        model = Chapter
        # fields =  ['number', 'title']
        fields = '__all__'


class VerseForm(forms.ModelForm):

    class Meta:
        model = Verse
        # fields = ['number', 'original_text', 'greek_translation']
        fields = '__all__'


class AnnotationForm(forms.ModelForm):

    class Meta:
        model = Annotation
        # fields =  ['number', 'phrase', 'annotation']
        fields = '__all__'


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']


class UserLoginForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username',  'password']


class ContactForm(forms.Form):
    # gmail overrides from_email option with EMAIL_HOST_USER
    from_email = forms.EmailField(required=False)
    subject = forms.CharField(required=True)
    name = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    team = forms.CharField(required=True)

    message = forms.CharField(widget=forms.Textarea, required=True)
