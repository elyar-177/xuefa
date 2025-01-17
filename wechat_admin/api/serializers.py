from rest_framework import serializers
from users.models import User
from vip.models import VIPPackage, VIPSubscription
from carousel.models import Carousel
from question_bank.models import Category, Question, QuestionOption, UserAnswer

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'nickname', 'avatar', 'phone', 'is_vip', 'gender')
        read_only_fields = ('is_vip',)

class VIPPackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = VIPPackage
        fields = ('id', 'name', 'price', 'duration', 'description', 'features')

class CarouselSerializer(serializers.ModelSerializer):
    class Meta:
        model = Carousel
        fields = ('id', 'title', 'image', 'url')

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'parent')

class QuestionOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionOption
        fields = ('id', 'content', 'order')

class QuestionListSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    
    class Meta:
        model = Question
        fields = ('id', 'category', 'category_name', 'title', 'question_type', 'difficulty')

class QuestionDetailSerializer(serializers.ModelSerializer):
    options = QuestionOptionSerializer(many=True, read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    
    class Meta:
        model = Question
        fields = ('id', 'category', 'category_name', 'title', 'question_type', 
                 'difficulty', 'options', 'answer', 'analysis')

class UserAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAnswer
        fields = ('id', 'question', 'answer', 'is_correct', 'created_at')
        read_only_fields = ('is_correct',)
