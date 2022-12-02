from rest_framework import serializers
from users.models import User
from store.models import Filter, Comment
from ImageStorage.models import Image
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from store.serializers import OutputImageSerializer

class UserSerializer(serializers.ModelSerializer):
    passwordcheck = serializers.CharField(style={'input_type':'password'}, write_only=True)


    class Meta:
        model = User
        fields = ('email','username','phone_number', 'password','passwordcheck')
        extra_kwargs={
            'password':{'write_only':True}
        }

    def create(self, validated_data):
        user = super().create(validated_data)
        password = user.password
        user.set_password(password)
        user.save()
        return user

    def update(self, obj, validated_data):
        obj.email = validated_data.get('email', obj.email)
        obj.password = validated_data.get('password', obj.password)
        obj.username = validated_data.get('username', obj.username)
        obj.set_password(obj.password)
        obj.save()
        return obj


    def validate(self, data):
        email = User.objects.filter(email=data['email'])
        password=data.get('password')
        passwordcheck=data.pop('passwordcheck')
        if password != passwordcheck:
            raise serializers.ValidationError(
                detail={"error":"비밀번호가 맞지 않습니다"}
            )


        if not len(data.get("email", "")) >= 2:
            raise serializers.ValidationError(
                detail={"error": "email 길이는 2자리 이상이어야 합니다."}
            )

        if not len(data.get("password", "")) >= 2:
            raise serializers.ValidationError(
                detail={"error": "password의 길이는 8자리 이상이어야합니다."}
            )


        if email.exists():
            raise serializers.ValidationError('이메일이 이미 존재합니다.')

        return data

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['email'] = user.email

        return token