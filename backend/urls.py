from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from app_users.views import ModifierUtilisateurView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('app_users.urls')), 
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('utilisateur/modifier/', ModifierUtilisateurView.as_view(), name='modifier-utilisateur'),
    path('api/offres/', include('app_offres.urls')),
    path('api/candidatures/', include('app_candidatures.urls')),
    
]