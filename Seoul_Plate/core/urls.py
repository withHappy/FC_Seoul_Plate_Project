from rest_framework.routers import SimpleRouter
from rest_framework_nested import routers

from blogs.views import BlogViewSet
from bookmarks.views import BookMarkViewSet
from restaurant.views import RestViewSet, RestDetailViewSet
from review.views import ReviewViewSet, ReviewNestedViewSet
from user.views import UserViewSet

router = SimpleRouter(trailing_slash=False)

router.register(r'reviews', ReviewViewSet, basename='reviews')
router.register(r'blogs', BlogViewSet)
router.register(r'restaurant', RestViewSet, basename='restaurant')
router.register(r'restaurant', RestDetailViewSet, basename='restaurant')
router.register(r'user', UserViewSet)
router.register(r'bookmark', BookMarkViewSet)

restaurant_reviews_router = routers.NestedSimpleRouter(router, r'restaurant', lookup='owner_rest')
restaurant_reviews_router.register(r'reviews', ReviewNestedViewSet, basename='restaurant-reviews')

urlpatterns = router.urls + restaurant_reviews_router.urls

# urlpatterns = patterns('',
#     url(r'^', include(router.urls)),
#     url(r'^', include(domains_router.urls)),
# )
