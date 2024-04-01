from rest_framework import generics
from api.serializers.user import RegisterSerializer

from accounts.models import User

from  rest_framework_simplejwt.views import TokenObtainPairView
from api.serializers.user import CustomTokenObtainPairSerializer


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.user
        response.data['username'] = user.username
        return response