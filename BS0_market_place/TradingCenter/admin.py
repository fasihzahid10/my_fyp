from django.contrib import admin
from TradingCenter import models
from django.contrib.admin.options import ModelAdmin
# Register your models here.

admin.site.site_header = "Welcome to TradingCenter Admin Panel"
admin.site.site_title = "TradingCenter"
admin.site.index_title = "TradingCenter"

class FinantialAccount(ModelAdmin):
    list_display = ["balance", "commited_balance"]
    search_fields = ["balance", "commited_balance"]
    list_filter = ["balance", "commited_balance"]
admin.site.register(models.finantial_account, FinantialAccount)

class Customer(ModelAdmin):
    list_display = ["user", "customers_account"]
    search_fields = ["user", "customers_account"]
    list_filter = ["user", "customers_account"]
admin.site.register(models.customer, Customer)

class Message(ModelAdmin):
    list_display = ["sender", "reciver"]
    search_fields = ["sender", "reciver"]
    list_filter = ["sender", "reciver"]
admin.site.register(models.message, Message)

class Sector(ModelAdmin):
    list_display = ["name", "location"]
    search_fields = ["profit_on_brand", "description","name", "location","type_of_manager_allowed"]
    list_filter = ["profit_on_brand","name", "location","type_of_manager_allowed"]
admin.site.register(models.sector, Sector)

class Brand(ModelAdmin):
    list_display = ["name", "owner"]
    search_fields = ["name", "owner","brand_sector","location","description"]
    list_filter = ["name", "owner","brand_sector","location"]
admin.site.register(models.brand, Brand)

class InventoryManager(ModelAdmin):
    list_display = ["name", "brands_product"]
    search_fields = ["name", "brands_product","amount","description","selling_price","total_rating","seconds_spends_on_product"]
    list_filter = ["name", "brands_product","amount","selling_price","total_rating","seconds_spends_on_product"]
admin.site.register(models.inventory_managment, InventoryManager)


class SoftwareManager(ModelAdmin):
    list_display = ["name", "brands_product"]
    search_fields = ["name", "brands_product","description","selling_price","total_rating","seconds_spends_on_product"]
    list_filter = ["name", "brands_product","selling_price","total_rating","seconds_spends_on_product"]
admin.site.register(models.software_manager, SoftwareManager)


class ServiceManager(ModelAdmin):
    list_display = ["name", "brands_product"]
    search_fields = ["name", "brands_product","package_price","total_rating","seconds_spends_on_product"]
    list_filter = ["name", "brands_product","package_price","total_rating","seconds_spends_on_product"]
admin.site.register(models.services_manager, ServiceManager)


class InventoryOrder(ModelAdmin):
    list_display = ["manager_id", "buyers_id","commited_amount","is_complete"]
    search_fields = ["manager_id", "buyers_id","commited_amount","is_complete","amount_buy"]
    list_filter = ["manager_id__brands_product__brand_sector__commit_allowed","is_commited_by_customer","is_commited_by_owner","is_commited_by_admin","is_active"]
    readonly_fields = ["check_out"]
admin.site.register(models.inventory_orders, InventoryOrder)


class SoftOrder(ModelAdmin):
    list_display = ["manager_id", "buyers_id","commited_amount","is_complete"]
    search_fields = ["manager_id", "buyers_id","commited_amount","is_complete","url"]
    list_filter = ["manager_id__brands_product__brand_sector__commit_allowed","is_commited_by_customer","is_commited_by_owner","is_commited_by_admin","is_active"]
    readonly_fields = ["check_out"]
admin.site.register(models.software_orders, SoftOrder)

class ProblemForm(ModelAdmin):
    list_display = ["problem_title","completion_date"]
    search_fields = ["problem_title","background","demands","completion_date"]
    list_filter = ["problem_title","background","demands","completion_date"]
admin.site.register(models.services_form, ProblemForm)

class RequestOnService(ModelAdmin):
    list_display = ["customer_id","service_id"]
    search_fields = ["form","customer_id","service_id","is_accepted"]
    list_filter = ["form","customer_id","service_id","is_accepted"]
admin.site.register(models.request_on_sevice, RequestOnService)


class ServiceOrder(ModelAdmin):

    list_display = ["request_id","commited_amount","is_complete"]
    search_fields = ["request_id","commited_amount","is_complete"]
    list_filter = ["request_id__service_id__brands_product__brand_sector__commit_allowed","is_commited_by_customer","is_commited_by_owner","is_commited_by_admin","is_active"]
    readonly_fields = ["check_out"]
admin.site.register(models.service_order, ServiceOrder)


class InventoryProductsComments(ModelAdmin):
    list_display = ["order","rating"]
    search_fields = ["order","rating","comment"]
    list_filter = ["order","rating","comment"]
admin.site.register(models.comment_on_inventory_order, InventoryProductsComments)


class SoftwareProductsComments(ModelAdmin):
    list_display = ["order","rating"]
    search_fields = ["order","rating","comment"]
    list_filter = ["order","rating","comment"]
admin.site.register(models.comment_on_software_order, SoftwareProductsComments)


class ServiceProductsComments(ModelAdmin):
    list_display = ["order","rating"]
    search_fields = ["order","rating","comment"]
    list_filter = ["order","rating","comment"]
admin.site.register(models.comment_on_service, ServiceProductsComments)

class Report_On_Item(ModelAdmin):
    list_display = ['order']
    search_fields = ["order","title","report","is_accepted"]
    list_filter = ["is_accepted"]
admin.site.register(models.report_on_inventory,Report_On_Item)



class Report_On_Software(ModelAdmin):
    list_display = ['order']
    search_fields = ["order","title","report","is_accepted"]
    list_filter = ["is_accepted"]
admin.site.register(models.report_on_software,Report_On_Software)



class Report_On_Service(ModelAdmin):
    list_display = ['order']
    search_fields = ["order","title","report","is_accepted"]
    list_filter = ["is_accepted"]
admin.site.register(models.report_on_service,Report_On_Service)
