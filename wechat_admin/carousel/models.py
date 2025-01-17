from django.db import models

# Create your models here.

class Carousel(models.Model):
    title = models.CharField('标题', max_length=100)
    image = models.ImageField('轮播图', upload_to='carousel/')
    url = models.URLField('链接', blank=True, null=True)
    order = models.IntegerField('排序', default=0)
    is_active = models.BooleanField('是否启用', default=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        verbose_name = '轮播图'
        verbose_name_plural = verbose_name
        ordering = ['order', '-created_at']

    def __str__(self):
        return self.title
