from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import Category, Question, QuestionOption, UserAnswer

class CategoryResource(resources.ModelResource):
    class Meta:
        model = Category
        fields = ('id', 'name', 'parent', 'order', 'is_active')

@admin.register(Category)
class CategoryAdmin(ImportExportModelAdmin):
    resource_class = CategoryResource
    list_display = ('name', 'parent', 'order', 'is_active', 'created_at')
    list_filter = ('is_active', 'parent')
    search_fields = ('name',)
    ordering = ('order',)
    list_editable = ('order', 'is_active')

class QuestionOptionInline(admin.TabularInline):
    model = QuestionOption
    extra = 4
    fields = ('content', 'is_correct', 'order')

class QuestionResource(resources.ModelResource):
    class Meta:
        model = Question
        fields = ('id', 'category', 'title', 'question_type', 'difficulty', 'answer', 'analysis', 'is_active', 'created_by')

@admin.register(Question)
class QuestionAdmin(ImportExportModelAdmin):
    resource_class = QuestionResource
    list_display = ('title_display', 'category', 'question_type', 'difficulty_display', 'is_active', 'created_by', 'created_at')
    list_filter = ('is_active', 'question_type', 'difficulty', 'category')
    search_fields = ('title', 'answer', 'analysis')
    inlines = [QuestionOptionInline]
    readonly_fields = ('created_by',)
    
    fieldsets = (
        ('基本信息', {
            'fields': ('category', 'title', 'question_type', 'difficulty')
        }),
        ('答案与解析', {
            'fields': ('answer', 'analysis')
        }),
        ('状态', {
            'fields': ('is_active', 'created_by')
        }),
    )
    
    def title_display(self, obj):
        return format_html('<div style="width: 400px; word-wrap: break-word;">{}</div>', obj.title[:100])
    title_display.short_description = '题目内容'
    
    def difficulty_display(self, obj):
        colors = {1: '#28a745', 2: '#ffc107', 3: '#dc3545'}
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            colors[obj.difficulty],
            obj.get_difficulty_display()
        )
    difficulty_display.short_description = '难度'
    
    def save_model(self, request, obj, form, change):
        if not change:  # 如果是新建，设置创建人
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

@admin.register(UserAnswer)
class UserAnswerAdmin(ImportExportModelAdmin):
    list_display = ('user', 'question_display', 'answer_display', 'is_correct', 'created_at')
    list_filter = ('is_correct', 'created_at', 'question__category')
    search_fields = ('user__username', 'question__title')
    readonly_fields = ('user', 'question', 'answer', 'is_correct', 'created_at')
    
    def question_display(self, obj):
        return format_html('<div style="width: 300px; word-wrap: break-word;">{}</div>', obj.question.title[:80])
    question_display.short_description = '题目'
    
    def answer_display(self, obj):
        return format_html('<div style="width: 200px; word-wrap: break-word;">{}</div>', obj.answer[:50])
    answer_display.short_description = '答案'
    
    def has_add_permission(self, request):
        return False
