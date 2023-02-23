from django.db.models import Count
from rest_framework import generics, permissions, status
from rest_framework.response import Response

from music.api import serializers
from music.models import ChooseMusicByCategory, HomeSlider, Music, Category, FavoriteMusic


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
    serializer_class = serializers.MusicByCategorySerializer

    def get_queryset(self):
        category_object = ChooseMusicByCategory.objects.last()
        if category_object is None:
            return Music.objects.none()
        else:
            queryset = Music.objects.published().filter(category__id=category_object.category.id)
            return queryset

    def get_serializer_context(self):
        context = super().get_serializer_context()
        category_object = ChooseMusicByCategory.objects.last()
        if category_object is None:
            context['category_name'] = "None"
        else:
            context['category_name'] = category_object.category.title
        return context


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


class CateogryListView(generics.ListAPIView):
    # permission_classes = [permissions.IsAuthenticated]

    serializer_class = serializers.CategoryListSerializer

    def get_queryset(self):
        queryset = Category.objects.all()
        return queryset


class InternationalMusicList(generics.ListAPIView):
    serializer_class = serializers.MusicListSerializer
    queryset = Music.objects.published().filter(type='International')
    
   
class UserFavoriteMusicView(generics.ListAPIView):
    serializer_class = serializers.MusicListSerializer

    def get_queryset(self):
        user = self.request.user
        favorite_music_ids = FavoriteMusic.objects.filter(user=user).values_list('music_id', flat=True)
        return Music.objects.filter(id__in=favorite_music_ids)


