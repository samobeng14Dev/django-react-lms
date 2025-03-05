from django.contrib import admin
from userauths.models import User, Profile

class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'full_name', 'country', 'date']
    search_fields = ['user', 'full_name', 'country', 'date']
    list_filter = ['date']

# Register your models here.
admin.site.register(User)
admin.site.register(Profile)

