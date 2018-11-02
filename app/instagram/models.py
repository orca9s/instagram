from django.db import models


class Post(models.Model):
    author = models.ForeignKey(
        'User',
        on_delete=models.CASCADE,
    )
    photo = models.ImageField(upload_to='post')


class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
    )
    author = models.ForeignKey(
        'User',
        on_delete=models.CASCADE,
    )
    content = models.TextField()