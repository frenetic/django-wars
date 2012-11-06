from django.conf.urls import patterns, include, url

import djangowars.views

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^$', djangowars.views.site.index),
                       
                       url(r'^registrar/$', djangowars.views.player.registrar), # pagina de cadastro
                       url(r'^login/$', djangowars.views.player.logar), # pagina de login
                       
                       url(r'^crimes/$', djangowars.views.crimes.crimes),
                       url(r'^crimes/cometer/1/$', djangowars.views.crimes.cometer_crime1),
                       url(r'^crimes/cometer/2/$', djangowars.views.crimes.cometer_crime2),
                       
                       url(r'^loja/$', djangowars.views.loja.loja), # pagina de loja
                       url(r'^loja/comprar/armadura/(\d+)/$', djangowars.views.loja.comprar_armadura), # pagina de loja
                       url(r'^loja/vender/armadura/(\d+)/$', djangowars.views.loja.vender_armadura), # pagina de loja
                       url(r'^loja/comprar/arma/(\d+)/$', djangowars.views.loja.comprar_arma), # pagina de loja
                       url(r'^loja/vender/arma/(\d+)/$', djangowars.views.loja.vender_arma), # pagina de loja
                       
                       url(r'^inventario/$', djangowars.views.inventario.inventario),
                       url(r'^inventario/equipar/armadura/(\d+)/$', djangowars.views.inventario.equipar_armadura),
                       url(r'^inventario/equipar/arma/(\d+)/$', djangowars.views.inventario.equipar_arma),
                       
                       
                       # Uncomment the next line to enable the admin:
                       url(r'^admin/', include(admin.site.urls)),
                       
                       # Uncomment the admin/doc line below to enable admin documentation:
                       # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
)