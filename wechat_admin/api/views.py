from django.shortcuts import render
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings
from users.models import User
from vip.models import VIPPackage, VIPSubscription
from carousel.models import Carousel
from question_bank.models import Category, Question, QuestionOption, UserAnswer
from .serializers import (
    UserSerializer, VIPPackageSerializer, CarouselSerializer,
    CategorySerializer, QuestionListSerializer, QuestionDetailSerializer,
    UserAnswerSerializer
)
import json
import requests

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.action == 'wx_login':
            return [permissions.AllowAny()]
        return super().get_permissions()

    @action(detail=False, methods=['POST'])
    def wx_login(self, request):
        code = request.data.get('code')
        if not code:
            return Response({'error': '需要微信code'}, status=status.HTTP_400_BAD_REQUEST)

        # 从settings获取微信配置
        appid = settings.WECHAT_MINI_APP['APP_ID']
        secret = settings.WECHAT_MINI_APP['APP_SECRET']
        
        # 请求微信接口
        url = f'https://api.weixin.qq.com/sns/jscode2session'
        params = {
            'appid': appid,
            'secret': secret,
            'js_code': code,
            'grant_type': 'authorization_code'
        }
        
        try:
            response = requests.get(url, params=params)
            data = response.json()
            
            if 'errcode' in data:
                return Response({
                    'error': f"微信登录失败: {data.get('errmsg', '未知错误')}"
                }, status=status.HTTP_400_BAD_REQUEST)
                
            if 'openid' not in data:
                return Response({
                    'error': '微信登录失败: 未获取到openid'
                }, status=status.HTTP_400_BAD_REQUEST)
                
            # 获取或创建用户
            user, created = User.objects.get_or_create(
                openid=data['openid'],
                defaults={
                    'username': f"wx_{data['openid'][:8]}",
                    'nickname': request.data.get('nickname', ''),
                    'avatar': request.data.get('avatar', '')
                }
            )
            
            # 如果用户已存在但有新的信息，更新用户信息
            if not created:
                update_fields = []
                if 'nickname' in request.data and request.data['nickname']:
                    user.nickname = request.data['nickname']
                    update_fields.append('nickname')
                if 'avatar' in request.data and request.data['avatar']:
                    user.avatar = request.data['avatar']
                    update_fields.append('avatar')
                if update_fields:
                    user.save(update_fields=update_fields)
            
            # 生成JWT令牌
            refresh = RefreshToken.for_user(user)
            
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': UserSerializer(user).data,
                'is_new_user': created
            })
            
        except requests.RequestException as e:
            return Response({
                'error': f'网络请求错误: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response({
                'error': f'服务器错误: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class VIPPackageViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = VIPPackage.objects.filter(is_active=True)
    serializer_class = VIPPackageSerializer
    permission_classes = [permissions.IsAuthenticated]

class CarouselViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Carousel.objects.filter(is_active=True)
    serializer_class = CarouselSerializer
    permission_classes = [permissions.IsAuthenticated]

class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.filter(is_active=True)
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]

class QuestionViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = Question.objects.filter(is_active=True)
        category = self.request.query_params.get('category', None)
        if category:
            queryset = queryset.filter(category_id=category)
        return queryset

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return QuestionDetailSerializer
        return QuestionListSerializer

    @action(detail=True, methods=['POST'])
    def submit_answer(self, request, pk=None):
        question = self.get_object()
        answer = request.data.get('answer', '')
        
        # 创建答题记录
        user_answer = UserAnswer.objects.create(
            user=request.user,
            question=question,
            answer=answer
        )
        
        # 判断答案是否正确
        if question.question_type in ['single', 'multiple']:
            correct_options = set(question.options.filter(is_correct=True).values_list('id', flat=True))
            try:
                user_options = set(json.loads(answer))
                is_correct = correct_options == user_options
            except:
                is_correct = False
        elif question.question_type == 'judge':
            is_correct = answer.lower() == question.answer.lower()
        else:
            # 填空题和问答题需要人工判断
            is_correct = False
            
        user_answer.is_correct = is_correct
        user_answer.save()
        
        return Response({
            'is_correct': is_correct,
            'correct_answer': question.answer,
            'analysis': question.analysis
        })

class UserAnswerViewSet(viewsets.ModelViewSet):
    serializer_class = UserAnswerSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return UserAnswer.objects.filter(user=self.request.user)
