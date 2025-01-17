from django.contrib import admin
from django.utils.html import format_html
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import DailyStats

class DailyStatsResource(resources.ModelResource):
    class Meta:
        model = DailyStats
        fields = ('date', 'new_users', 'active_users', 'new_vip_users', 'total_revenue')

@admin.register(DailyStats)
class DailyStatsAdmin(ImportExportModelAdmin):
    resource_class = DailyStatsResource
    list_display = ('date', 'new_users', 'active_users', 'new_vip_users', 'display_revenue', 'trend_indicator')
    list_filter = ('date',)
    ordering = ('-date',)
    date_hierarchy = 'date'
    
    def has_add_permission(self, request):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False
        
    def display_revenue(self, obj):
        return format_html('<span style="color: #28a745;">¥ {:,.2f}</span>', obj.total_revenue)
    display_revenue.short_description = '总收入'
    
    def trend_indicator(self, obj):
        try:
            previous_day = DailyStats.objects.filter(date__lt=obj.date).order_by('-date').first()
            if previous_day:
                if obj.active_users > previous_day.active_users:
                    return format_html('<span style="color: #28a745;"><i class="fas fa-arrow-up"></i> 上升</span>')
                elif obj.active_users < previous_day.active_users:
                    return format_html('<span style="color: #dc3545;"><i class="fas fa-arrow-down"></i> 下降</span>')
                return format_html('<span style="color: #6c757d;"><i class="fas fa-minus"></i> 持平</span>')
        except:
            pass
        return '-'
    trend_indicator.short_description = '活跃度趋势'

    class Media:
        css = {
            'all': (
                'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css',
            )
        }
