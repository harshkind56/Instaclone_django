from django.contrib import admin
from django.urls import path, include
from users import views as user_views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework_simplejwt.views import TokenVerifyView
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.views import APIView
from django.conf import settings

from rest_framework.routers import DefaultRouter




urlpatterns = [
    path('admin/', admin.site.urls),
    path('', user_views.index, name = 'home' ),
    path('signup/', user_views.Signup, name = 'user_signup' ),

    path('add/', user_views.create_user, name = "create_user_of"),# signupAPI.
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('login/',TokenObtainPairView.as_view(), name = 'login-api' ),
    path('list/', user_views.user_list, name = 'user_list_api'),
    path('users/<int:pk>/', user_views.UserProfileDetail.as_view(), name ="get_single_user" ),
    path('edge/', user_views.UserNetworkEdgeView.as_view(), name = "network_edge"),
    path('posts/', include('content.urls'))
    
   

   # path('update/', user_views.userProfileUpdated, name = "user_profile_update")
    # Base_URl + 'users.url'
]

if settings.DEBUG:
    urlpatterns +=  static(settings.MEDIA_URL , document_root=settings.MEDIA_ROOT )
