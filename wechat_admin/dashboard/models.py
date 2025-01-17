from django.db import models

# Create your models here.

class DailyStats(models.Model):
    date = models.DateField('统计日期', unique=True)
    new_users = models.IntegerField('新增用户数', default=0)
    active_users = models.IntegerField('活跃用户数', default=0)
    new_vip_users = models.IntegerField('新增VIP用户数', default=0)
    total_revenue = models.DecimalField('总收入', max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        verbose_name = '每日统计'
        verbose_name_plural = verbose_name
        ordering = ['-date']

    def __str__(self):
        return str(self.date)
