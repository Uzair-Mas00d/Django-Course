from rest_framework.routers import DefaultRouter

from products.viewsets import ViewSet,GenericViewSet


router = DefaultRouter()
# router.register('products',ViewSet,basename='products')
router.register('products',GenericViewSet,basename='products')

urlpatterns = router.urls