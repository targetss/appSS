from django.contrib import admin
from .models import *

class ApplicationObjectAdmin(admin.ModelAdmin):
    list_display = ["id", "number_object", "name_object", "address_object", "type_of_problem", "initiator_of_the_application"]
    #list_filter = ["number_object"]
    search_fields = ["number_object", "address_object", "initiator_of_the_application"]
    readonly_fields = ('date_application',)

    class Meta:
        model = ApplicationObject

class TechnicianAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]

    class Meta:
        model = Technician

admin.site.register(ApplicationObject, ApplicationObjectAdmin)
admin.site.register(Technician, TechnicianAdmin)
