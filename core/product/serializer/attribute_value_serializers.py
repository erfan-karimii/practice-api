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
    # value_option = serializers.PrimaryKeyRelatedField(allow_null=True, queryset=OptionGroupValue.objects.all())
    class Meta:
        model = ProductAttributeValue
        fields = '__all__'
    
    def validate_value_option(self, attrs):
        import logging
        logger = logging.getLogger(__name__)
        logger.warning('yrfdetyudyfutyuastfyua')
        return attrs