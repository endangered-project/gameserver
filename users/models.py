from PIL import Image
from decouple import config
from django.contrib.auth.models import User
from django.db import models

CURRENT_URL = config('CURRENT_URL')


class Profile(models.Model):
    """Profile model."""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/', default='avatars/default.jpeg')

    class Meta:
        """Meta class."""
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'

    def __str__(self):
        """Return name."""
        return self.user.username + ' profile'

    def save(self, *args, **kwargs):
        """Resize image on save"""
        super().save(*args, **kwargs)
        image = Image.open(self.avatar.path)
        if image.height > 500 or image.width > 500:
            output_size = (500, 500)
            image.thumbnail(output_size)
            image.save(self.avatar.path)

    def get_full_avatar_url(self):
        return CURRENT_URL + self.avatar.url
