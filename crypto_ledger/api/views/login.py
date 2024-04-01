from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from api.models import User
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['POST'])
def password_rest(request):
    email = request.data.get('email')
    user = User.objects.get(email=email)
    if user:
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        reset_url = f'http://localhost:5173/reset-password/{uid}/{token}'
        send_mail(
            'Password Reset Requested',
            f'Follow this link to rest your password: {reset_url}',
            'test@test.com',
            [user.email],
            fail_silently=False,
        )
    return Response({'message': 'Password reset email has been sent.'})
            