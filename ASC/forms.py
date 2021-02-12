from django import forms
from ASC.models import Image


class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ('file', 'xfile')

        def save(self):
            image = super(ImageForm, self).save()
            return image
