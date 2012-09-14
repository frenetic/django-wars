# importamos o modulo de admin
from django.contrib import admin

# importamos os modelos desta app que desejamos que o django-admin administre
from djangowars.itens.models import Arma, Armadura


#cadastramos o modelo das armas no django-admin
admin.site.register(Arma)

#cadastramos o modelo das armaduras no django-admin
admin.site.register(Armadura)