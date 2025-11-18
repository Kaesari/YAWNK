from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import SiteConfiguration
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'email', 'is_seller', 'location']
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('is_seller', 'bio', 'location', 'profile_picture')}),
    )


from django.contrib import admin
from .models import SiteConfiguration

@admin.register(SiteConfiguration)
class SiteConfigurationAdmin(admin.ModelAdmin):
    # Define the columns to be displayed in the admin list view
    list_display = ('site_name', 'logo', 'favicon')  # Add more fields as needed
    
    # Prevent adding more than one configuration
    def has_add_permission(self, request):
        return not SiteConfiguration.objects.exists()

    # Prevent deletion of the SiteConfiguration object
    def has_delete_permission(self, request, obj=None):
        return False

    # Optionally, make the fields editable inline if needed
    # fieldsets = (
    #     (None, {
    #         'fields': ('site_name', 'logo')  # Add more fields you want to allow editing
    #     }),
    # )

    # Make the `site_name` and `logo` fields editable in the list view
    search_fields = ['site_name']



admin.site.register(CustomUser, CustomUserAdmin)




