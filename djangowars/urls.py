from django.conf.urls import patterns, include, url

import djangowars.views

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^$', djangowars.views.index),
                       url(r'^registrar/$', djangowars.views.registrar), # pagina de cadastro
                       url(r'^login/$', djangowars.views.logar), # pagina de login

                       url(r'^crimes/$', djangowars.views.crimes),
                       url(r'^crimes/cometer/1/$', djangowars.views.cometer_crime1),
                       url(r'^crimes/cometer/2/$', djangowars.views.cometer_crime2),

                       url(r'^loja/$', djangowars.views.loja), # pagina de loja
                       url(r'^loja/comprar/armadura/(\d+)/$', djangowars.views.comprar_armadura), # pagina de loja
                       url(r'^loja/vender/armadura/(\d+)/$', djangowars.views.vender_armadura), # pagina de loja
                       url(r'^loja/comprar/arma/(\d+)/$', djangowars.views.comprar_arma), # pagina de loja
                       url(r'^loja/vender/arma/(\d+)/$', djangowars.views.vender_arma), # pagina de loja
                       
                       # Uncomment the next line to enable the admin:
                       url(r'^admin/', include(admin.site.urls)),
                       
                       # Uncomment the admin/doc line below to enable admin documentation:
                       # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
)