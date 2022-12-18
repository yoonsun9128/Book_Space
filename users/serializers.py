from rest_framework import serializers
from users.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from articles.serializers import ArticleImageSerializer, BookRecommendSerializer


class UserSerializer(serializers.ModelSerializer):
    passwordcheck = serializers.CharField(style={'input_type':'password'}, write_only=True)

    class Meta:
        model = User
        fields = ('email','username' ,'password','passwordcheck')
        extra_kwargs={
            'password':{'write_only':True}
        }

    def update(self, obj, validated_data):
        # obj.profile_img = validated_data.get('profile_img', obj.profile_img)
        obj.password = validated_data.get('password', obj.password)
        obj.username = validated_data.get('username', obj.username)
        obj.set_password(obj.password)
        obj.save()
        return obj

    def validate(self, data):
        password=data.get('password')
        passwordcheck=data.pop('passwordcheck')
        if password != passwordcheck:
            raise serializers.ValidationError(
                detail={"error":"비밀번호가 맞지 않습니다"}
            )

        if not len(data.get("password", "")) >= 2:
            raise serializers.ValidationError(
                detail={"error": "password의 길이는 8자리 이상이어야합니다."}
            )

        return data


class UserMypageSerializer(serializers.ModelSerializer): #마이페이지를 위한 시리얼라이즈
    article_set = ArticleImageSerializer(many=True)
    class Meta:
        model = User
        fields =  ("id","username", "article_set", "profile_img" )

class UserImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("profile_img",)


class RecommendSerializer(serializers.ModelSerializer):
    select_books = BookRecommendSerializer(many=True, read_only=True)
    class Meta:
        model = User
        fields = ("select_books",)