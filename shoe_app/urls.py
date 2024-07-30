from django.urls import path, include
from rest_framework.routers import DefaultRouter

from order_app.views import OrderViewSet, CartViewSet
from shoe_app.views import CategoryViewSet, ShoeViewSet, ReviewViewSet

router = DefaultRouter()
router.register('category', CategoryViewSet, basename='category')
router.register('shoe', ShoeViewSet, basename='shoe')
router.register('review', ReviewViewSet, basename='review')
router.register('order', OrderViewSet, basename='order')
router.register('cart', CartViewSet, basename='cart')

urlpatterns = [
    path('', include(router.urls)),
]
