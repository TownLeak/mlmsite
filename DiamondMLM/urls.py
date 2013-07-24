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
    url(r'^password_reset/$', 'password_reset'),
    url(r'^registration/$', 'registration'),
    url(r'^login/$', 'login'),
    url(r'^logout/$', 'logout'),
    url(r'^bad_login/$', 'bad_login'),
    url(r'^graph_eval/$', 'graph_eval'),
    url(r'^graph_eval/more_users/$', 'graph_eval_more_users'),
    url(r'^graph_eval/thousand_users/$', 'graph_eval_thousand_users'),
    url(r'^graph_eval/gyalu/$', 'graph_eval_gyalu'),
    url(r'^graph_eval/binary_matrix/$', 'graph_eval_binary_matrix'),
    url(r'^graph_eval/unilevel_matrix/$', 'graph_eval_unilevel_matrix'),
    url(r'^graph_eval/leave/(\d)$', 'graph_eval_leave'),
    url(r'^graph_eval/next_month/$', 'graph_eval_next_month'),
    url(r'^bootstrap/$', 'bootstrap'),
    url(r'^try_paypal/$', 'try_paypal'),
    url(r'^try_paypal_success/$', 'try_paypal_success'),
    url(r'^try_paypal_cancel/$', 'try_paypal_cancel'),
)

urlpatterns += patterns('paypal.standard.ipn.views',
    (r'^atyalapatyala/', 'ipn'),
)
