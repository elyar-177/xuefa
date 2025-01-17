from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import VIPPackage, VIPSubscription

class VIPPackageResource(resources.ModelResource):
    class Meta:
        model = VIPPackage
        fields = ('id', 'name', 'price', 'duration', 'description', 'features', 'is_active')

@admin.register(VIPPackage)
class VIPPackageAdmin(ImportExportModelAdmin):
    resource_class = VIPPackageResource
    list_display = ('name', 'price', 'duration', 'is_active', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('name',)
    ordering = ('price',)
    
    # 列表页面的批量操作
    actions = ['activate_packages', 'deactivate_packages']
    
    def activate_packages(self, request, queryset):
        queryset.update(is_active=True)
    activate_packages.short_description = "启用所选套餐"
    
    def deactivate_packages(self, request, queryset):
        queryset.update(is_active=False)
    deactivate_packages.short_description = "停用所选套餐"

class VIPSubscriptionResource(resources.ModelResource):
    class Meta:
        model = VIPSubscription
        fields = ('id', 'user', 'package', 'start_date', 'end_date', 'is_active', 'payment_id')

@admin.register(VIPSubscription)
class VIPSubscriptionAdmin(ImportExportModelAdmin):
    resource_class = VIPSubscriptionResource
    list_display = ('user', 'package', 'start_date', 'end_date', 'is_active', 'created_at')
    list_filter = ('is_active', 'package', 'start_date', 'end_date')
    search_fields = ('user__username', 'user__nickname', 'payment_id')
    ordering = ('-created_at',)
    date_hierarchy = 'start_date'  # 添加日期层级导航
    
    def get_readonly_fields(self, request, obj=None):
        if obj:  # 编辑时
            return ('payment_id', 'user', 'package', 'start_date')
        return ()
