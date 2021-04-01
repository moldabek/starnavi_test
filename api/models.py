from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


class Post(models.Model):
    name = models.CharField(max_length=255, verbose_name='name')
    description = models.TextField(verbose_name='description')
    published_at = models.DateTimeField(auto_now_add=True, verbose_name="Published date")
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(to=User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Post"
        verbose_name_plural = "Posts"

    def __str__(self):
        return self.name


class PostLike(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='like')
    published_at = models.DateField(format('%Y-%m-%d'), auto_now_add=True, null=True, blank=True)


class PostUnlike(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='unlikes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='unlike')
    published_at = models.DateField(format('%Y-%m-%d'), auto_now_add=True, null=True, blank=True)


@receiver(signal=post_save, sender=User)
def create_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
