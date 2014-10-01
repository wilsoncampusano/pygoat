from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^$', 'lists.views.home_page', name='home'),
    url(r'^(\d+)/$', 'lists.views.view_list', name='view_list'),
    url(r'^new$', 'lists.views.new_list', name='new_list'),
    url(r'^(\d+)/add_item$', 'lists.views.add_item', name='new_list')
)
