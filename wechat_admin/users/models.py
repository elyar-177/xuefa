from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    GENDER_CHOICES = (
        ('M', '男'),
        ('F', '女'),
        ('U', '未知'),
    )
    
    nickname = models.CharField('昵称', max_length=50, blank=True)
    phone = models.CharField('手机号', max_length=11, unique=True, null=True, blank=True)
    avatar = models.ImageField('头像', upload_to='avatars/', null=True, blank=True)
    gender = models.CharField('性别', max_length=1, choices=GENDER_CHOICES, default='U')
    openid = models.CharField('微信OpenID', max_length=100, unique=True, null=True, blank=True)
    register_date = models.DateTimeField('注册时间', auto_now_add=True)
    last_login_date = models.DateTimeField('最后登录时间', auto_now=True)
    is_vip = models.BooleanField('是否是VIP', default=False)
    
    class Meta:
        verbose_name = '用户'
        verbose_name_plural = verbose_name
        
    def __str__(self):
        return self.nickname or self.username
