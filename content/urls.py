from django.urls import path,include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('like',views.PostLikeViewSet)
router.register('comment', views.PostCommentViewSet)

urlpatterns = [
    path('', views.UserPostCreateFeed.as_view(), name = 'user_post-view'),
    path('media/', views.UserPostMediaView.as_view(), name = 'post_media_view'),
    path('<int:pk>/', views.UserPostDetailUpdateView.as_view(), name = 'post_media_view'),
    path('', include(router.urls))
]
