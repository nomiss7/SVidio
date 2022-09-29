from rest_framework import generics, permissions, viewsets
from apps.api.blog.serializers import ArticleSerializer
from apps.blog.models import Article


class ArticleViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAdminUser]
    serializer_class = ArticleSerializer
    queryset = Article.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user.username)

    def get_queryset(self):
        queryset = Article.objects.filter()
        if self.request.query_params.get('category'):
            queryset = queryset.filter(category=self.request.query_params['category'])

        if self.request.query_params.get('user'):
            queryset = queryset.filter(name__icontains=self.request.query_params['user'])

        return queryset
