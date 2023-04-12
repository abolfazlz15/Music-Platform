from django.db.models import Count
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from music.api import serializers
from music.models import ChooseMusicByCategory, HomeSlider, Music, Category, FavoriteMusic

from rest_framework.filters import SearchFilter

# Home API Views
class PopularMusicListView(generics.ListAPIView):
    serializer_class = serializers.MusicListSerializer

    def get_queryset(self):
        queryset = Music.objects.annotate(num_likes=Count('favorite_musics')).filter(status=True).order_by('-num_likes')[:10]
        return queryset


class RecentMusicListView(generics.ListAPIView):  
    serializer_class = serializers.MusicListSerializer

    def get_queryset(self):
        queryset = Music.objects.published().order_by('-created_at')
        return queryset


class MusicByCategoryListView(generics.ListAPIView):
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
            context['category_name'] = 'None'
        else:
            context['category_name'] = category_object.category.title
        return context


class MusicByTrendCategoryListView(generics.ListAPIView):
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
    serializer_class = serializers.MusicDetailSerializer
    def get(self, request, pk):
        instance = Music.objects.get(id=pk)
        if request.user.favorite_musics.filter(music__id=pk, user=request.user.id).exists():
            is_liked = True
        else:
            is_liked = False
        serializer = serializers.MusicDetailSerializer(instance=instance, context={'request': request, 'is_liked': is_liked})
        return Response(serializer.data, status=status.HTTP_200_OK)


class CateogryListView(generics.ListAPIView):
    serializer_class = serializers.CategoryListSerializer

    def get_queryset(self):
        queryset = Category.objects.all()
        return queryset

class CategoryDetailView(generics.ListAPIView):
    serializer_class = serializers.MusicListSerializer

    def get_queryset(self):
        queryset = Music.objects.published().filter(category__id=self.kwargs['pk'])
        return queryset


class InternationalMusicList(generics.ListAPIView):
    serializer_class = serializers.MusicListSerializer
    queryset = Music.objects.published().filter(type='International')

    
class UserFavoriteMusicView(generics.ListAPIView):
    serializer_class = serializers.MusicListSerializer

    def get_queryset(self):
        favorite_music_ids = FavoriteMusic.objects.filter(user__id=self.kwargs['pk']).values_list('music_id', flat=True)
        return Music.objects.filter(id__in=favorite_music_ids)
 

class UserAddFavoriteMusicView(generics.GenericAPIView):

    def post(self, request):
        music_pk = request.data['pk']
        music = get_object_or_404(Music, id=music_pk)
        try:
            like = FavoriteMusic.objects.get(music_id=request.data['pk'], user_id=request.user.id)
            like.delete()
            return Response({'status': False, 'result': 'unlike', 'count': music.favorite_musics.count()}, status=status.HTTP_204_NO_CONTENT)  
        except:
            FavoriteMusic.objects.create(user=request.user, music=music)
            return Response({'status': True, 'result': 'like', 'count': music.favorite_musics.count()}, status=status.HTTP_200_OK)


class MusicSearchView(generics.ListAPIView):
    queryset = Music.objects.published()
    serializer_class = serializers.MusicListSerializer
    filter_backends = [SearchFilter]
    search_fields = ['title']