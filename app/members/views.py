from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect

from members.forms import LoginForm


def login_view(request):
    # URL: /members/login/
    # config.urls에서 '/members/'부분을 'members.urls'를 사용하도록 include
    # members.urls에서 '/login/'부분을 이 view에 연ㅅ결

    # Template: members/login.html
    # 템플릿에는 아래의 LoginForm 인스턴스를 사용

    # Form: members/forms.py
    # LoginForm
    #   username, password를 받을 수 있도록 함
    #       password는 widget에 PasswordInput을 사용하기
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('posts:post-list')
        else:
            # 인증 실패시
            pass
        # 1. request.POST에 데이터가 옴
        # 2. 온 데이터 중에서 username에 해당하는 값과 password에 해당하는 값을 각각
        #    username, password변수에 할
        # 3. 사용자 인증을 수행
        #    username/password에 해당하는 사용자가 있는지 확인
        # 4-1. 인증에 성공한다면
        #      세션/쿠키 기반의 로그인과정을 수행, 완료 후 posts:post-list 페이지로 redirect
        # 4-2. 인증에 실패한다면
        #      이 페이지에서 인증에 실패했음을 사용자에게 알려줌
    else:
        form = LoginForm()
        context = {
            'form': form,
        }
        return render(request, 'members/login.html', context)


def logout_view(request):
    # URL: /members/logout/
    # Template: 없음

    # !POST 요청일 때만 처리
    # 처리 완료 후 'posts:post-list'로 이동

    # base.html에 있는 'Logout'버튼이 이 view로의 POST요청을 하도록 함
    #   -> form을 구현해야 함
    if request.method == 'POST':
        logout(request)
        return redirect('posts:post-list')


def signup_view(request):
    # URL: /members/signup/
    # Template: members/signup.html
    # Form:
    #   SignupForm
    #       username, password1, password2를 받음
    # 나머지 요소들은 login.html의 요소를 최대한 재활용

    # GET요청시 해당 템플릿 보여주도록 처리
    #   base.html에 이쓴 'Signup'버튼이 이 쪽으로 이동할 수 있도록 url
    pass

