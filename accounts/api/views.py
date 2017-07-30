

from django.contrib.auth import get_user_model

from cocktail.api.pagination import LargeResultsSetPagination, StandardResultsSetPagination

from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import RegisterSerializer, LoginSerializer, UserSerializer

from rest_framework.permissions import AllowAny


User = get_user_model()

class RegisterAPIView(CreateAPIView):
    serializer_class = RegisterSerializer
    pagination_class = StandardResultsSetPagination
    queryset = User.objects.all()
    permission_classes = [AllowAny]

class LoginAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = LoginSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            new_data = serializer.data
            return Response(new_data, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class UserAPIView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # permission_classes = [AllowAny]







