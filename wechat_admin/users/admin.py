from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import User

class UserResource(resources.ModelResource):
    class Meta:
        model = User
        exclude = ('password',)
        export_order = ('id', 'username', 'nickname', 'phone', 'email', 'is_vip', 'gender', 'register_date')

@admin.register(User)
class CustomUserAdmin(UserAdmin, ImportExportModelAdmin):
    resource_class = UserResource
    list_display = ('username', 'nickname', 'phone', 'email', 'is_vip', 'is_staff', 'is_active')
    list_filter = ('is_vip', 'is_staff', 'is_active', 'gender')
    search_fields = ('username', 'nickname', 'phone', 'email')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('个人信息', {'fields': ('nickname', 'email', 'phone', 'avatar', 'gender')}),
        ('微信信息', {'fields': ('openid',)}),
        ('权限', {'fields': ('is_active', 'is_staff', 'is_superuser', 'is_vip', 'groups', 'user_permissions')}),
    )
    
    # 列表页面的批量操作
    actions = ['make_vip', 'cancel_vip']
    
    def make_vip(self, request, queryset):
        queryset.update(is_vip=True)
    make_vip.short_description = "设为VIP用户"
    
    def cancel_vip(self, request, queryset):
        queryset.update(is_vip=False)
    cancel_vip.short_description = "取消VIP资格"
