from django.contrib import admin
from .models import Organization, User, Membership


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
	list_display = (
		'id',
		'name',
		'slug',
		'created_at'
	)
	search_fields = (
		'name',
		'slug'
	)


@admin.register(User)
class CustomUserAdmin(admin.ModelAdmin):
	list_display = (
		'id',
		'email',
		'username',
		'is_staff',
		'is_active'
	)
	search_fields = (
		'email',
		'username'
	)
	list_filter = (
		'is_staff',
		'is_active'
	)


@admin.register(Membership)
class MembershipAdmin(admin.ModelAdmin):
	list_display = (
		'id',
		'user',
		'organization',
		'role',
		'is_active'
	)
	search_fields = (
		'user__email',
		'organization__slug'
	)
