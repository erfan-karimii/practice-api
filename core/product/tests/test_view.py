from django.urls import reverse

from rest_framework.test import APITestCase
from rest_framework import status
from model_bakery import baker

from product.models import Product


class TestViewsApi(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.product = baker.make(Product,structure='parent',title='title')
        cls.product1 = baker.make(Product,structure='child',parent=cls.product,title='title1')
        cls.product2 = baker.make(Product,structure='child',parent=cls.product,title='title2')
        cls.product3 = baker.make(Product,structure='standalone',title='title3')
        
        cls.url = reverse("product:product-list")
        
    
    def test_view(self):
        x = [{"title":title} for title in [self.product,self.product1,self.product2,self.product3]]
        response = self.client.get(self.url)
        
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(len(response.data),2)
        self.assertEqual(response.data,x)
        

        