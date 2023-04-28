from django.urls import path, include
from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter

from api.views import PostViewSet, GroupViewSet, CommentViewSet, FollowingViewSet

router = DefaultRouter()
router.register('posts', PostViewSet, basename='post')
router.register('groups', GroupViewSet, basename='group')
router.register(r'posts/(?P<post_id>\d+)/comments',
                CommentViewSet, basename='comment')
router.register('follow', FollowingViewSet, basename='follow')



app_name = 'api'

urlpatterns = [
    path('v1/', include((router.urls, 'api'))),
    path('v1/jwt/', include('djoser.urls')),
    # JWT-эндпоинты, для управления JWT-токенами:
    path('v1/jwt/', include('djoser.urls.jwt')),

]
