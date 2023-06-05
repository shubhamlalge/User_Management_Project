from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    '''
    This serializer class is used for all fields
    '''

    class Meta:
        model = User
        fields = '__all__'


class LoginSerializer(serializers.Serializer):
    '''
    This serializer class is used for login purpose it contains username and password
    '''
    username = serializers.CharField(max_length=200)
    password = serializers.CharField(max_length=200)


class ChangePasswordSerializer(serializers.Serializer):
    '''
        This Serializer class is used for reset password it contains new and confirm password
    '''
    model = User

    new_password = serializers.CharField(max_length=128)
    confirm_password = serializers.CharField(max_length=128)

    def validate(self, attrs):
        '''
        function for validating new password and confirm password
        '''

        new_password = attrs.get('new_password')
        confirm_password = attrs.get('confirm_password')

        if new_password != confirm_password:
            raise serializers.ValidationError("password do not match")

        return attrs


class CustomUpdateSerializer(serializers.ModelSerializer):
    '''This serilizer class for exclude update fields'''
    class Meta:
        model = User

        exclude = ['username', 'email', 'password']
