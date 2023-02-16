from django.db.models import Count
from rest_framework import generics

from music.api import serializers
from music.models import ChooseMusicByCategory, Music

# Home API Views
class PopularMusicListView(generics.ListAPIView):
    serializer_class = serializers.MusicListSerializer

    def get_queryset(self):
        queryset = Music.objects.annotate(num_likes=Count('favorite_musics')).filter(status=True).order_by('-num_likes')[:1]
        return queryset


class RecentMusicListView(generics.ListAPIView):
    serializer_class = serializers.MusicListSerializer

    def get_queryset(self):
        queryset = Music.objects.published().order_by('-created_at')
        return queryset


class MusicByCategoryListView(generics.ListAPIView):
    serializer_class = serializers.MusicListSerializer
    
    def get_queryset(self):
        category_object = ChooseMusicByCategory.objects.last()
        queryset = Music.objects.published().filter(category__id=category_object.category.id)
        return queryset


class MusicByTrendCategoryListView(generics.ListAPIView):
    serializer_class = serializers.MusicListSerializer
    
    def get_queryset(self):
        queryset = Music.objects.published().filter(category__title='trend')
        return queryset
