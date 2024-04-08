from rest_framework import serializers
from rest_framework.validators import ValidationError
from product.models import Product , ProductAttribute , ProductAttributeValue , ProductClass , OptionGroupValue , OptionGroup


class ShowTitleField(serializers.RelatedField):
    def to_representation(self, value):
        return value.title


class AttributeValueSerilizer(serializers.ModelSerializer):
    attr = serializers.ReadOnlyField(source='attribute.title')
    attr_type = serializers.ReadOnlyField(source='attribute.type')
    value_option = ShowTitleField(read_only=True)
    
    class Meta:
        model = ProductAttributeValue
        fields = ('attr','attr_type','value_text','value_integer','value_float','value_option',"value_multi_option")


class ListProductSerilizer(serializers.ModelSerializer):
    product_class = serializers.ReadOnlyField(source='product_class.title')
    categories = ShowTitleField(read_only=True,many=True)
    attributes = AttributeValueSerilizer(source='productattributevalue_set',many=True)
    class Meta:
        model = Product
        fields = ('id','structure','title','product_class','categories','attributes')


class DetailProductSerilizer(serializers.ModelSerializer):
    product_class = serializers.ReadOnlyField(source='product_class.title')
    categories = ShowTitleField(read_only=True,many=True)
    attributes = AttributeValueSerilizer(source='productattributevalue_set',many=True)
    
    class Meta:
        model = Product
        # fields = ('id','structure','title','product_class','categories','attributes')
        fields = "__all__"


class CreateProductSerializer(serializers.ModelSerializer):
    parent = serializers.IntegerField()
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


######
class OptionGroupValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = OptionGroupValue
        fields = ('title',)
        

class OptiongroupSerializer(serializers.ModelSerializer):
    value = OptionGroupValueSerializer(source='optiongroupvalue_set',many=True,read_only=True)
    class Meta:
        model = OptionGroup
        fields = ('title','value')


class AttributeValueSerilizer(serializers.ModelSerializer):

    option_group = OptiongroupSerializer(read_only=True)
    class Meta:
        model = ProductAttribute
        fields = ('title','type','option_group','required')
        
        
class ListProductClassSerilizer(serializers.ModelSerializer):

    attrs = AttributeValueSerilizer(source='attributes',many=True,read_only=True)
    class Meta:
        model = ProductClass
        fields = ('title','description','slug','track_stock','require_shipping','attrs') 
######            

        
class ListProductCategorySerilizer(serializers.ModelSerializer):
    product_class= serializers.ReadOnlyField(source='product_class.title')
    categories = ShowTitleField(read_only=True,many=True)
    attributes = AttributeValueSerilizer(source='productattributevalue_set',many=True)
    class Meta:
        model = Product
        fields = ('id','structure','title','product_class','categories','attributes')

