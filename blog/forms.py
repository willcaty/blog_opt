# -*- coding; utf-8 -*-

from django import forms


class UserForm(forms.Form):
    username = forms.CharField(max_length=30)
    password = forms.CharField(max_length=50)

class ArticleForm(forms.Form):
    title = forms.CharField(max_length=50,required=True)
    abstract = forms.CharField(max_length=50,required=True)
    category = forms.ChoiceField(required=True)