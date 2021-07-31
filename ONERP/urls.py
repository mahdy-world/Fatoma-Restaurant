"""ONERP URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from Information import views

urlpatterns = [
    path('admincp/', admin.site.urls),
    path('', include('Website.urls')),
    path('admin/', include('Core.urls')),
    path('auth/', include('Auth.urls')),
    path('products/', include('Products.urls')),
    path('branches/', include('Branches.urls')),
    path('customers/', include('Customers.urls')),
    path('partners/', include('Partners.urls')),
    path('hr/', include('HR.urls')),
    path('barcode/', include('Barcode.urls')),
    path('invoices/', include('Invoices.urls')),
    path('select2/', include('django_select2.urls')),
    path('reports/', include('Reports.urls')),
    path('calendar/', include('Calendar.urls')),
    path('maintenance/', include('Maintenance.urls')),
    path('projects/', include('Projects.urls')),
    path('setup/', include('Setting.urls')),
    path('password_reset/', auth_views.PasswordResetView.as_view, name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view, name='password_reset_done'),
    path('reset/<slug:uidb64>/<slug:token>/', auth_views.PasswordResetConfirmView.as_view, name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view, name='password_reset_complete'),
    path('POS/', include('POS.urls')),
    path('chat/', include('Chat.urls')),
    path('information/', include('Information.urls')),
    path('ckeditor', include('ckeditor_uploader.urls')),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)