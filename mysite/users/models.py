from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):

    email = models.EmailField(unique=True)
    bio = models.CharField(max_length=255)
    avatar = models.ImageField(default='mysite/files/avatars/default/user.png', upload_to='mysite/files/avatars')
    following = models.ManyToManyField('self', symmetrical=False, related_name='followers')

    def __str__(self):
        return self.username
