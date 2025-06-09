from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.user.username)
            slug = base
            count = 1
            while UserProfile.objects.filter(slug=slug).exists():
                slug = f"{base}-{count}"
                count += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.user.username
