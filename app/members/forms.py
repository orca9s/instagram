from django import forms


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
