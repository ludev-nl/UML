from django import forms
from model.models import Requirement
from django.forms import widgets


class UploadForm(forms.Form):
    file = forms.FileField(label='file', required=False, allow_empty_file=True,
                           widget=forms.FileInput(attrs={'class': 'special', }))


class SelectTitleForm(forms.Form):
    title = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control', }))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].choices = Requirement.objects.all().values_list('id', 'title')





