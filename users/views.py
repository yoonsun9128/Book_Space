from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView
from rest_framework import status, permissions
from rest_framework.response import Response
from .models import User, Inquiry
from users.serializers import UserSerializer, UserMypageSerializer, RecommendSerializer, UserImageSerializer, InquirySerializer

from django.http import HttpResponseRedirect
from rest_framework.permissions import AllowAny
from allauth.account.models import EmailConfirmation, EmailConfirmationHMAC

from django.shortcuts import redirect

class MypageView(APIView):
    def get(self, request, user_id):
        user = User.objects.get(id=user_id)
        serializer = UserMypageSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        if request.user == user:
            serializer = UserSerializer(user, data = request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("권한이 없습니다.!", status=status.HTTP_403_FORBIDDEN)

    def delete(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        user.delete()
        return Response(status=status.HTTP_202_ACCEPTED)

class LikeArticlesView(APIView):
    def get(self, request, user_id):
        book = Article.objects.filter(Q(likes=user_id))
        print(book)
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



class ConfirmEmailView(APIView):
    permission_classes = [AllowAny]

    def get(self, *args, **kwargs):
        self.object = confirmation=self.get_object()
        confirmation.confirm(self.request)
        # A React Router Route will handle the failure scenario
        return redirect('http://127.0.0.1:5500/templates/main.html') # 인증성공

    def get_object(self, queryset=None):
        key = self.kwargs['key']
        email_confirmation = EmailConfirmationHMAC.from_key(key)
        if not email_confirmation:
            if queryset is None:
                queryset = self.get_queryset()
            try:
                email_confirmation = queryset.get(key=key.lower())
            except EmailConfirmation.DoesNotExist:
                # A React Router Route will handle the failure scenario
                return HttpResponseRedirect('/') # 인증실패
        return email_confirmation

    def get_queryset(self):
        qs = EmailConfirmation.objects.all_valid()
        qs = qs.select_related("email_address__user")
        return qs

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