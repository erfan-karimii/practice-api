from snippets.models import Snippet
from snippets.serializers import SnippetSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class SnippetList(APIView):
    def get(self,request,format=None):
        snippets = Snippet.objects.all()
        serializer = SnippetSerializer(snippets,many=True)
        
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    def post(self,request,format=None):
        serializer = SnippetSerializer(data=request.data)
        if serializer.is_valid():
            instance = serializer.save()
            return Response(f"object created (\'{instance.code}\')",status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class SnippetDetail(APIView):
    def get_object(self,id):
        try:
            instance = Snippet.objects.get(id=id)
        except Snippet.DoesNotExist:
            raise Http404
        
        return instance
        
    def get(self,request,id,format=None):
        instance = self.get_object(id=id)

        serializer = SnippetSerializer(instance)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    def put(self,request,id,format=None):
        instance = self.get_object(id=id)
        
        serializer = SnippetSerializer(instance,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
            
    
    def delete(self,request,id,format=None):
        instance = self.get_object(id=id)
        instance.delete()
        
        return Response('snippet delete successfully',status=status.HTTP_204_NO_CONTENT)
        
        