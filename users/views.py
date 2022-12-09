from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework_simplejwt.views import ( TokenObtainPairView,TokenRefreshView, )
from .models import User
from users.serializers import CustomTokenObtainPairSerializer, UserSerializer, UserMypageSerializer, ProfileSerializer, RecommendSerializer

from django.http import HttpResponseRedirect
from rest_framework.permissions import AllowAny
from allauth.account.models import EmailConfirmation, EmailConfirmationHMAC

from django.shortcuts import redirect



class UserView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message":"가입완료"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"message":f"${serializer.errors}"}, status=status.HTTP_400_BAD_REQUEST)

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class MypageView(APIView):
    def get(self, request, user_id):
        user = User.objects.get(id=user_id)
        serializer = UserMypageSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        if request.user == user:
            serializer = ProfileSerializer(user, data = request.data, partial=True)
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
            

