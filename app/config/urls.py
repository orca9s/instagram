"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

from . import views
from posts.views import tag_post_list

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(pattern_name='posts:post-list'), name='index'),
    # path('', views.index, name='index'),
#   /posts/로 들어오는 URL은 posts.urls모듈에서 처리
    path('posts/', include('posts.urls')),
    path('explore/tags/<str:tag_name>/', tag_post_list, name='tag-post-list'),
    path('members/', include('members.urls')),
]
# 하나의 포스트를 만들어서 return을 해주는 역할을 한다.
# MEDIA_URL로 시작하는 URL은 static()내의 serve()함수를 통해 처리
# MEDIA_ROOT기준으로 파일을 검색함
# MEDIA가 있어야 MEDIA를 찾아준다 배포된 S3는 자동으로 주소를 정해주지만
# 로컬에서 작업시에는 자동으로 해주지 않기 때문에 urlpatterns가 필요하다
urlpatterns += static(
    prefix=settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT,
)
