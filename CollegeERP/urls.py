from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from info.views import UserList

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='info/login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(template_name='info/logout.html'), name='logout'),
    path('', include('info.urls')),
    # path('api/', include('info.urls')),
]
