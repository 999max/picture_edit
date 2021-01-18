from django import forms

from .models import Picture


class PictureForm(forms.ModelForm):
    class Meta:
        model = Picture
        fields = '__all__'


class SizeForm(forms.Form):
    width = forms.IntegerField(label="Ширина", required=False)
    height = forms.IntegerField(label="Высота", required=False)
