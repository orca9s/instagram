from django.shortcuts import render
from .models import post


posts = Post.objects.all()
context = {
    'posts': posts,
}
