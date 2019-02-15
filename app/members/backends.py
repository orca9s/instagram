import imghdr

import requests
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile

User = get_user_model()


class FacebookBackend:
    def authenticate(self, request, facebook_request_token):
        api_base = 'https://graph.facebook.com/v3.2'
        api_get_access_token = f'{api_base}/oauth/access_token'
        api_me = f'{api_base}/me'
        # URL: /members/facebook-login/
        # URL name: 'members:facebook-login'
        # request.GET에 전달된 'code'값읋
        # 그대로 HttpResponse로 출력

        # 페이스북으로부터 받아온 request token
        code = facebook_request_token

        # request token을 access token으로 교환
        # params를 사용해서 키 밸류 형태의 dict타입으로 보내줌
        # get요청에 자동으로 뒤에 변형해서 넣도록 하는것 을 requests가 제공
        params = {
            'client_id': settings.FACEBOOK_APP_ID,
            'redirect_uri': 'http://localhost:8000/members/facebook-login/',
            'client_secret': settings.FACEBOOK_APP_SECRET,
            'code': code,
        }

        response = requests.get(api_get_access_token, params)
        # 인수로 전달한 문자열이 'JSON'형식일 것으로 생각
        # json.loads는 전달한 문자열이 JSON형식일 경우, 해당 문자열을 parsing해서 파이썬 Object를 리턴
        # response_object = json.loads(response.text)
        # return HttpResponse(response_object)
        # 위 방식이 아니라 아래의 방식을 사용하면 자동으로 json으로 변역해서
        # 그 결과를 바로 파이썬 객체로 돌려준다.
        data = response.json()
        access_token = data['access_token']

        # access_token을 사용해서 사용자 정보를 가져오기
        params = {
            'access_token': access_token,
            'fields': ','.join([
                'id',
                'first_name',
                'last_name',
                'picture.type(large)',
            ]),
        }
        response = requests.get(api_me, params)
        data = response.json()

        facebook_id = data['id']
        first_name = data['first_name']
        last_name = data['last_name']
        url_img_profile = data['picture']['data']['url']
        # HTTP GET요청의 응답을 받아옴
        img_response = requests.get(url_img_profile)
        img_data = img_response.content

        # 응답의 binary data를 사용해서 In-memory binary stream(file)객체를 생성
        # 이렇게 안하고 FilleField가 지원한 InMemoryUploadedFille객체를 사용하기!
        # f = io.BytesIO(img_response.content)

        # 위처럼 안하고 아래 simpleuploaded쓰면 간편히 해결 되지만 파일의 이름을
        # 꼭 정해주어야 한다.

        # imghdr모듈을 사용해 Image binary data의 확장자를 알아냄
        ext = imghdr.what('', h=img_data)
        # Form에서 업로드한 것과 같은 형태의 file-like object생성
        # 직접 메모리상에서 객체를 만들면 이름이 없기 때문에 이름을 지어 주어야한다.
        # 문제는 확장자를 모르기 때문에 파이썬이 가지고 있는 모듈을 써서 확장자를 가져와야 한다.
        f = SimpleUploadedFile(f'{facebook_id}.{ext}', img_response.content)

        try:
            user = User.objects.get(username=facebook_id)
            # update_or_create
            user.last_name = last_name
            user.first_name = first_name
            # user.img_profile = f
            user.save()
        except User.DoesNotExist:
            user = User.objects.create_user(
                username=facebook_id,
                first_name=first_name,
                last_name=last_name,
                img_profile=f,
            )

        return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
