from django.db import models
# Create your models here.


class Image(models.Model):
    file = models.FileField(upload_to='images', blank=False)
    xfile = models.FileField(upload_to='files', blank=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file
