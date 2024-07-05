from django.contrib import admin
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import UserCreationForm
from .models import *
# from med_app.models import *
# Register your models here.
class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'first_name', 'is_admin',"is_active")
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name','last_name')}),
        ('Permissions', {'fields': ('is_admin',"is_active",)}),
        ('Profile Type',{'fields':('is_manager','is_member')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'password1', 'password2'),
        }),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()


# Now register the new UserAdmin...
admin.site.register(User, UserAdmin)
# admin.site.register(Summary)
admin.site.unregister(Group)

@admin.register(OTPModel)
class OTPAdmin(admin.ModelAdmin):
    list_display= ['user','otp']


@admin.register(DealerProfileModel)
class DealerProfileAdmin(admin.ModelAdmin):
    list_display= ['user']
    # ,'company_name'

@admin.register(ClientProfileModel)
class CostomerAdmin(admin.ModelAdmin):
    list_display= ['user','gender','address','profile_picture']

@admin.register(JobTypeModel)
class JobTypeAdmin(admin.ModelAdmin):
    list_display= ['job_type_title','job_type_desc']

@admin.register(JobCategoryModel)
class JobCategoryAdmin(admin.ModelAdmin):
    list_display= ['category_title','category_desc']
    