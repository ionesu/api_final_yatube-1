from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView, TokenRefreshView
)

from api import views as api_views

router_1 = DefaultRouter()
router_1.register(
    r'^posts',
    api_views.PostsViewSet,
    basename='posts'
)
router_1.register(
    r'^posts/(?P<post_id>[0-9]+)/comments',
    api_views.CommentsViewSet,
    basename='comments'
)
router_1.register(
    r'^follow',
    api_views.FollowViewSet,
    basename='follow'
)
router_1.register(
    r'^group',
    api_views.GroupViewSet,
    basename='group'
)

urlpatterns = [
    path(
        'v1/token/',
        TokenObtainPairView.as_view(),
        name='token_obtain_pair'
    ),
    path(
        'v1/token/refresh/',
        TokenRefreshView.as_view(),
        name='token_refresh'
    ),
    path('v1/', include(router_1.urls)),
]
