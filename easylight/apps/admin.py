from django.contrib import admin
from .models import State, Municipality, TipsAndAdvertising, Receipt, Contract, Rate
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

class RateResource(resources.ModelResource):
    class Meta:
        model = Rate

class RateImportExport(ImportExportModelAdmin):
    resource_class = RateResource
    list_display = ('name_rate', 'period_name', 'consumption_name', 'kilowatt', 'cost')


admin.site.register(State, StateAdmin)
admin.site.register(Municipality, MunicipalityAdmin)
admin.site.register(Rate, RateImportExport)
# admin.site.register(Profile)
admin.site.register(Contract)
admin.site.register(Receipt)
admin.site.register(TipsAndAdvertising)
