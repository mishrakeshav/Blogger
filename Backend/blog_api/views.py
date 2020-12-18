from django.shortcuts import get_object_or_404
from rest_framework import generics, serializers
from .serializers import PostSerializer
from rest_framework.permissions import (
    IsAdminUser , DjangoModelPermissions, 
    BasePermission,SAFE_METHODS,IsAuthenticatedOrReadOnly
)
from rest_framework import viewsets, filters
from rest_framework.response import Response

from blog.models import Post

class PostUserWritePermission(BasePermission):
    message = 'Editing posts is restricted to the author only'

    def has_object_permission(self,request,view,obj):
        if request.method in SAFE_METHODS:
            return True 
        return request.user == obj.author


# using ModelViewSet
class PostList(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly, ]
    serializer_class = PostSerializer

    def get_object(self, queryset=None,**kwargs):
        item = self.kwargs.get('pk')
        print(item,'here')
        return get_object_or_404(Post, slug=item)

    # Define Custom QuerySet
    def get_queryset(self):
        return Post.postobjects.all()




# using ViewSet 
# class PostList(viewsets.ViewSet):
#     permission_classes = [IsAuthenticatedOrReadOnly,]
#     queryset = Post.postobjects.all()

#     def list(self,request):
#         serializer_class = PostSerializer(self.queryset,many=True)
#         return Response(serializer_class.data)

#     def retrieve(self,request,pk=None):
#         post =  get_object_or_404(self.queryset,pk=pk)
#         serializer_class = PostSerializer(post)
#         return Response(serializer_class.data)

#     def update(self,request, pk=None):
#         pass 

#     def partial_update(self,request,pk=None):
#         pass 

#     def destroy(self,request,pk=None):
#         pass 

# class PostList(generics.ListCreateAPIView):
#     permission_classes = [IsAuthenticatedOrReadOnly,]
#     queryset = Post.postobjects.all()
#     serializer_class = PostSerializer

# class PostDetail(generics.RetrieveUpdateDestroyAPIView,PostUserWritePermission):
#     permission_classes = [PostUserWritePermission,]
#     queryset = Post.objects.all() 
#     serializer_class = PostSerializer


""" Concrete View Classes
#CreateAPIView
Used for create-only endpoints.
#ListAPIView
Used for read-only endpoints to represent a collection of model instances.
#RetrieveAPIView
Used for read-only endpoints to represent a single model instance.
#DestroyAPIView
Used for delete-only endpoints for a single model instance.
#UpdateAPIView
Used for update-only endpoints for a single model instance.
##ListCreateAPIView
Used for read-write endpoints to represent a collection of model instances.
RetrieveUpdateAPIView
Used for read or update endpoints to represent a single model instance.
#RetrieveDestroyAPIView
Used for read or delete endpoints to represent a single model instance.
#RetrieveUpdateDestroyAPIView
Used for read-write-delete endpoints to represent a single model instance.
"""