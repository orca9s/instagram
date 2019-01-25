import re

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Post, Comment, HashTag
from .forms import PostCreateForm, CommentCreateForm, CommentForm, PostForm


def post_list(request):
    posts = Post.objects.all()
    context = {
        'posts': posts,
        'comment_form': CommentForm(),
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

        return redirect('posts:post-list')


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
