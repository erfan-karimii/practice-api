from rest_framework import serializers
from product.models import Product , ProductAttributeValue
from rest_framework.validators import ValidationError


class ShowTitleField(serializers.RelatedField):
    def to_representation(self, value):
        return value.title


class ProductAttributeSerializerField(serializers.ModelSerializer):
    attr = serializers.ReadOnlyField(source='attribute.title')
    attr_type = serializers.ReadOnlyField(source='attribute.type')
    value_option = ShowTitleField(read_only=True)
    
    class Meta:
        model = ProductAttributeValue
        fields = ('attr','attr_type','value_text','value_integer','value_float','value_option',"value_multi_option")

    
class DetailProductSerilizer(serializers.ModelSerializer):
    product_class = serializers.ReadOnlyField(source='product_class.title',required=False)
    categories = ShowTitleField(read_only=True,many=True)
    attributes = ProductAttributeSerializerField(source='productattributevalue_set',many=True)
    
    class Meta:
        model = Product
        # fields = ('id','structure','title','product_class','categories','attributes')
        fields = "__all__"


class ListProductSerilizer(serializers.ModelSerializer):
    product_class = serializers.ReadOnlyField(source='product_class.title')
    categories = ShowTitleField(read_only=True,many=True)
    attributes = ProductAttributeSerializerField(source='productattributevalue_set',many=True)
    class Meta:
        model = Product
        fields = ('id','structure','title','product_class','categories','attributes')


class CreateProductSerializer(serializers.ModelSerializer):
    parent = ()
    class Meta:
        model = Product
        fields = ('title','structure','parent','product_class','slug',)
        
    def validate_parent(self,value):
        obj = Product.objects.filter(id=value)
        if obj.exists() :
            return obj.first()
        else:
            return None
    
    def validate(self, attrs):
        if attrs.get('structure') != Product.ProductTypeChoice.child:
            attrs['parent'] = None
        elif attrs.get('parent') is None:
            raise ValidationError({'parent':'Parent must be set'})
      
        return super().validate(attrs)

