from django.urls import path
from . import views as my_views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', my_views.base_info, name='base_info'),
    path('profile/', my_views.profile, name='profile'),
    path('edit_profile/', my_views.edit_profile, name='edit_profile'),
    path('register/', my_views.register, name='register'),
    path('favourite/', my_views.favourite, name='favourite'),
    path('login/', auth_views.LoginView.as_view(template_name='virus_app/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='virus_app/logout.html'), name='logout'),
    path('more_virus_info/<int:pk>/', my_views.more_virus_info, name = 'more_virus_info'),
    path('more_virus_info/<int:pk>/edit_virus_info/', my_views.edit_virus_info, name='edit_virus_info'),
    path('scroll_epidemic/<int:epidemiology_pk>/', my_views.scroll_epidemic, name = 'scroll_epidemic'),
    path('scroll_epidemic/<int:epidemiology_pk>/more_epidemic_info/<int:epidemic_pk>/', my_views.more_epidemic_info, name = 'more_epidemic_info'),
    path('scroll_epidemic/<int:epidemiology_pk>/more_epidemic_info/<int:epidemic_pk>/edit_epidemic_info/', my_views.edit_epidemic_info, name='edit_epidemic_info'),
    path('scroll_epidemic/<int:epidemiology_pk>/scroll_region/<int:epidemic_pk>/', my_views.scroll_region, name = 'scroll_region'),
    path('scroll_epidemic/<int:epidemiology_pk>/scroll_region/<int:epidemic_pk>/scroll_country/<str:region_name>/', my_views.scroll_country, name = 'scroll_country'),
    path('scroll_epidemic/<int:epidemiology_pk>/scroll_region/<int:epidemic_pk>/scroll_country/<str:region_name>/scroll_town/<str:country_name>/', my_views.scroll_town, name = 'scroll_town'),
]

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)