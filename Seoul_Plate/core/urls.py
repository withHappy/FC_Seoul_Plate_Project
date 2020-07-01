from rest_framework.routers import SimpleRouter

from blogs.views import BlogViewSet
from bookmarks.views import BookMarkViewSet
from restaurant.views import RestViewSet, RestDetailViewSet
from review.views import ReviewViewSet
from user.views import UserViewSet

router = SimpleRouter(trailing_slash=False)

router.register(r'reviews', ReviewViewSet, basename='reviews')
router.register(r'blogs', BlogViewSet)
router.register(r'restaurant', RestViewSet, basename='restaurant')
router.register(r'restaurant', RestDetailViewSet, basename='restaurant')
router.register(r'user', UserViewSet)
router.register(r'bookmark', BookMarkViewSet)

urlpatterns = router.urls
