from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework_jwt.settings import api_settings
JWT_PAYLOAD_HANDLER = api_settings.JWT_PAYLOAD_HANDLER
JWT_ENCODE_HANDLER = api_settings.JWT_ENCODE_HANDLER


from .models import EntryModel

class NewUserSerializer(serializers.ModelSerializer):
    username = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())],
        max_length=100, 
        required=True)
    password = serializers.CharField(
        max_length=100,
        min_length = 4,
        write_only=True,
        required=True
    )
    
    class Meta:
        model=User
        fields=['username','password']
        
    def create(self,validated_data):
        return User.objects.create_user(**validated_data)


class EntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = EntryModel
        fields = ['date','entry', 'entry_body', 'amount','owner']

import pdb
class LoginSerializer(serializers.Serializer):
    username = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())],
        max_length=100, 
        required=True)
    password = serializers.CharField(
        max_length=100,
        min_length = 4,
        write_only=True,
        required=True
    )

    def validate(self, data):
        pdb.set_trace()
        email = data['username']
        password = data['password']
        user = authenticate(username=email, password=password)
        if user is not None:
            payload = JWT_PAYLOAD_HANDLER(user)
            token = JWT_ENCODE_HANDLER(payload)
            return {
                'email':user.username,
                'token':token
                }
        return {'result' : 'login info dne'}
        