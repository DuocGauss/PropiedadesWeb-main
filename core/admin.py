from django.contrib import admin
from .models import EmpresaCorredora, Agente, Cliente


# Register your models here.
admin.site.register(EmpresaCorredora)
admin.site.register(Agente)
admin.site.register(Cliente)