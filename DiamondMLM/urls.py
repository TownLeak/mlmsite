from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings

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

dev_graph_eval_patterns = patterns('mlmsite.dev.graph_eval.views',
    url(r'^$', 'graph_eval'),
    url(r'^more_users/$', 'graph_eval_more_users'),
    url(r'^thousand_users/$', 'graph_eval_thousand_users'),
    url(r'^gyalu/$', 'graph_eval_gyalu'),
    url(r'^binary_matrix/$', 'graph_eval_binary_matrix'),
    url(r'^unilevel_matrix/$', 'graph_eval_unilevel_matrix'),
    url(r'^leave/(\d)$', 'graph_eval_leave'),
    url(r'^next_month/$', 'graph_eval_next_month'),
)

dev_patterns = patterns('mlmsite.dev.views',
    url(r'^graph_eval/', include(dev_graph_eval_patterns)),
    url(r'^bootstrap/$', 'bootstrap'),
    url(r'^try_paypal/$', 'try_paypal'),
    url(r'^try_paypal_success/$', 'try_paypal_success'),
    url(r'^try_paypal_cancel/$', 'try_paypal_cancel'),
)

urlpatterns += patterns('mlmsite.views',
    url(r'^dev/', include(dev_patterns)),
    url(r'^$', 'index'),
    url(r'^bad_login/$', 'bad_login'),
    url(r'^password_reset/$', 'password_reset'),
    url(r'^registration/$', 'registration'),
    url(r'^login/$', 'login'),
    url(r'^logout/$', 'logout')
)

if settings.DEVELOPMENT_MODE:
    urlpatterns += patterns('',
        url(r'^dev/', include(dev_patterns))
    )

urlpatterns += patterns('paypal.standard.ipn.views',
    (r'^atyalapatyala/', 'ipn'),
)
