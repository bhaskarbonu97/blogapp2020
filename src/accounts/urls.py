from django.conf.urls import url
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

from django.conf.urls.static import static
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


urlpatterns = [
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^Profile/$',views.profile_edit, name='Profile_edit'),
    url(r'^profile_list/$',views.ProfileListView.as_view(), name='profile_list'),
    path('profile/<int:pk>', views.getprofile ,name='profile'),
    path('profile/follow/<int:pk>', views.follow, name='follow'),
    path('profile/unfollow/<int:pk>', views.unfollow, name='unfollow'),

    url(r'login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    url(r'logout/', auth_views.LogoutView.as_view(template_name='registration/logout.html'), name='logout',
     kwargs={'next_page': '/'}),

    url(r'password-reset/', auth_views.PasswordResetView.as_view(template_name='registration/password_reset_form.html'), name='password_reset'),
    url(r'password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), name='password_reset_done'),
    path('password_reset/confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'),
        name='password_reset_confirm'),
    url(r'reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), name='password_reset_complete'),

    path('password-change/', auth_views.PasswordChangeView.as_view(template_name='registration/password_change.html'), name='password_change'),
    path('password-change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='registration/password_change_done.html'), name='password_change_done'),

]
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
