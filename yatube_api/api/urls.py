from django.db import router
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import PostViewSet, CommentViewSet, GroupViewSet, FollowViewSet


router = DefaultRouter()

router.register('posts', PostViewSet)
router.register('groups', GroupViewSet)
router.register('follow',FollowViewSet, basename='follow')
#  basename должен быть указан, т.к. queryset не задан во вьюсете, а определён через метод get_queryset()
router.register(r'posts/(?P<post_id>\d+)/comments', CommentViewSet, basename='comments')


urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/', include('djoser.urls')),
    path('v1/', include('djoser.urls.jwt')),
]
