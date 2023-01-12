from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView
from rest_framework import status, permissions
from rest_framework.response import Response
from django.shortcuts import render
from articles.models import Article
from .models import User, Inquiry, Taste
from users.serializers import UserSerializer, UserMypageSerializer, RecommendSerializer, UserImageSerializer, InquirySerializer, MainNumberousBookSerializer, UserChoiceBookSerializer, UserNameSerializer,UserPasswordSerializer
from articles.serializers import ArticleImageSerializer
from articles.models import Article
from django.db.models import Q, Count
from django.contrib.auth.hashers import check_password
from rest_framework_simplejwt.views import ( TokenObtainPairView,TokenRefreshView, )
from users.serializers import CustomTokenObtainPairSerializer
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from users.token import account_activation_token
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView
from django.contrib.auth.forms import PasswordResetForm
import traceback

class UserView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message":"가입완료"}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class UserActivate(APIView):
    permission_classes = (permissions.AllowAny, )
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        try:
            if user is not None and account_activation_token.check_token(user, token):
                user.is_active = True
                user.save()
                return Response(user.email + '계정이 활성화 되었습니다', status=status.HTTP_200_OK)
            else:
                return Response('만료된 링크입니다.', status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(traceback.format_exc())

# 패스워드 변경
class PasswordResetView(PasswordResetView):
    template_name = 'user/password_reset.html'
    form_class = PasswordResetForm

    def check_email(self, form):
        if User.objects.filter(email=self.request.POST.get('email')) is not None :
            return super().check_email(form)
        else:
            return render (self.request, 'user/password_reset_done_fail.html' )

# class PasswordResetView(APIView):
#     def post(self, request):
#         print(request.data['email'])
#         user = User.objects.filter(email=request.data['email'])
#         if user is not None:
#             print("통과")
#             serializer = UserPasswordResetSerializer(data=request.data)
#             print("통과dddd")
#             if serializer.is_valid():
#                 print("통과2")
#                 serializer.save()
#                 return Response({"message":"메일인증 완료"}, status=status.HTTP_202_ACCEPTED)
#             else:
#                 return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)
#         else:
#             return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)

class MypageView(APIView):
    def get(self, request, user_id):
        user = User.objects.get(id=user_id)
        serializer = UserMypageSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        data = request.data
        print(data)
        if request.user == user:
            if check_password(data['now_password'],user.password) == True:
                if data['password'] =="":
                    data = dict({key:value for key, value in data.items() if value !=""})
                    serializer = UserNameSerializer(user, data = request.data, partial=True)
                    if serializer.is_valid():
                        serializer.save()
                        return Response(serializer.data, status=status.HTTP_200_OK)
                    else:
                        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                elif data['username'] =="":
                    data = dict({key:value for key, value in data.items() if value !=""})
                    serializer = UserPasswordSerializer(user, data = request.data, partial=True)
                    if serializer.is_valid():
                        serializer.save()
                        return Response(serializer.data, status=status.HTTP_200_OK)
                    else:
                        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                else:
                    serializer = UserSerializer(user, data = request.data, partial=True)
                    if serializer.is_valid():
                        serializer.save()
                        return Response(serializer.data, status=status.HTTP_200_OK)
                    else:
                        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else: return Response("현재 비밀번호가 틀렸습니다.", status=status.HTTP_403_FORBIDDEN)
        else:
            return Response("권한이 없습니다.!", status=status.HTTP_403_FORBIDDEN)

    def delete(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        if user == request.user:
            user.delete()
            return Response(status=status.HTTP_202_ACCEPTED)
        else:
            return Response("해당 사용자가 아닙니다.", status=status.HTTP_401_UNAUTHORIZED)

class LikeArticlesView(APIView):
    def get(self, request, user_id):
        book = Article.objects.filter(Q(likes=user_id))
        serializer = ArticleImageSerializer(book, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class MypageImage(APIView): #프로필 이미지만 수정파트
    def put(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        if request.user == user:
            serializer = UserImageSerializer(user, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("권한이 없습니다.!", status=status.HTTP_403_FORBIDDEN)


class RecommendView(APIView):
    def post(self, request):
        serializer = RecommendSerializer(data=request.data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class InquiryView(APIView):
    def get(self, request):
        inquiry = Inquiry.objects.all().order_by('-id')
        serializer = InquirySerializer(inquiry, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = InquirySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

class MostNumberousBook(APIView):
    def get(self, request):
        user = User.objects.all().annotate(num_likes=Count('article')).order_by('-num_likes', 'id')[:3]
        serializer = MainNumberousBookSerializer(user, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserChoiceBook(APIView):
    def post(self, request):
        book_dict = request.data
        book_list = book_dict.get("choice")
        user = Taste.objects.filter(user_id=request.user)
        if user.count() >= 1:
            user.delete()
        for i in book_list:
            serializer = UserChoiceBookSerializer(data={"choice":i})
            if serializer.is_valid():
                serializer.save(user=request.user)
        return Response(serializer.data)



