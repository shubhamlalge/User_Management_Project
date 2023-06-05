from django.contrib.auth.tokens import PasswordResetTokenGenerator, default_token_generator
from django.core.mail import send_mail
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from rest_framework import status

from rest_framework.decorators import api_view
import six
from usermanagement import settings
from .pagination import CustomPagination
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListAPIView, CreateAPIView, get_object_or_404, RetrieveUpdateAPIView, \
    RetrieveDestroyAPIView

from rest_framework.views import APIView
from rest_framework.authtoken.views import Token
from django.contrib.auth import authenticate, login, logout
from rest_framework.response import Response
from .models import User
from .serializer import UserSerializer, LoginSerializer, ChangePasswordSerializer, CustomUpdateSerializer


class CreateUser(CreateAPIView):
    '''This class is used for user creation'''
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        '''This method is used for convert password into hash password'''
        instance = serializer.save()
        instance.set_password(instance.password)
        instance.save()

        uid = urlsafe_base64_encode(force_bytes(instance.pk))
        token = account_activation_token.make_token(instance)
        subject = "Account Verification link"
        message = 'Click on the below link\n\nhttp://127.0.0.1:8000/activate/' + str(uid) + '/' + str(token) + '/'
        send_mail(subject, message, settings.EMAIL_HOST_USER, [instance.email], fail_silently=False)


@api_view(('GET',))
def activate(request, uidb64, token):
    '''
    This function is used for activate a user for login
    '''

    try:
        uid = force_bytes(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except User.DoesNotExist:
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return Response('user activate succesfully')
    else:
        return Response('Activation link is invalid!')


class UserList(ListAPIView):
    ''' This is a class for retrieve a data  '''

    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterSet_fields = ['id', 'username', 'email']
    search_fields = ['first_name', 'Last_name']

    def get_queryset(self):
        '''This function is used to give access to view data only that user for authenticated user  '''

        if self.request.user.is_superuser:
            return User.objects.all()
        elif self.request.user.is_authenticated:
            return User.objects.filter(id=self.request.user.id)
        else:
            return User.objects.none()


class RetrieveUpdate(RetrieveUpdateAPIView):
    """ This is a class for update or delete a data  """

    queryset = User.objects.all()
    serializer_class = CustomUpdateSerializer

    def get_queryset(self):

        if self.request.user.is_superuser:
            return User.objects.all()

        if self.request.user.is_authenticated:
            return User.objects.filter(id=self.request.user.id)
        else:
            raise User.objects.none()


class RetrieveDelete(RetrieveDestroyAPIView):
    """ This is a class for update or delete a data  """

    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_queryset(self):
        if self.request.user.is_superuser:
            return User.objects.all()

        if self.request.user.is_authenticated:
            return User.objects.filter(id=self.request.user.id)
        else:
            raise User.objects.none()


class Login(APIView):
    ''' This class is used to log in purpose '''

    def post(self, request):
        '''
        This function is post request for login a user by taking username and password
        '''
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:

            user = authenticate(username=serializer.validated_data['username'],
                                password=serializer.validated_data['password'])
        except:
            return Response({'error': 'user Does not exist'})

        if user:
            login(request, user)
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key, 'id': user.id})
        else:
            return Response({'error': 'Invalid credentials'}, status=400)


class Logout(APIView):
    '''This class is used to log out purpose'''

    def post(self, request):
        user = request.user
        if user.is_authenticated:
            token = Token.objects.filter(user=user)
            token.delete()
            logout(request)
            return Response({'message': 'Logged out'})
        else:
            return Response({'error': 'User is not authenticated'}, status=400)


class TokenGenerator(PasswordResetTokenGenerator):
    '''
    This class is used for generate a token
    '''

    def _make_hash_value(self, user, timestamp):
        return six.text_type(user.pk) + six.text_type(timestamp) + six.text_type(user.is_active)


account_activation_token = TokenGenerator()


class ForgetPassword(APIView):
    '''
    This class is used for forget password in that user send a link for reset password
    '''

    def post(self, request):
        email = request.data.get('email')
        user = get_object_or_404(User, email=email)
        token = default_token_generator.make_token(user)
        reset_link = f'http:////127.0.0.1:8000/reset/{user.id}/{token}'
        message = f'Click the following link to reset password: {reset_link}'
        send_mail('Password Reset', message, 'shubhamlalge10@gmail.com', [user.email])
        return Response({'message': 'Password reset link send to email'}, status=status.HTTP_200_OK)


class ChangePassword(APIView):
    '''
    This class is used for change password by using serializer
    '''

    def post(self, request, user_id, token):
        user = get_object_or_404(User, id=user_id)

        if not default_token_generator.check_token(user, token):
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user.set_password(serializer.validated_data['new_password'])
        user.save()

        return Response({'message': 'Password reset succesfully'}, status=status.HTTP_200_OK)
