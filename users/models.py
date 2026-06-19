from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    phone = models.CharField(max_length=50, blank=True)
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)
    
    def __str__(self):
        return self.email if self.email else self.username
    
    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

