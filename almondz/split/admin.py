from django.contrib import admin
from .models import User, Split

class UserAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'name', 'email', 'mobile')
    search_fields = ('user_id', 'name', 'email', 'mobile')

class SplitAdmin(admin.ModelAdmin):
    list_display = ('paid_by', 'amount', 'split_type')
    list_filter = ('split_type',)
    search_fields = ('paid_by__name', 'amount')

admin.site.register(User, UserAdmin)
admin.site.register(Split, SplitAdmin)
