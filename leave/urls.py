from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^$', views.login_init, name='home'),
    url(r'^login/$', views.login_init, name='login_init'),
    url(r'^login/auth/$', views.login_auth, name='login'),
    url(r'^logout/$', views.logout_auth, name='logout'),
    url(r'^mark_attendance/$', views.mark_attendance_init, name='mark_attendance_init'),
    url(r'^send_attendance/$', views.mark_attendance, name='mark_attendance'),
    url(r'^change_password/$', views.change_password_init, name='change_password'),
    url(r'^change_password_confirm/$', views.change_password, name='change_password_confirm'),
]