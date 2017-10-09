from django.contrib import admin
from .models import State, Profile, Municipality, TipsAndAdvertising, Receipt, Contract, Rate, Records
from import_export.admin import ImportExportModelAdmin
from import_export import resources
from rest_framework.authtoken.admin import TokenAdmin
# Register your models here.

TokenAdmin.raw_id_fields = ('user',)

class StateResource(resources.ModelResource):
    class Meta:
        model = State
        # exclude = ('id',)

class StateAdmin(ImportExportModelAdmin):
    resource_class = StateResource

class MunicipalityResource(resources.ModelResource):
    class Meta:
        model = Municipality
        # exclude = ('id',)
        # import_id_fields = ('key_mun',)

class MunicipalityAdmin(ImportExportModelAdmin):
    resource_class = MunicipalityResource
    list_display = ['get_state', 'get_mun']
    list_filter = ['state']
    search_fields = ['state__state', 'name_mun']
    list_per_page = 25

    def get_mun(self, obj):
        return obj.name_mun
    get_mun.short_description = ("Municipio")

    def get_state(self, obj):
        return obj.state
    get_state.short_description = ("Estado")

class ReceiptAdmin(admin.ModelAdmin):
    list_display = ['get_payday','get_amount', 'get_period', 'get_update', ]
    list_per_page = 25

    def get_payday(self, obj):
        return obj.payday_limit
    get_payday.short_description = ("Fecha Limite del Recibo")

    def get_amount(self, obj):
        return obj.amount_payable
    get_amount.short_description = ("Monto a pagar")

    def get_period(self, obj):
        return obj.period
    get_period.short_description = ("Periodo")

    def get_update(self, obj):
        return obj.update_date
    get_update.short_description = ("Ultima Actualizacion")


class RateResource(resources.ModelResource):
    class Meta:
        model = Rate

class RateImportExport(ImportExportModelAdmin):
    resource_class = RateResource
    list_display = ('name_rate', 'period_name', 'consumption_name', 'kilowatt', 'cost')

class RecordsAdmin(admin.ModelAdmin):
    list_display = ('date',)
    pass


admin.site.register(State, StateAdmin)
admin.site.register(Municipality, MunicipalityAdmin)
admin.site.register(Rate, RateImportExport)
admin.site.register(Profile)
admin.site.register(Contract)
admin.site.register(Records, RecordsAdmin)
admin.site.register(Receipt, ReceiptAdmin)
admin.site.register(TipsAndAdvertising)
