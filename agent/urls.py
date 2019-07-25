from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings
from . import views
from django.contrib.auth import views as auth_views

urlpatterns=[
    url('^$', views.home, name = 'home'),
    # url(r'^daraja/stk-push$', views.index, name='mpesa_stk_push_callback'),
    url(r'^add_user/([A-Za-z0-9\s]+)/$', views.create_user, name='add_user'),
    url(r'^user_profile/(\d)/$', views.user_profile, name='user_profile'),
    url(r'^edit_user/(\d)/$', views.edit_user, name='edit_user'),
    url(r'^create_building/$', views.create_building, name='create_building'),
    url(r'^create_house/$', views.create_house, name='create_house'),
    url(r'^view_houses/([A-Za-z0-9\s]+)/$', views.view_houses, name='view_houses'),
    url(r'^view_tenant/([A-Za-z0-9\s]+)/$', views.view_tenant, name='view_tenant'),
    url(r'^pay_with_mpesa$', views.pay_with_mpesa, name='pay-with-mpesa'),
    url(r"^magent_callback",views.stk_push_callback,name='mpesa_stk_push_callback')
   

    ]
if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)