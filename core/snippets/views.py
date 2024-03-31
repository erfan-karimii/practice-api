from django.http import Http404
from django.contrib.auth.models import User

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status ,renderers

from snippets.models import Snippet
from snippets.serializers import SnippetSerializer ,UserSerializer
from snippets.permissions import IsOwnerOrReadOnly


class SnippetList(APIView):
    permission_classes = (IsOwnerOrReadOnly, )
    
    def get(self,request,format=None):
        snippets = Snippet.objects.all()
        serializer = SnippetSerializer(snippets,many=True)
        
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    def post(self,request,format=None):
        serializer = SnippetSerializer(data=request.data)
        if serializer.is_valid():
            instance = serializer.save(owner=request.user)
            return Response(f"object created (\'{instance.code}\')",status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class SnippetDetail(APIView):
    permission_classes = (IsOwnerOrReadOnly, )
    
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


class SnippetHighlight(APIView):
    renderer_classes = [renderers.StaticHTMLRenderer]
    def get_object(self,id):
        try:
            instance = Snippet.objects.get(id=id)
        except Snippet.DoesNotExist:
            raise Http404
        
        return instance

    def get(self, request,id, *args, **kwargs):
        snippet = self.get_object(id=id)
        return Response(snippet.highlighted)
        

class UserListView(APIView):
    def get(self,request):
        users = User.objects.all()
        serializer = UserSerializer(users,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)


class UserDetailView(APIView):
    def get(self,request,id):
        user = User.objects.get(id=id)
        serializer = UserSerializer(user)
        return Response(serializer.data,status=status.HTTP_200_OK)
                   