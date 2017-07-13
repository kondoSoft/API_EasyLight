from django.contrib import admin
from .models import State, Municipality, TipsAndAdvertising, TableRate, Receipt, Contract
from import_export.admin import ImportExportModelAdmin
from import_export import resources
# Register your models here.


class StateResource(resources.ModelResource):
    class Meta:
        model = State
        exclude = ('id',)
        import_id_fields = ('key_state',)

class StateAdmin(ImportExportModelAdmin):
    resource_class = StateResource

class MunicipalityResource(resources.ModelResource):
    class Meta:
        model = Municipality
        exclude = ('id',)
        import_id_fields = ('key_mun',)

class MunicipalityAdmin(ImportExportModelAdmin):
    resource_class = MunicipalityResource

admin.site.register(State, StateAdmin)
admin.site.register(Municipality, MunicipalityAdmin)
admin.site.register(TableRate)
admin.site.register(Contract)
admin.site.register(Receipt)
admin.site.register(TipsAndAdvertising)
