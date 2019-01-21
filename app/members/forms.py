from django import forms
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    username = forms.CharField(
        # 일반 input[tpye=text]
        # form-control css클래스 사용
        #   (bootstrap규칙)
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    password = forms.CharField(
        # input[type=password]
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
            }
        )
    )


class SignupForm(forms.Form):
    username = forms.CharField(
        label='사용자명',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    password1 = forms.CharField(
        label='비밀번호',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    password2 = forms.CharField(
        label='비밀번호 학인',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
            }
        )
    )

    def clean_username(self):
        # username이 유일한지 검사
        data = self.cleaned_data['username']
        if User.objects.filter(username=data).exists():
            self.fields['username'].widget.attrs['class'] += ' is-invalid'
            raise forms.ValidationError('이미 사용중인 사용자명입니다')
        return data

    def clean_password2(self):
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        if password1 != password2:
            self.fields['password1'].widget.attrs['class'] += ' is-invalid'
            self.fields['password2'].widget.attrs['class'] += ' is-invalid'
            raise forms.ValidationError('비밀번호와 비밀번호 확인이 다릅니다')
        return password2