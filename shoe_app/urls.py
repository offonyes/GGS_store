from django.urls import path, include
from rest_framework.routers import DefaultRouter

from shoe_app.views import CategoryViewSet, ShoeViewSet, ReviewViewSet

router = DefaultRouter()
router.register('category', CategoryViewSet)
router.register('shoe', ShoeViewSet)
router.register('review', ReviewViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
