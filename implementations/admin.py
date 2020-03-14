from django.contrib import admin
from .models import Algorithm, QuantumComputer, QubitType, QubitSubtype, NISQImplementation

# Register your models here.
admin.site.register(Algorithm)
admin.site.register(QuantumComputer)
admin.site.register(QubitType)
admin.site.register(QubitSubtype)
admin.site.register(NISQImplementation)
