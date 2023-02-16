from django.db.models import Count
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import permissions, status

from music.api import serializers
from music.models import ChooseMusicByCategory, HomeSlider, Music


# Home API Views
class PopularMusicListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.MusicListSerializer

    def get_queryset(self):
        queryset = Music.objects.annotate(num_likes=Count('favorite_musics')).filter(status=True).order_by('-num_likes')[:1]
        return queryset


class RecentMusicListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.MusicListSerializer

    def get_queryset(self):
        queryset = Music.objects.published().order_by('-created_at')
        return queryset


class MusicByCategoryListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.MusicListSerializer

    def get_queryset(self):
        category_object = ChooseMusicByCategory.objects.last()
        queryset = Music.objects.published().filter(category__id=category_object.category.id)
        return queryset


class MusicByTrendCategoryListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.MusicListSerializer

    def get_queryset(self):
        queryset = Music.objects.published().filter(category__title='trend')
        return queryset

class SliderHomePage(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.SliderHomePageSerializer

    def get_queryset(self):
        queryset = HomeSlider.objects.filter(status=True)
        return queryset
# End Home API Views


class MusicDetailView(generics.GenericAPIView):
    # permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        instance = Music.objects.get(id=pk)
        serializer = serializers.MusicDetailSerializer(instance=instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

