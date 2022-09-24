"""
Django admin customization.
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext as _

from core import models


class UserAdmin(BaseUserAdmin):
    ordering = ['id']
    list_display = ['id', 'email', 'username', 'is_staff', 'last_login']

    fieldsets = (
        (
            None,  # Here title is 'None'
            {
                "fields": ('email', 'password')
            }
        ),
        (
            _('Personal Info'),
            {
                "fields": ('username',)
            }
        ),
        (
            _('Permissions'),
            {
                "fields": ('is_active', 'is_staff', 'is_superuser')
            }
        ),
        (
            _('Important dates'),
            {
                "fields": ('last_login', 'date_joined')
            }
        )
    )

    # Don't know the reason for the type error here
    # readonly_fields: ['last_login']

    # To modify Create/Add new user page in django admin
    add_fieldsets = (
        (None, {
            # 'classes' To add custom css classes.
            # ('wide') class to make the field wide
            # in new user django admin page.
            'classes': ('wide',),
            'fields': (
                'email',
                'password1',
                'password2',
                'username',
                'is_active',
                'is_staff',
                'is_superuser',
            )
        }),
    )


class TeamAdmin(admin.ModelAdmin):
    ordering = ['-created_on']
    list_display = ['id', 'name', 'owner']

    # To make use of Custom TeamManager method to create new instance
    # djangoadmin.
    def save_form(self, request, form, change):
        if not change:
            form.instance = self.model.objects.create_team(
                form.cleaned_data['name'],
                form.cleaned_data['description'],
                form.cleaned_data['owner'].id,
            )
            return super().save_form(request, form, change)


class TeamMembershipAdmin(admin.ModelAdmin):
    ordering = ['-joined_on']


class TopicAdmin(admin.ModelAdmin):
    ordering = ['-created_on']
    list_display = ['id', 'title', 'creator', 'team']


class CommentAdmin(admin.ModelAdmin):
    ordering = ['-created_on']
    list_display = ['id', 'body', 'commented_by', 'topic']


admin.site.register(models.User, UserAdmin)
admin.site.register(models.Team, TeamAdmin)
admin.site.register(models.TeamMembership, TeamMembershipAdmin)
admin.site.register(models.Role)
admin.site.register(models.Topic, TopicAdmin)
admin.site.register(models.Comment, CommentAdmin)


