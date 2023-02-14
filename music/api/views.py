from django.db.models import Count
from rest_framework import generics
from rest_framework.views import APIView

from music.api import serializers
from music.models import Music


class PopularMusicListView(generics.ListAPIView):
    serializer_class = serializers.ArticleListSerializer

    def get_queryset(self):
        queryset = Music.objects.annotate(num_likes=Count('favorite_musics')).order_by('-num_likes')[:1]
        return queryset