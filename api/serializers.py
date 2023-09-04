from rest_framework import serializers
from blog.models import Article



class ArticleSerializer(serializers.ModelSerializer):
    author_email = serializers.EmailField(source='author.username', read_only=True)

    class Meta:
        model = Article
        fields = "__all__"