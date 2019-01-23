from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Post
from .forms import PostCreateForm


def post_list(request):
    posts = Post.objects.all()
    context = {
        'posts': posts,
    }

    return render(request, 'posts/post_list.html', context)


# login_required를 써주면 로그인 되어 있을 경우만 작동
@login_required
def post_create(request):
    # 로그인이 안되어있을경우 로그인 페이지로 보내줌
    # if not request.user.is_autheticated:
    #     return redirect('members:login')

    # 1. posts/post_create.html 구현
    #  form구현
    #   input[type=file]
    #   button[type=submit]

    # 2. /posts/create/ URL에 이 view를 연결
    #    URL명은 'post-create'를 사용
    # 3. render를 적절히 사용해서 해당 템플릿을 return
    # 4. base.html의 nav부분에 '+ Add Post'텍스트를 갖는 a링크 하나 추가,
    #     {% url %} 태그를 사용해서 포스트 생성 으로 링크 걸어주기
    context = {}
    if request.method == 'POST':
        form = PostCreateForm(request.POST, request.FILES)
        if form.is_valid():
            form.save(author=request.user)
        return redirect('posts:post-list')
    else:
        form = PostCreateForm()
    context['form'] = form
    return render(request, 'posts/post_create.html', context)


def comment_create(request, post_pk):
    pass
