from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect

from .forms import LoginForm, SignupForm


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


@login_required
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
    context = {}
    if request.method == 'POST':
        # Django의 Form
        # 1. HTML위젯 생성
        # 2. 요청(request)으로부터 데이터를 받는 역할
        # 3. 받아온 데이터를 유효성 검증
        # 4. 유효성 검증에 실패한 원인을 출력

        # POST로 전달된 데이터를 확인
        # 올바르다면 User를 생성하고 post-list화면으로 이동
        # (is_valid()가 True면 올바르다고 가정)
        form = SignupForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1'],
            )
            login(request, user)
            return redirect('posts:post-list')
        # Form이 유효하지 않을 경우,
        # Bound된 상태로 if-else구문 아래의 render까지 이동
    else:
        # GET요청 시 빈 Form을 생성
        form = SignupForm()

    # GET요청시 또는 POST로 전달된 데이터가 올바르지 않을경우
    #   signup.html에
    #   빈 Form 또는 올바르지 않은 데이터에 대한 정보가 포함된
    #   포함된 Form을 전달해서 동적으로 form을 렌더링

    context['form'] = form
    return render(request, 'members/signup.html', context)
