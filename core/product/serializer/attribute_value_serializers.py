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
        fields = ('product','attribute','value_text','value_integer',
                  'value_float','value_option','value_multi_option')
    



class CreateAttributeValueSerializer(serializers.ModelSerializer):
    value_option = serializers.IntegerField(allow_null=True,required=False)
    value_multi_option = serializers.ListField(child=serializers.IntegerField())
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
            data = OptionGroupValue.objects.filter(id__in=data)
        else:
            data = None
        return data

    # def 
    
    
