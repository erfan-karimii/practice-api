from rest_framework import serializers
from rest_framework.validators import ValidationError

from product.models import ProductAttributeValue , ProductAttribute , OptionGroup , OptionGroupValue


class OptionGroupValueSerializerField(serializers.ModelSerializer):
    class Meta:
        model = OptionGroupValue
        fields = ('title',)


class OptionGroupSerializerField(serializers.ModelSerializer):
    value = OptionGroupValueSerializerField(source='optiongroupvalue_set',many=True,read_only=True)
    class Meta:
        model = OptionGroup
        fields = ('id','title','value')


class ListAttributeSerializer(serializers.ModelSerializer):
    option_group = OptionGroupSerializerField()
    class Meta:
        model = ProductAttribute
        fields = ('title','type','option_group','required')


class CreateAttributeSerializer(serializers.ModelSerializer):
    option_group = serializers.IntegerField()
    class Meta:
        model = ProductAttribute
        fields = ('title','type','option_group','required','product_class')
    
    def validate_option_group(self,value):
        obj = OptionGroup.objects.filter(id=value)
        if obj.exists() :
            return obj.first()
        else:
            return None
    
    def validate(self, attrs):
        if attrs.get('type') in ['value_option','value_multi_option'] and attrs.get('option_group') == None:
            raise ValidationError({'option_group':'Option Group must be set'})
        else:
            attrs['option_group'] = None
      
        return super().validate(attrs)
