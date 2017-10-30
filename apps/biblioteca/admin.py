from django.contrib import admin
from apps.biblioteca.models import Biblioteca, Libro
from django.contrib.auth.models import User, Group

admin.site.unregister(Group)
# Register your models here.
admin.site.register(Biblioteca)
admin.site.register(Libro)

class GroupAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False
admin.site.register(Group, GroupAdmin)
