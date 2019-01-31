import re

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.decorators.http import require_POST

from .models import Post, Comment, HashTag
from .forms import PostCreateForm, CommentCreateForm, CommentForm, PostForm


def post_list(request):
    posts = Post.objects.all()
    context = {
        'posts': posts,
        'comment_form': CommentForm(),
    }

    return render(request, 'posts/post_list.html', context)


# def post_detail(request):
#     posts = Post.objects.all()
#     context = {
#         'posts': posts,
#         'comment_form': CommentForm(),
#     }
#     return render(request, 'posts/post_detail.html', context)


@require_POST
@login_required
def post_delete(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    if post.author != request.user:
        raise PermissionDenied('지울 권환이 없습니다')
    post.delete()
    return redirect('posts:post-list')


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
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()

            # PostForm에 'comment'값이 전달도었다면
            comment_content = form.cleaned_data['comment']
            # 위에서 생성한 post에 연결되는 Comment생성
            post.comments.create(
                author=request.user,
                content=comment_content,
            )
        return redirect('posts:post-list')
    else:
        form = PostForm()
    context['form'] = form
    return render(request, 'posts/post_create.html', context)


def comment_create(request, post_pk):
    # 1. post_pk에 해당하는 Post객체를 가져와 post변수에 할당
    # 2. request.POST에 전달된 'content'키의 값을 content변수에 할당
    # 3. Comment생성
    #   author: 현재 요청의 User
    #   post: post_pk에 해당하는 Post객체
    #   content: request.POST로 전달된 'content'키의 값
    # 4. posts:post-list로 redirect하기
    # if request.method == 'POST':
    #     post = Post.objects.get(pk=post_pk)
    #     content = request.POST['content']
    #     Comment.objects.create(
    #         author=request.user,
    #         post=post,
    #         content=content,
    #     )
    post = Post.objects.get(pk=post_pk)
    form = CommentForm(request.POST)
    if form.is_valid():
        # form.save(
        #     post=post,
        #     author=request.user,
        # )
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
        url = reverse('posts:post-list')
        return redirect(url+f'#post-{post_pk}')


def tag_post_list(request, tag_name):
    posts = Post.objects.filter(comments__tags__name=tag_name)
    context = {
        'posts': posts,
    }
    return render(request, 'posts/tag_post_list.html', context)


def tag_search(request):
    search_keword = request.GET.get('search_keyword')
    substituted_keyword = re.sub(r'#|\s+', '', search_keword)
    return redirect('tag-post-list', substituted_keyword)


def post_like_toggle(request, post_pk):
    # URL: '/posts/<post_pk>/like-toggle/
    # URL Name: 'posts:post-like-toggle'
    # POST method에 대해서만 처리

    # request.user가 post_pk에 해당하는 Post에
    #   Like Toggle처리
    if request.method == 'POST':
        post = get_object_or_404(Post, pk=post_pk)
        post.like_toggle(request.user)
        url = reverse('posts:post-list')
        # 모델에 like_toggle 함수를 만들어 놓아서 여기서는 가져다 쓰기만하면 된다.
        # 모델에 함수를 따로 만들지 않았으면 여기서 다시 정의해주어야 한다.
        return redirect(url + f'#post-{post_pk}')
