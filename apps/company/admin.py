from django.contrib import admin
from .models import Company, Address, Establishment, Product


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
	list_display = (
		'id',
		'legal_name',
		'trade_name',
		'tax_regime',
		'is_active'
	)
	search_fields = (
		'legal_name',
		'trade_name'
	)


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
	list_display = (
		'id',
		'street',
		'city_name',
		'state',
		'postal_code'
	)
	search_fields = (
		'street',
		'city_name',
		'postal_code'
	)


@admin.register(Establishment)
class EstablishmentAdmin(admin.ModelAdmin):
	list_display = (
		'id',
		'cnpj',
		'company',
		'is_matrix',
		'environment_default',
		'is_active'
	)
	search_fields = (
		'cnpj',
		'company__legal_name'
	)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
	list_display = (
		'id',
		'name',
		'sku',
		'company',
		'sale_price',
		'is_active'
	)
	search_fields = (
		'name',
		'sku'
	)
