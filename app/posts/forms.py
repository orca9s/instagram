from django import forms

from .models import Post, Comment


class PostCreateForm(forms.Form):
    photo = forms.ImageField(
        # 이 필드는 파일입력 위젯을 사용
        widget=forms.FileInput(
            # HTML위젯의 속성 설정
            #   form-control-file클래스를 사용
            attrs={
                'class': 'form-control-file'
            }
        )
    )
    comment = forms.CharField(
        # 반드시 채워져 있을 필요는 없음
        required=False,
        # HTML랜더링 위젯으로 textarea를 사용
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
            }
        ),
    )

    def save(self, **kwargs):
        post = Post.objects.create(
            photo=self.cleaned_data['photo'],
            **kwargs,
        )
        # 만약에 comment항목이 있다면
        # 생성한 Post에 연결되는 Comment를 생성
        #   author = request.user
        #   post=post가 되도록
        comment_content = self.cleaned_data.get('comment')
        if comment_content:
            post.comments.create(
                author=post.author,
                content=comment_content,
            )
        return post


class CommentCreateForm(forms.Form):
    content = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'rows': 2,
            }
        )
    )

    def save(self, post, **kwargs):
        content = self.cleaned_data['content']
        return post.comments.create(
            content=content,
            **kwargs,
        )


class PostForm(forms.ModelForm):
    comment = forms.CharField(
        label='내용',
        required=False,
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'rows': 2,
            }
        )
    )
    # 일딴은 다른 방법으로 처리 지금 건들기에는 너무 어렵다.
    # def save(self, *args, **kwargs):
    #     if 'author' not in kwargs:
    #         raise  ValueError('PostForm.save()에는 반드시 author항목이 포함되어야 합니다')
    #     if kwargs.get('commit', True) is False:
    #         raise ValueError('PostForm은 반드시 commit=True여야 합니다')
    #     # post인스턴스는 무조건 commit=True(DB에 저장된 모델)상태
    #     post = super().save(*args, **kwargs)
    #     comment_content = self.cleaned_data['comment']
    #     if comment_content:
    #         post.comments.create(
    #
    #         )


    class Meta:
        model = Post
        fields = [
            'photo',
        ]
        widgets = {
            'photo': forms.ClearableFileInput(
                attrs={
                    'class': 'form-control-file',
                }
            )
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = [
            'content',
        ]
        widgets = {
            'content': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 2,
                }
            )
        }

