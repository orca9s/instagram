from django.urls import path

from . import views

# 이 urls모듈의 app_name

app_name = 'posts'

urlpatterns = [
    # posts.urls내의 패턴들은, prefix가 '/posts/'임
    path('', views.post_list, name='post-list')
]