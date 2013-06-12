from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^i18n/', include('django.conf.urls.i18n')),
)

urlpatterns += patterns('accounts.views',
    url(r'^accounts/signup/$', 'signup'),
    url(r'^accounts/', include('userena.urls')),
    url(r'^postaladdress/$', 'postaladdress'),
)

urlpatterns += patterns('mlmsite.views',
    url(r'^$', 'index'),
    url(r'^graph_eval/$', 'graph_eval'),
    url(r'^graph_eval/more_users/$', 'graph_eval_more_users'),
    url(r'^graph_eval/gyalu/$', 'graph_eval_gyalu'),
    url(r'^graph_eval/leave/(\d)$', 'graph_eval_leave'),
    url(r'^bootstrap/$', 'bootstrap'),
)
