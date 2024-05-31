from django.contrib import admin
from .models import EmpresaCorredora, Agente, Cliente, Tipo_Cliente, Propiedad


# Register your models here.
admin.site.register(EmpresaCorredora)
admin.site.register(Agente)
admin.site.register(Cliente)
admin.site.register(Tipo_Cliente)
admin.site.register(Propiedad)