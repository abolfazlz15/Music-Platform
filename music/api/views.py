from django.db.models import Count, Q
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response
from django.db.models import Max, Min
from accounts.api.serializers import ArtistListSerializer, UserSerializer
from accounts.models import Artist, User
from music.api import serializers
from music.models import (Category, ChooseMusicByCategory, FavoriteMusic,
                          HomeSlider, Music)


# Home API Views
class PopularMusicListView(generics.ListAPIView):
    serializer_class = serializers.MusicListSerializer

    def get_queryset(self):
        queryset = Music.objects.annotate(num_likes=Count('favorite_musics')).filter(status=True).order_by(
            '-num_likes')[:10]
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
    serializer_class = serializers.SliderHomePageSerializer

    def get_queryset(self):
        queryset = HomeSlider.objects.filter(status=True)
        return queryset


# End Home API Views
class MusicDetailView(generics.GenericAPIView):
    serializer_class = serializers.MusicDetailSerializer

    def get(self, request, pk):
        instance = Music.objects.select_related('category').prefetch_related('artist').get(id=pk)
        is_liked = instance.favorite_musics.filter(user=request.user).exists()
        next_music_id = self.get_next_music_id(instance)
        previous_music_id = self.get_previous_music_id(instance)
        related_music = instance.related_music()
        serializer = self.get_serializer(instance, context={'request': request, 'is_liked': is_liked,
                                                            'related_music': related_music,
                                                            'skip_music': {'next_music_id': next_music_id,
                                                                           'previous_music_id': previous_music_id}})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get_next_music_id(self, instance):
        return Music.objects.filter(id__gt=instance.id, category=instance.category).aggregate(Min('id')).get('id__min')

    def get_previous_music_id(self, instance):
        return Music.objects.filter(id__lt=instance.id, category=instance.category).aggregate(Max('id')).get('id__max')


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
            return Response({'status': False, 'result': 'unlike'}, status=status.HTTP_204_NO_CONTENT)
        except:
            FavoriteMusic.objects.create(user=request.user, music=music)
            return Response({'status': True, 'result': 'like'}, status=status.HTTP_200_OK)


class MusicSearchView(generics.GenericAPIView):
    def get(self, request):
        search = request.query_params.get('search', None)
        if search:
            # music 
            music = Music.objects.published().filter(
                Q(title__icontains=search) |
                Q(artist__name__icontains=search)
            ).distinct()
            music_serializer = serializers.MusicListSerializer(instance=music, context={'request': request}, many=True)

            # user
            user = User.objects.filter(username__icontains=search)
            user_serializer = UserSerializer(instance=user, many=True, context={'request': request})

            # artist
            artist = Artist.objects.filter(name__icontains=search)
            artist_serializer = ArtistListSerializer(instance=artist, many=True, context={'request': request})
            return Response(
                {'music': music_serializer.data, 'user': user_serializer.data, 'artist': artist_serializer.data})
        else:
            return Response({'result': 'there is no content'})
