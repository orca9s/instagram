from django import forms


class PostCreateFoem(forms.Form):
    photo = forms.ImageField()
