from django.db.models import Q

from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from drf_spectacular.utils import extend_schema

from product.serializer import ListProductClassSerilizer, ListProductSerilizer , ListProductCategorySerilizer ,DetailProductSerilizer , CreateProductSerializer
from product.models import Product , ProductClass
# Create your views here.


class ListProductView(APIView):
    # serializer_class = ListProductSerilizer
    def get(self,request,*args,**kwargs):
        products = Product.objects.filter(~Q(structure=Product.ProductTypeChoice.child) & Q(is_public=True))
        serializer = ListProductSerilizer(products,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    @extend_schema(
        request=CreateProductSerializer,
    )
    def post(self,request,*args,**kwargs):
        
        serializer = CreateProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'product created'},status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class DetailProductView(APIView):
    serilizer_class = DetailProductSerilizer
    def get(self,request,id,*args,**kwargs):
        products = Product.objects.get(~Q(structure=Product.ProductTypeChoice.parent) & Q(is_public=True,id=id))
        serializer = DetailProductSerilizer(products)
        return Response(serializer.data,status=status.HTTP_200_OK)

class ListProductClassView(APIView):
    def get(self,request):
        product_classes = ProductClass.objects.all()
        serilizer = ListProductClassSerilizer(product_classes,many=True)
        return Response(serilizer.data,status=status.HTTP_200_OK)

# class ListProductCategoryView(APIView):
#     serializer_class = ListProductCategorySerilizer
#     def get(self,request,id,*args,**kwargs):
#         products = Product.objects.filter(~Q(structure=Product.ProductTypeChoice.child) & Q(is_public=True,categories__id=id))
#         serializer = ListProductCategorySerilizer(products,many=True)
#         return Response(serializer.data,status=status.HTTP_200_OK)
