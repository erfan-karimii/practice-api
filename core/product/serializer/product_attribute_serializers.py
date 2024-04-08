from rest_framework import serializers
from product.models import ProductClass , ProductAttribute , OptionGroup , OptionGroupValue

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
    product_class = serializers.PrimaryKeyRelatedField(queryset=ProductClass.objects.all())
    class Meta:
        model = ProductAttribute
        fields = ('title','type','option_group','required','product_class')
