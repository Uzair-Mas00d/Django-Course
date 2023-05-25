import json
# from django.http import JsonResponse,HttpResponse
from django.forms.models import model_to_dict
from rest_framework.decorators import api_view
from rest_framework.response import Response

from products.models import Product
from products.serializers import ProductSerializer

# def api_home(request, *args, **kwargs):
#     # request.body
#     print(request.GET) # url query params
#     print(request.POST)
#     body = request.body # byte string of JSON data
#     data = {}
#     try:
#         data = json.loads(body) # string of JSON data -> Python Dict
#     except:
#         pass
#     print(data)
#     data['params'] = dict(request.GET)
#     data['headers'] = dict(request.headers)
#     data['content_type'] = request.content_type
#     return JsonResponse(data)

    # model_data = Product.objects.all().order_by("?").first()
    # data = {}
    # if model_data:
    #     data['id'] = model_data.id
    #     data['title'] = model_data.title
    #     data['content'] = model_data.content
    #     data['price'] = model_data.price
    #       --- OR ---
    #     data = model_to_dict(model_data)
    # return JsonResponse(data)
    # return HttpResponse(data) --> it throw an error beacuse it accept string as a parameter

@api_view(["POST"])
def api_home(request, *args, **kwargs):
    """
    DRF API View
    """
    # instance = Product.objects.all().order_by("?").first()
    # data = {}
    # if instance:
          # data = model_to_dict(instance, fields=['id', 'title', 'price','sale_price'])
    #     data = ProductSerializer(instance).data

    # data = request.data
    searlizer = ProductSerializer(data=request.data)
    if searlizer.is_valid(raise_exception=True):
        # print(searlizer.data)
        # data = searlizer.data
        # return Response(data)

        # instance = searlizer.save()
        print(searlizer.data)
        return Response(searlizer.data)