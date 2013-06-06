from django.contrib import admin
from accounts.models import PostalAddress


# -----------------------------------------------------------------------------
class PostalAddressAdmin(admin.ModelAdmin):
    list_display = ('country', 'state', 'zip_code', 'city', 'address')
    search_fields = ('country', 'state', 'zip_code', 'city', 'address')
    list_filter = ('country',)

admin.site.register(PostalAddress, PostalAddressAdmin)
