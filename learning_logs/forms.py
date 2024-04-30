from django import forms
from django.contrib.auth.models import User
from .models import Topic, Entry


class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['text', 'body', 'tags']
        labels = {'text': '',
                  'body': '',
                  'tags': ''}


class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ['text']
        labels = {'text': ''}
        widgets = {'text': forms.Textarea(attrs={'cols': 80})}


class EmailPostForm(forms.Form):
    # name = forms.CharField(max_length=25)
    # email = forms.EmailField(max_length=25)
    to = forms.EmailField()
    # comments = forms.CharField(required=False, widget=forms.Textarea)


class SearchForm(forms.Form):
    search = forms.CharField()


class ContactForm(forms.Form):
    subject = forms.CharField(label='Subject', max_length=100, required=True)
    email = forms.EmailField(label='Sender email', required=True)
    message = forms.CharField(label='Message', widget=forms.Textarea, required=True)
