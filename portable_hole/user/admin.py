from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . import models
from pocket_dimension.models import PortableHole


class OwnerOf(admin.TabularInline):
    model = PortableHole
    verbose_name = 'Owns'
    verbose_name_plural = 'Owns'
    fields = ('name', 'system',)
    readonly_fields = ('name', 'system',)

    def has_add_permission(self, request, obj):
        return False


class MemberOf(admin.TabularInline):
    model = PortableHole.party_members.through
    verbose_name = 'Member Of'
    verbose_name_plural = 'Member Of'

    def has_add_permission(self, request, obj):
        return False

    def has_delete_permission(self, request, obj=None):
        return True


class CustomUserAdmin(UserAdmin):
    model = models.PHUser
    fieldsets = (
        *UserAdmin.fieldsets,
    )
    inlines = [OwnerOf, MemberOf]
    list_display = ('username', 'email', 'first_name', 'last_name', 'owns', 'joined',)

    def owns(self, obj):
        if obj.owner_of is not None:
            return ', '.join([ph.name for ph in obj.owner_of.all()])
    owns.short_description = 'Owner Of'

    def joined(self, obj):
        if obj.owner_of is not None:
            return ', '.join([ph.name for ph in obj.member_of.all()])
    joined.short_description = 'Member Of'


admin.site.register(models.PHUser, CustomUserAdmin)
