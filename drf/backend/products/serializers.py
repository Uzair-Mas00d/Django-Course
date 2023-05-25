from rest_framework import serializers
from products.models import Product
from rest_framework.reverse import reverse
from .validotars import validate_title,validate_title_no_hello,unique_product_title
from api.serializers import UserPublicSerializer


class ProductInlineSerializer(serializers.Serializer):
    url = serializers.HyperlinkedIdentityField(view_name='product-detail',read_only=True)
    title = serializers.CharField(read_only=True)

class ProductSerializer(serializers.ModelSerializer):
    owner = UserPublicSerializer(source='user',read_only=True)
    # related_products = ProductInlineSerializer(source='user.product_set.all',read_only=True,many=True) #another way of showing nested data
    # my_user_data = serializers.SerializerMethodField(read_only=True)
    # my_discount = serializers.SerializerMethodField(read_only=True) # for changing field name
    edit_url = serializers.SerializerMethodField(read_only=True) # for updating product
    url = serializers.HyperlinkedIdentityField(view_name='product-detail') # for showing url
    title = serializers.CharField(validators=[validate_title_no_hello,unique_product_title]) # another way to valadiating
    # email = serializers.EmailField(source="user.email",read_only=True)
    # name = serializers.CharField(source='title',read_only=True)
    class Meta: 
        model = Product
        fields = [
            'owner',
            # 'email',
            'url',
            'edit_url',
            'pk',
            'title',
            # 'name',
            'content',
            'price',
            'sale_price',
            'public',
            # 'get_discount',
            # 'my_discount',
            # 'my_user_data',
            # 'related_products',
        ]
    # def get_my_user_data(self,obj):
    #     return {
    #         'username': obj.user.username
    #     }


    # def validate_title(self, value): # check valadtion of title
    #     qs = Product.objects.filter(title__iexact=value) # OR exact. exact is not case senstitive
    #     if qs.exists():
    #         raise serializers.ValidationError(f'{value} is already a product name')

    #     return value

    # def create(self, validated_data): # for sending mail
    #     # email = validated_data.pop('email') you can call it on the view
    #     return super().create(validated_data)
    
    # def update(self, instance, validated_data):
    #     email = validated_data.pop('email')
    #     return super().update(instance, validated_data)

    def get_edit_url(self,obj):
        # return f'/api/products/{obj.pk}/'
        request = self.context.get('request') # same as self.request but better
        if request is None:
            return None
        
        # return reverse('product-detail',kwargs={'pk':obj.pk},request=request)
        return reverse('product-edit',kwargs={'pk':obj.pk},request=request)

    # def get_my_discount(self,obj): # for changing field name
    #     if not hasattr(obj,'id'):
    #         return None
    #     if not isinstance(obj,Product):
    #         return None
    #     return obj.get_discount()
       