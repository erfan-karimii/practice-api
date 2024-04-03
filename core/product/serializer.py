from rest_framework import serializers
from product.models import Product , ProductAttribute , ProductAttributeValue


class ShowTitleField(serializers.RelatedField):
    def to_representation(self, value):
        return value.title


class AttributeSerilizer(serializers.ModelSerializer):
    attr = serializers.ReadOnlyField(source='attribute.title')
    attr_type = serializers.ReadOnlyField(source='attribute.type')
    value_option = ShowTitleField(read_only=True)
    
    class Meta:
        model = ProductAttributeValue
        fields = ('attr','attr_type','value_text','value_integer','value_float','value_option',"value_multi_option")


class ListProductSerilizer(serializers.ModelSerializer):
    product_class = serializers.ReadOnlyField(source='product_class.title')
    categories = ShowTitleField(read_only=True,many=True)
    attributes = AttributeSerilizer(source='productattributevalue_set',many=True)
    class Meta:
        model = Product
        fields = ('id','structure','title','product_class','categories','attributes')


class DetailProductSerilizer(serializers.ModelSerializer):
    product_class = serializers.ReadOnlyField(source='product_class.title')
    categories = ShowTitleField(read_only=True,many=True)
    attributes = AttributeSerilizer(source='productattributevalue_set',many=True)
    
    class Meta:
        model = Product
        # fields = ('id','structure','title','product_class','categories','attributes')
        fields = "__all__"


class ListProductCategorySerilizer(serializers.ModelSerializer):
    product_class= serializers.ReadOnlyField(source='product_class.title')
    categories = ShowTitleField(read_only=True,many=True)
    attributes = AttributeSerilizer(source='productattributevalue_set',many=True)
    class Meta:
        model = Product
        fields = ('id','structure','title','product_class','categories','attributes')
        # exclude = ('structure','is_public')
