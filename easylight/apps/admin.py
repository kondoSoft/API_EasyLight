from django.contrib import admin
from .models import State, History, Profile, Municipality, TipsAndAdvertising, Receipt, Contract, Rate, Records, RateHighConsumption, LimitRateDac, TableRegion
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
    list_display = ['get_state', 'get_mun', 'get_region']
    list_filter = ['state']
    search_fields = ['state__state', 'name_mun']
    list_per_page = 25

    def get_mun(self, obj):
        return obj.name_mun
    get_mun.short_description = ("Municipio")

    def get_state(self, obj):
        return obj.state
    get_state.short_description = ("Estado")

    def get_region(self, obj):
        return obj.region
    get_region.short_description = ("Region")

class ReceiptAdmin(admin.ModelAdmin):
    list_display = ['get_payday','get_amount', 'get_period', 'get_update', 'get_contract',]
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

    def get_contract(self, obj):
        return obj.contract
    get_contract.short_description = ("Contrato")

class RateResource(resources.ModelResource):
    class Meta:
        model = Rate

class RateImportExport(ImportExportModelAdmin):
    resource_class = RateResource
    list_display = ('get_name_rate', 'period_name', 'consumption_name', 'kilowatt', 'cost')

    def get_name_rate(self, obj):
        return obj.name_rate
    get_name_rate.short_description = ("Tarifa")

class RecordsAdmin(admin.ModelAdmin):
    list_display = ['get_date', 'get_daily_reading','get_projection', 'get_projected_payment', 'get_amount_payable', 'get_contracts', 'get_status']
    list_per_page = 25

    def get_date(self, obj):
        return obj.date
    get_date.short_description = ("Fecha")

    def get_daily_reading(self, obj):
        return obj.daily_reading
    get_daily_reading.short_description = ("Lectura del Día")

    def get_contracts(self, obj):
        return obj.contracts
    get_contracts.short_description = ("Contrato")

    def get_projection(self, obj):
        return obj.projection
    get_projection.short_description = ("Proyección")

    def get_projected_payment(self, obj):
        return obj.projected_payment
    get_projected_payment.short_description = ("Pago Proyectado")

    def get_amount_payable(self, obj):
        return obj.amount_payable
    get_amount_payable.short_description = ("Cantidad Pagada")

    def get_status(self, obj):
        return obj.status
    get_status.short_description = ("Estado")
    
class HistoryAdmin(admin.ModelAdmin):
    list_display = ['get_period', 'get_kilowatt', 'get_cost', ]
    list_per_page = 25

    def get_period(self, obj):
        return obj.period_name
    get_period.short_description = ("Periodo")

    def get_kilowatt(self, obj):
        return obj.kilowatt
    get_kilowatt.short_description = ("Consumo kwh")

    def get_cost(self, obj):
        return obj.cost
    get_cost.short_description = ("Costo")


class TableRegionResource(resources.ModelResource):
    class Meta:
        model = TableRegion
        # exclude = ('id',)

class TableRegionAdmin(ImportExportModelAdmin):
    resource_class = TableRegionResource


class RateHighConsumptionResource(resources.ModelResource):
    class Meta:
        model = RateHighConsumption

class RateHighConsumptionAdmin(ImportExportModelAdmin):
    list_display = [ 'get_month', 'region', 'get_fixed_charge','get_cost_verano', 'get_cost_no_verano', 'get_unique_rate']
    resource_class = RateHighConsumptionResource

    def get_month(self, obj):
        return obj.month
    get_month.short_description = ("Mes")

    def get_fixed_charge(self, obj):
        return obj.fixed_charge
    get_fixed_charge.short_description = ("Cargo Fijo")

    def get_cost_verano(self, obj):
        return obj.cost_verano
    get_cost_verano.short_description = ("Costo en Verano")

    def get_cost_no_verano(self, obj):
        return obj.cost_no_verano
    get_cost_no_verano.short_description = ("Costo Fuera de Verano")

    def get_unique_rate(self, obj):
        return obj.unique_rate
    get_unique_rate.short_description = ("Tarifa Unica")


class LimitRateDacResource(resources.ModelResource):
    class Meta:
        model = LimitRateDac

class LimitRateDacAdmin(ImportExportModelAdmin):
    list_display=['get_name_rate', 'get_kilowatt']
    resource_class = LimitRateDacResource

    def get_name_rate(self, obj):
        return obj.name_rate
    get_name_rate.short_description = ("Tarifa")

    def get_kilowatt(self,obj):
        return obj.kilowatt
    get_kilowatt.short_description = ("Limite KwH/mes")

admin.site.register(State, StateAdmin)
admin.site.register(Municipality, MunicipalityAdmin)
admin.site.register(Rate, RateImportExport)
admin.site.register(Profile)
admin.site.register(Contract)
admin.site.register(Records, RecordsAdmin)
admin.site.register(Receipt, ReceiptAdmin)
admin.site.register(History, HistoryAdmin)
admin.site.register(TipsAndAdvertising)
admin.site.register(RateHighConsumption, RateHighConsumptionAdmin)
admin.site.register(LimitRateDac, LimitRateDacAdmin)
admin.site.register(TableRegion, TableRegionAdmin)