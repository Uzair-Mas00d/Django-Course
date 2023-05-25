from rest_framework import mixins, viewsets

from .models import Product
from .serializers import ProductSerializer

# help in permforming CRUD
class ViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class GenericViewSet( # viewset for performing specific CRUD Opreations
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
    ):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

# product_list_view = GenericViewSet.as_view({'get':'list'})
# product_detail_view = GenericViewSet.as_view({'get':'retrieve'})