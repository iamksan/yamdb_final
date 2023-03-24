from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.v1.views import (CategoryViewSet, CommentViewSet, GenreViewSet,
                          get_jwt_token, ReviewViewSet, signup, TitleViewSet,
                          UserViewSet)

router_v1 = DefaultRouter()
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews',
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments',
)
router_v1.register('titles', TitleViewSet, basename='titles')
router_v1.register('genres', GenreViewSet, basename='genres')
router_v1.register('categories', CategoryViewSet, basename='categories')
router_v1.register('users', UserViewSet, basename='users')

urlpatterns = [
    path('', include(router_v1.urls)),
    path('auth/token/', get_jwt_token, name='token'),
    path('auth/signup/', signup),
]
