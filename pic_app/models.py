from django.core.exceptions import ValidationError
from django.db import models

# Create your models here.


class Picture(models.Model):
    url_picture = models.CharField(verbose_name='Ссылка', max_length=200, null=True, blank=True)
    picture = models.ImageField(verbose_name='Файл', null=True, blank=True)

    def clean(self):
        if not self.url_picture and not self.picture:
            raise ValidationError("Данные не введены")
        elif self.url_picture and self.picture:
            raise ValidationError("Заполните только одно поле")
