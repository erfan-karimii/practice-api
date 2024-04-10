from rest_framework import serializers
from rest_framework.validators import ValidationError

from product.models import ProductAttributeValue , OptionGroupValue


class ShowTitleField(serializers.RelatedField):
    def to_representation(self, value):
        return value.title


class ListAttributeValueSerializer(serializers.ModelSerializer):
    product = ShowTitleField(read_only=True)
    attribute = ShowTitleField(read_only=True)
    class Meta:
        model = ProductAttributeValue
        fields = ('id','product','attribute','value_text','value_integer',
                  'value_float','value_option','value_multi_option')
    

class CreateAttributeValueSerializer(serializers.ModelSerializer):
    value_option = serializers.IntegerField(allow_null=True,required=False)
    value_multi_option = serializers.ListField(child=serializers.IntegerField(),required=False,allow_null=True)
    class Meta:
        model = ProductAttributeValue
        fields = '__all__'
    
    def validate_value_option(self, data):
        obj = OptionGroupValue.objects.filter(id=data)
        if obj.exists() :
            return obj.first()
        else:
            return None
    
    def validate_value_multi_option(self,data):
        if data  in OptionGroupValue.objects.all().values('id'):
            return OptionGroupValue.objects.filter(id__in=data)
        else:
            return []

    def validate(self, attrs:dict) -> dict:
        product = attrs.get('product')
        product_attribute = attrs.get('attribute')

        if product.product_class != product_attribute.product_class:
            raise ValidationError('this attribute does not blong to this product')
        
        product_attribute_type = product_attribute.type

        if attrs.get(product_attribute_type,None) == None:
            raise ValidationError({product_attribute_type:"'None' value for this field is not allowed"})
        
        elif product_attribute_type in ['value_option','value_multi_option'] and product.structure != 'child':
            raise ValidationError({product_attribute_type:"value_option and value_multi_option are only for child product"})

        
        return attrs


class UpdateAttributeValueSerializer(serializers.ModelSerializer):
    value_option = serializers.IntegerField(allow_null=True,required=False)
    value_multi_option = serializers.ListField(child=serializers.IntegerField(),required=False,allow_null=True)

    class Meta:
        model = ProductAttributeValue
        fields = ["value_text","value_integer","value_float","value_option","value_multi_option"]
    
    def validate_value_option(self, data):
        obj = OptionGroupValue.objects.filter(id=data)
        if obj.exists() :
            return obj.first()
        else:
            return None
    
    def validate_value_multi_option(self,data):
        if data  in OptionGroupValue.objects.all().values('id'):
            return OptionGroupValue.objects.filter(id__in=data)
        else:
            return []

    
    def update(self, instance:ProductAttributeValue, validated_data):
        product_attribute_type = instance.attribute.type
        if validated_data.get(product_attribute_type,None) == None:
            raise ValidationError({product_attribute_type:"'None' value for this field is not allowed"})

        return super().update(instance, validated_data)

