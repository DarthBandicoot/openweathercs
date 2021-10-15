from django.contrib import admin

from todo.models import Locations, Tasks


class LocationAdmin(admin.ModelAdmin):
    pass


class TaskAdmin(admin.ModelAdmin):
    pass


admin.site.register(Locations, LocationAdmin)
admin.site.register(Tasks, TaskAdmin)
