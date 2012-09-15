from django.conf.urls import patterns, include, url

import djangowars.views

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^$', djangowars.views.index),
                       url(r'^registrar/$', djangowars.views.registrar), # pagina de cadastro
                       url(r'^login/$', djangowars.views.logar), # pagina de login
                       url(r'^crimes/$', djangowars.views.crimes), # pagina de login
                       
                       # Uncomment the next line to enable the admin:
                       url(r'^admin/', include(admin.site.urls)),
                       
                       # Uncomment the admin/doc line below to enable admin documentation:
                       # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
)