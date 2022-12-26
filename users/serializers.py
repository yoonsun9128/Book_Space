from rest_framework import serializers
from users.models import User, Inquiry, Taste
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from articles.serializers import ArticleImageSerializer, BookRecommendSerializer

class InquirySerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()


    def get_updated_at(self, obj):
        return obj.updated_at.strftime('%Y-%m-%d')

    def get_user(self, obj):
        return obj.user.email

    class Meta:
        model = Inquiry
        fields = "__all__"

class UserSerializer(serializers.ModelSerializer):
    passwordcheck = serializers.CharField(style={'input_type':'password'}, required=False)

    class Meta:
        model = User
        fields = ('email','username' ,'password','passwordcheck')
        extra_kwargs={
            'password':{'write_only':True, 'required': False}
        }


    def update(self, obj, validated_data):
        obj.username = validated_data.get('username', obj.username)
        obj.password = validated_data.get('password', obj.password)
        obj.set_password(obj.password)
        obj.save()
        return obj

    def validate(self, data):
        password=data.get('password')
        passwordcheck=data.get('passwordcheck')
        if password != passwordcheck:
            raise serializers.ValidationError(
                detail={"error":"비밀번호가 맞지 않습니다"}
            )

        if not len(data.get("password", "")) >= 2:
            raise serializers.ValidationError(
                detail={"error": "password의 길이는 8자리 이상이어야합니다."}
            )

        return data
    def validate_email(self, data):
        if User.objects.filter(email=data).exists():
            raise serializers.ValidationError("이메일이 이미 존재합니다.")
        return data

class UserNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username",)

class UserPasswordSerializer(serializers.ModelSerializer):
    passwordcheck = serializers.CharField(style={'input_type':'password'}, required=False)
    class Meta:
        model = User
        fields = ("password", "passwordcheck")
    def update(self, obj, validated_data):
        obj.password = validated_data.get('password', obj.password)
        obj.set_password(obj.password)
        obj.save()
        return obj


class UserMypageSerializer(serializers.ModelSerializer): #마이페이지를 위한 시리얼라이즈
    article_set = ArticleImageSerializer(many=True)
    class Meta:
        model = User
        fields =  ("id","username", "article_set", "profile_img", )

class UserImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("profile_img",)


class RecommendSerializer(serializers.ModelSerializer):
    select_books = BookRecommendSerializer(many=True, read_only=True)
    class Meta:
        model = User
        fields = ("select_books",)

class MainNumberousBookSerializer(serializers.ModelSerializer):
    article_count = serializers.IntegerField(source='article_set.count', read_only=True)
    class Meta:
        model = User
        fields =  ("id","username", "article_count")


class UserChoiceBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Taste
        fields = ("choice",)
