from rest_framework import authentication,generics,mixins,permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
# from django.http import Http404
from django.shortcuts import get_object_or_404

# from api.authentaction import TokenAuthentication
from .models import Product
# from .api.permissions import IsStaffEditorPermisson
from api.mixins import StaffEditorPermissonMixin, UserQuerySetMixin
from .serializers import ProductSerializer

# doing CRUD with Generic Api View
# class ProductCreateApiView(generics.CreateAPIView): # it use post to create and save new instance of Product
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer

#     def perform_create(self,serializer):
#         # serializer.save(user=self.request.user)
#         # print(serializer.validated_data)
#         title = serializer.validated_data.get('title')
#         content = serializer.validated_data.get('content')
#         if content is None:
#             content = title

#         serializer.save(content=content)

# product_create_view = ProductCreateApiView.as_view()


class ProductListCreateApiView(
    UserQuerySetMixin, # another way to show data to relevent user
    StaffEditorPermissonMixin, # try to avoid repetion in permission so create mixin or premession mixin
    generics.ListCreateAPIView
    ): # class use both get and post method to retrive and create object
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    # authentication_classes = [  after declring it into setting we don't need it
    #     authentication.SessionAuthentication,
    #     TokenAuthentication,
    #     # authentication.TokenAuthentication,
    # ]
    # permission_classes = [permissions.IsAdminUser,IsStaffEditorPermisson] # we overwrite setting permission
    # permission_classes = [permissions.DjangoModelPermissions]
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self,serializer):
        # serializer.save(user=self.request.user)
        # print(serializer.validated_data)
        # email = serializer.validated_data.pop('email')
        title = serializer.validated_data.get('title')
        content = serializer.validated_data.get('content')
        if content is None:
            content = title

        serializer.save(user=self.request.user,content=content)
    
    # def get_queryset(self,*args,**kwargs): # show data to relevant user
    #     qs = super().get_queryset(*args,**kwargs)
    #     request = self.request
    #     user = request.user
    #     if not user.is_authenticated:
    #         return Product.objects.none()
    #     # print(request.user)
    #     return qs.filter(user=request.user)

product_list_create_view = ProductListCreateApiView.as_view()


class ProductDetailApiView(
    UserQuerySetMixin,
    StaffEditorPermissonMixin,
    generics.RetrieveAPIView
    ): # generics.RetrieveAPIView is used to retrive object based on primary key
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    # permission_classes = [permissions.IsAdminUser,IsStaffEditorPermisson]

product_detail_view = ProductDetailApiView.as_view() # Second way to write class based view


class ProductUpdateApiView(
    UserQuerySetMixin,
    StaffEditorPermissonMixin,
    generics.UpdateAPIView
    ):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    # permission_classes = [permissions.IsAdminUser,IsStaffEditorPermisson]

    def perform_update(self,serializer):
        instance = serializer.save()
        if not instance.content:
            instance.content = instance.title

product_update_view = ProductUpdateApiView.as_view()


class ProductDestroyAPIView(
    UserQuerySetMixin,
    StaffEditorPermissonMixin,
    generics.DestroyAPIView
    ):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    # permission_classes = [permissions.IsAdminUser,IsStaffEditorPermisson]

    def perform_destroy(self,instance):
        super().perform_destroy(instance)

product_destroy_view = ProductDestroyAPIView.as_view()


# class ProductListApiView(generics.ListAPIView): # it use get method to retrive list of object From Products
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer

# product_list_view = ProductListApiView.as_view()


# Doing CRUD with mixin api view
class ProductMixinView(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    generics.GenericAPIView
    ):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer 

    def get(self,request,*args,**kwargs):
        print(args,kwargs)
        pk = kwargs.get('pk')
        if pk is not None:
            return self.retrieve(request,*args,**kwargs)
        
        return self.list(request,*args,*kwargs)
    
    def post(self,request,*args,**kwargs):
        return self.create(request,*args,*kwargs)
    
    def perform_create(self,serializer):
        title = serializer.validated_data.get('title')
        content = serializer.validated_data.get('content')
        if content is None:
            content = 'this is single view doing cool stuff'

        serializer.save(content=content)

product_mixin_view = ProductMixinView.as_view()


# doing CRUD with function view
@api_view(['GET','POST'])
def product_alt_view(request,pk=None,*args,**kwargs):
    method = request.method

    if method == "GET":
        # Detail view
        if pk is not None:
            # queryset = Product.objects.filter(pk=pk)
            # if not queryset.exists():
            #     return Http404  
            obj = get_object_or_404(Product,pk=pk)
            data = ProductSerializer(obj, many=False).data

            return Response(data)
        # list view
        queryset = Product.objects.all()
        data = ProductSerializer(queryset, many=True).data # many use for list of data
        return Response(data)
    
    if method == "POST":
        searlizer = ProductSerializer(data=request.data)

        if searlizer.is_valid(raise_exception=True):
            title = searlizer.validated_data.get('title')
            content = searlizer.validated_data.get('content')
            if content is None:
                content = title

            searlizer.save(content=content)
            return Response(searlizer.data)
