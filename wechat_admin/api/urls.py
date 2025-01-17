from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'vip-packages', views.VIPPackageViewSet)
router.register(r'carousels', views.CarouselViewSet)
router.register(r'categories', views.CategoryViewSet)
router.register(r'questions', views.QuestionViewSet, basename='question')
router.register(r'user-answers', views.UserAnswerViewSet, basename='user-answer')

urlpatterns = [
    path('', include(router.urls)),
]
