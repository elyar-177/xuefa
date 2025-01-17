from django.db import models
from users.models import User

class Category(models.Model):
    """题目分类"""
    name = models.CharField('分类名称', max_length=100)
    parent = models.ForeignKey('self', verbose_name='父分类', null=True, blank=True, on_delete=models.CASCADE)
    order = models.IntegerField('排序', default=0)
    is_active = models.BooleanField('是否启用', default=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        verbose_name = '题目分类'
        verbose_name_plural = verbose_name
        ordering = ['order', 'id']

    def __str__(self):
        if self.parent:
            return f'{self.parent.name} - {self.name}'
        return self.name

class Question(models.Model):
    """题目"""
    DIFFICULTY_CHOICES = (
        (1, '简单'),
        (2, '中等'),
        (3, '困难'),
    )
    
    TYPE_CHOICES = (
        ('single', '单选题'),
        ('multiple', '多选题'),
        ('judge', '判断题'),
        ('fill', '填空题'),
        ('essay', '问答题'),
    )

    category = models.ForeignKey(Category, verbose_name='分类', on_delete=models.CASCADE)
    title = models.TextField('题目内容')
    question_type = models.CharField('题目类型', max_length=10, choices=TYPE_CHOICES)
    difficulty = models.IntegerField('难度', choices=DIFFICULTY_CHOICES, default=1)
    answer = models.TextField('答案')
    analysis = models.TextField('解析', blank=True)
    is_active = models.BooleanField('是否启用', default=True)
    created_by = models.ForeignKey(User, verbose_name='创建人', on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        verbose_name = '题目'
        verbose_name_plural = verbose_name
        ordering = ['-created_at']

    def __str__(self):
        return self.title[:50]

class QuestionOption(models.Model):
    """选项（用于单选题和多选题）"""
    question = models.ForeignKey(Question, verbose_name='题目', related_name='options', on_delete=models.CASCADE)
    content = models.CharField('选项内容', max_length=500)
    is_correct = models.BooleanField('是否正确答案', default=False)
    order = models.IntegerField('排序', default=0)

    class Meta:
        verbose_name = '题目选项'
        verbose_name_plural = verbose_name
        ordering = ['order']

    def __str__(self):
        return self.content

class UserAnswer(models.Model):
    """用户答题记录"""
    user = models.ForeignKey(User, verbose_name='用户', on_delete=models.CASCADE)
    question = models.ForeignKey(Question, verbose_name='题目', on_delete=models.CASCADE)
    answer = models.TextField('用户答案')
    is_correct = models.BooleanField('是否正确', default=False)
    created_at = models.DateTimeField('答题时间', auto_now_add=True)

    class Meta:
        verbose_name = '答题记录'
        verbose_name_plural = verbose_name
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user.username} - {self.question.title[:30]}'
