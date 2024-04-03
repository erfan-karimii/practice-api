from django.db.models import Q

from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from product.serializer import ListProductSerilizer , ListProductCategorySerilizer ,DetailProductSerilizer
from product.models import Product
# Create your views here.


class ListProductView(APIView):
    def get(self,request,*args,**kwargs):
        products = Product.objects.filter(~Q(structure=Product.ProductTypeChoice.child) & Q(is_public=True))
        serializer = ListProductSerilizer(products,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)


class DetailProductView(APIView):
    def get(self,request,id,*args,**kwargs):
        products = Product.objects.get(~Q(structure=Product.ProductTypeChoice.parent) & Q(is_public=True,id=id))
        serializer = DetailProductSerilizer(products)
        return Response(serializer.data,status=status.HTTP_200_OK)

class ListProductCategoryView(APIView):
    def get(self,request,id,*args,**kwargs):
        products = Product.objects.filter(~Q(structure=Product.ProductTypeChoice.child) & Q(is_public=True,categories__id=id))
        serializer = ListProductCategorySerilizer(products,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
