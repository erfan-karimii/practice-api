from rest_framework.views import APIView
from product.serializer import ListProductSerilizer

# Create your views here.

class ListProductView(APIView):
    def get(self,request,*args,**kwargs):
        pass
