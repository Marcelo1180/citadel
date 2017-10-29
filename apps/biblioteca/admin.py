from django.contrib import admin
from apps.biblioteca.models import Biblioteca, Libro

# Register your models here.
admin.site.register(Biblioteca)
admin.site.register(Libro)
