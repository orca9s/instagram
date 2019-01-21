from django.shortcuts import render, redirect
from .models import Post
from .forms import PostCreateForm


def post_list(request):
    posts = Post.objects.all()
    context = {
        'posts': posts,
    }

    return render(request, 'posts/post_list.html', context)


def post_create(request):
    if not request.user.is_authenticated:
        return redirect('posts:post-list')
    # 1. posts/post_create.html 구현
    #  form구현
    #   input[type=file]
    #   button[type=submit]

    # 2. /posts/create/ URL에 이 view를 연결
    #    URL명은 'post-create'를 사용
    # 3. render를 적절히 사용해서 해당 템플릿을 return
    # 4. base.html의 nav부분에 '+ Add Post'텍스트를 갖는 a링크 하나 추가,
    #     {% url %} 태그를 사용해서 포스트 생성 으로 링크 걸어주기
    if request.method == 'POST':
        post = Post(
            # SessionMiddleware
            # AuthenticationMiddleware
            #   를 통해서 request의 user속성
            #   해당 사용자 인스턴스가 할당
            author=request.user,
            photo=request.FILES['photo'],
        )
        post.save()
        return redirect('posts:post-list')
    else:
        form = PostCreateForm()
        context = {
            'form': form,
        }
        return render(request, 'posts/post_create.html', context)



