from django.db import models
from users.models import User

# Create your models here.

class VIPPackage(models.Model):
    name = models.CharField('套餐名称', max_length=100)
    price = models.DecimalField('价格', max_digits=10, decimal_places=2)
    duration = models.IntegerField('时长(天)')
    description = models.TextField('套餐描述')
    features = models.TextField('特权说明')
    is_active = models.BooleanField('是否启用', default=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        verbose_name = 'VIP套餐'
        verbose_name_plural = verbose_name
        ordering = ['price']

    def __str__(self):
        return self.name

class VIPSubscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='用户')
    package = models.ForeignKey(VIPPackage, on_delete=models.PROTECT, verbose_name='套餐')
    start_date = models.DateTimeField('开始时间', auto_now_add=True)
    end_date = models.DateTimeField('结束时间')
    is_active = models.BooleanField('是否有效', default=True)
    payment_id = models.CharField('支付订单号', max_length=100, unique=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        verbose_name = 'VIP订阅'
        verbose_name_plural = verbose_name
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user.username} - {self.package.name}'
