from django.contrib import admin
from django.utils.html import format_html
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import Carousel

class CarouselResource(resources.ModelResource):
    class Meta:
        model = Carousel
        fields = ('id', 'title', 'url', 'order', 'is_active')

@admin.register(Carousel)
class CarouselAdmin(ImportExportModelAdmin):
    resource_class = CarouselResource
    list_display = ('title', 'display_image', 'url', 'order', 'is_active', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('title',)
    ordering = ('order', '-created_at')
    list_editable = ('order', 'is_active')  # 允许直接在列表中编辑
    
    readonly_fields = ('display_large_image',)
    
    fieldsets = (
        ('基本信息', {
            'fields': ('title', 'image', 'display_large_image', 'url')
        }),
        ('显示设置', {
            'fields': ('order', 'is_active')
        }),
    )

    def display_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100" height="50" style="object-fit: cover; border-radius: 5px;" />', obj.image.url)
        return "无图片"
    display_image.short_description = '预览图'

    def display_large_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="400" style="border-radius: 10px; box-shadow: 0 4px 8px rgba(0,0,0,0.1);" />', obj.image.url)
        return "无图片"
    display_large_image.short_description = '大图预览'
    
    # 列表页面的批量操作
    actions = ['activate_items', 'deactivate_items']
    
    def activate_items(self, request, queryset):
        queryset.update(is_active=True)
    activate_items.short_description = "启用所选轮播图"
    
    def deactivate_items(self, request, queryset):
        queryset.update(is_active=False)
    deactivate_items.short_description = "停用所选轮播图"

    class Media:
        css = {
            'all': ('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css',)
        }
