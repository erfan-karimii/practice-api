from django.db.models import Q
from django.http import Http404
from django.db.models.deletion import ProtectedError

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.validators import ValidationError

from drf_spectacular.utils import extend_schema

from product.serializer import *
from product.models import Product , ProductClass , ProductAttribute , ProductAttributeValue

from utils.db.selector import get_object
# Create your views here.


class ListProductView(APIView):
    # serializer_class = ListProductSerilizer
    def get(self,request,*args,**kwargs):
        products = Product.objects.filter(~Q(structure=Product.ProductTypeChoice.child) & Q(is_public=True))
        serializer = ListProductSerilizer(products,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    @extend_schema(request=CreateProductSerializer,)
    def post(self,request,*args,**kwargs):
        
        serializer = CreateProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'product created'},status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class DetailProductView(APIView):
    @extend_schema(request=DetailProductSerializer)
    def get(self,request,id,*args,**kwargs):
        products = Product.objects.get(~Q(structure=Product.ProductTypeChoice.parent) & Q(is_public=True,id=id))
        serializer = DetailProductSerializer(products)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    @extend_schema(request=UpdateProductSerializer)
    def patch(self,request,id):
        obj = get_object(id=id,class_=Product)
        serializer = UpdateProductSerializer(obj,data=request.data,partial=True)
        if serializer.is_valid():
            validated_product_class = serializer.validated_data.get('product_class',None)
            
            if obj.product_class != validated_product_class and obj.productattributevalue_set.exists():
                raise ValidationError({'please remove product attribute values first!'})
            
            serializer.save()
            return Response({'product updated successfuly'},status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,id):
        obj = get_object(id=id,class_=Product)
        obj.delete()
        return Response({'product deleted successfully'},status=status.HTTP_204_NO_CONTENT)
        

class ListProductClassView(APIView):
    def get(self,request):
        product_classes = ProductClass.objects.all()
        serializer = ListProductClassSerializer(product_classes,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    @extend_schema(
        request=ListProductClassSerializer,
    )
    def post(self,request):
        serializer = ListProductClassSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'product class created successfully'},status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class DetailProductClassView(APIView):
    def get(self,request,id):
        product_class = get_object(id=id,class_=ProductClass)
        serializer = ListProductClassSerializer(product_class)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    @extend_schema(request=ListProductClassSerializer)
    def patch(self,request,id):
        obj = get_object(id=id,class_=ProductClass)
        serializer = ListProductClassSerializer(obj,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'product class updated successfully'},status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        
    
    def delete(self,request,id):
        obj = get_object(id=id,class_=ProductClass)
        obj.delete()
        return Response({'product class deleted successfully'},status=status.HTTP_204_NO_CONTENT)


class ListProductAttributeView(APIView):
    def get(self,request):
        product_attrs = ProductAttribute.objects.all()
        serilizer = ListAttributeSerializer(product_attrs,many=True)
        return Response(serilizer.data,status=status.HTTP_200_OK)
    
    @extend_schema(request=CreateAttributeSerializer,)
    def post(self,request):
        serializer = CreateAttributeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'attribute created successfully'},status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class DetailProductAttributeView(APIView):
    def get_object(self,id):
        try:
            instance = ProductAttribute.objects.get(id=id)
        except ProductAttribute.DoesNotExist:
            raise Http404
        
        return instance

    def get(self,request,id):
        obj = self.get_object(id=id)
        serializer = ListAttributeSerializer(obj)
        return Response(serializer.data,status=status.HTTP_200_OK)

    @extend_schema(request=CreateAttributeSerializer,)
    def patch(self,request,id):
        obj = self.get_object(id=id)
        serializer = CreateAttributeSerializer(obj,data=request.data,partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,id):
        obj = self.get_object(id=id)
        try:
            obj.delete()
        except ProtectedError:
            return Response({'please remove product attribute value of related attribute first!'},status=status.HTTP_400_BAD_REQUEST)
        return Response({'product attribute deleted successfully'},status=status.HTTP_204_NO_CONTENT)


class ListRelatedProductAttributeValue(APIView):
    def get_object(self,id,model_class):
        try:
            instance = model_class.objects.get(id=id)
        except model_class.DoesNotExist:
            raise Http404
        
        return instance
    
    def get(self,request,product_id):
        product = self.get_object(id=product_id,model_class=Product)
        product_attr_values = product.productattributevalue_set.all()
        serializer = ListAttributeValueSerializer(product_attr_values,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)        


class ListProductAttributeValue(APIView):             
    
    @extend_schema(request=CreateAttributeValueSerializer,)
    def post(self,request):
        serializer = CreateAttributeValueSerializer(data=request.data)
        if serializer.is_valid():
            print('befor')
            serializer.save()
            print('after')
            return Response({'product attribute value create successfully'},status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)        


class DetailProductValueAttribute(APIView):
    def get_object(self,id):
        try:
            instance = ProductAttributeValue.objects.get(id=id)
        except ProductAttributeValue.DoesNotExist:
            raise Http404
        
        return instance
    
    def delete(self,request,id):
        obj = self.get_object(id=id)
        obj.delete()
        return Response({'product attribute value deleted successfully'},status=status.HTTP_204_NO_CONTENT)
    
    @extend_schema(request=UpdateAttributeValueSerializer)
    def patch(self,request,id):
        obj = self.get_object(id=id)
        serializer = UpdateAttributeValueSerializer(obj,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'product updated successfuly'},status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    

    



# class ListProductCategoryView(APIView):
#     serializer_class = ListProductCategorySerilizer
#     def get(self,request,id,*args,**kwargs):
#         products = Product.objects.filter(~Q(structure=Product.ProductTypeChoice.child) & Q(is_public=True,categories__id=id))
#         serializer = ListProductCategorySerilizer(products,many=True)
#         return Response(serializer.data,status=status.HTTP_200_OK)
