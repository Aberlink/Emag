from rest_framework import generics
from blog.models import Article
from rest_framework.permissions import (
    BasePermission,
    DjangoModelPermissionsOrAnonReadOnly,
    SAFE_METHODS,
    IsAuthenticated,
)
from .serializers import ArticleSerializer


class EditPostPermision(BasePermission):
    message = "Only author can edit or delete their posts."

    def has_object_permission(self, request, view, obj):
        """allow to view all articles, edit only author"""
        if request.method in SAFE_METHODS:
            return True
        return obj.author == request.user


class ArticleList(generics.ListCreateAPIView):
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
 

class ArticleDetail(generics.RetrieveUpdateDestroyAPIView, EditPostPermision):
    permission_classes = [EditPostPermision]
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    def perform_update(self, serializer):
        serializer.save(author=self.request.user)
