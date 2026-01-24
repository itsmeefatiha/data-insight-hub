from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Djoser Endpoints (Register, Me, Activation, Password Reset)
    path('api/auth/', include('djoser.urls')),
    
    # JWT Endpoints (Login, Refresh)
    path('api/auth/', include('djoser.urls.jwt')),
    
    # Social Auth (Google)
    path('api/auth/social/', include('djoser.social.urls')),
]