from rest_framework import serializers
from product.models import ProductClass , ProductAttributeValue, ProductAttribute, OptionGroup , OptionGroupValue
from rest_framework.validators import ValidationError


class OptionGroupValueSerializerField(serializers.ModelSerializer):
    class Meta:
        model = OptionGroupValue
        fields = ('title',)
        

class OptiongroupSerializerField(serializers.ModelSerializer):
    value = OptionGroupValueSerializerField(source='optiongroupvalue_set',many=True,read_only=True)
    class Meta:
        model = OptionGroup
        fields = ('title','value')


class ProductClassAttributeSerializerField(serializers.ModelSerializer):
    product_class = serializers.PrimaryKeyRelatedField(queryset=ProductClass.objects.all())
    option_group = OptiongroupSerializerField()
    class Meta:
        model = ProductAttribute
        fields = ('title','type','option_group','required','product_class')
        extra_kwargs = {'product_class': {'write_only': True}}
        
        
class ListProductClassSerializer(serializers.ModelSerializer):
    attrs = ProductClassAttributeSerializerField(source='attributes',many=True,read_only=True)
    class Meta:
        model = ProductClass
        fields = ('id','title','description','slug','track_stock','require_shipping','attrs')

