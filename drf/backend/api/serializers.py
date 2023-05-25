from rest_framework import serializers

class UserProductInlineSerializer(serializers.Serializer):
    url = serializers.HyperlinkedIdentityField(view_name='product-detail',read_only=True)
    title = serializers.CharField(read_only=True)

class UserPublicSerializer(serializers.Serializer):
    username = serializers.CharField(read_only=True)
    id = serializers.IntegerField(read_only=True)
    # other_product = serializers.SerializerMethodField(read_only=True)

    # def get_other_product(self,obj): Showing nested data
    #     user = obj
    #     my_products = user.product_set.all()[:5] #user.product_set.all()[:5] retrieves the related products of the user
    #     return UserProductInlineSerializer(my_products,many=True,context=self.context).data
