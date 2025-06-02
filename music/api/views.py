from django.core.paginator import Paginator
from django.db.models import Count, Max, Min, Q
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.api.serializers import ArtistListSerializer, UserDetailSerializer
from accounts.models import Artist, User
from music.api import serializers
from music.models import (
    Category,
    ChooseMusicByCategory,
    FavoriteMusic,
    HomeSlider,
    IPAddress,
    Music,
)
from music.pagination import CustomPagination


# Home API Views
class PopularMusicListView(generics.ListAPIView):
    serializer_class = serializers.MusicListSerializer

    def get_queryset(self):
        queryset = (
            Music.objects.annotate(num_likes=Count("favorite_musics"))
            .filter(status=True)
            .order_by("-num_likes")[:10]
        )
        return queryset


class RecentMusicListView(generics.ListAPIView):
    serializer_class = serializers.MusicListSerializer

    def get_queryset(self):
        queryset = (
            Music.objects.published()
            .filter(type="Iranian")
            .order_by("-created_at")[:10]
        )
        return queryset


class MusicByCategoryListView(generics.ListAPIView):
    serializer_class = serializers.MusicByCategorySerializer

    def get_queryset(self):
        category_object = ChooseMusicByCategory.objects.last()
        if category_object is None:
            return Music.objects.none()
        else:
            queryset = (
                Music.objects.published()
                .filter(category__id=category_object.category.id)
                .order_by("-created_at")[:10]
            )
            return queryset

    def get_serializer_context(self):
        context = super().get_serializer_context()
        category_object = ChooseMusicByCategory.objects.last()
        if category_object is None:
            context["category_name"] = "None"
        else:
            context["category_name"] = category_object.category.title
        return context


class MusicByTrendCategoryListView(generics.ListAPIView):
    serializer_class = serializers.MusicListSerializer

    def get_queryset(self):
        queryset = (
            Music.objects.published()
            .filter(category__title="trend")
            .order_by("-created_at")[:10]
        )
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
        instance = (
            Music.objects.select_related("category")
            .prefetch_related("artist")
            .get(id=pk)
        )
        is_liked = instance.favorite_musics.filter(user=request.user).exists()
        next_music_id = self.get_next_music_id(instance)
        previous_music_id = self.get_previous_music_id(instance)
        related_music = instance.related_music()
        serializer = self.get_serializer(
            instance,
            context={
                "request": request,
                "is_liked": is_liked,
                "related_music": related_music,
                "skip_music": {
                    "next_music_id": next_music_id,
                    "previous_music_id": previous_music_id,
                },
            },
        )

        client_ip = self.get_client_ip(request)
        self.add_view_music(client_ip, instance)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def get_next_music_id(self, instance):
        return (
            Music.objects.filter(id__gt=instance.id, category=instance.category)
            .aggregate(Min("id"))
            .get("id__min")
        )

    def get_previous_music_id(self, instance):
        return (
            Music.objects.filter(id__lt=instance.id, category=instance.category)
            .aggregate(Max("id"))
            .get("id__max")
        )

    def get_client_ip(self, request):
        # The X-Forwarded-For header is often used to capture the original client IP
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0]
        else:
            ip = request.META.get("REMOTE_ADDR")

        try:
            ip_address = IPAddress.objects.get(ip_address=ip)
        except IPAddress.DoesNotExist:
            ip_address = IPAddress(ip_address=ip)
            ip_address.save()
        return ip_address

    def add_view_music(self, client_ip, instance):
        if client_ip not in instance.views.all():
            instance.views.add(client_ip)


class CateogryListView(generics.ListAPIView):
    serializer_class = serializers.CategoryListSerializer

    def get_queryset(self):
        queryset = Category.objects.all()
        return queryset


class CategoryDetailView(generics.ListAPIView):
    pagination_class = CustomPagination
    serializer_class = serializers.MusicListSerializer

    def get_queryset(self):
        queryset = Music.objects.published().filter(category__id=self.kwargs["pk"])
        return queryset


class InternationalMusicList(generics.ListAPIView):
    serializer_class = serializers.MusicListSerializer
    queryset = (
        Music.objects.published()
        .filter(type="International")
        .order_by("-created_at")[:10]
    )


class UserFavoriteMusicView(generics.ListAPIView):
    serializer_class = serializers.MusicListSerializer

    def get_queryset(self):
        favorite_music_ids = FavoriteMusic.objects.filter(
            user__id=self.kwargs["pk"]
        ).values_list("music_id", flat=True)
        return Music.objects.filter(id__in=favorite_music_ids)


@extend_schema(
    request=int,
    responses=dict,
)
class UserAddFavoriteMusicView(generics.GenericAPIView):
    def post(self, request):
        music_pk = request.data["pk"]
        music = get_object_or_404(Music, id=music_pk)
        try:
            like = FavoriteMusic.objects.get(
                music_id=request.data["pk"], user_id=request.user.id
            )
            like.delete()
            return Response({"status": False}, status=status.HTTP_204_NO_CONTENT)
        except:
            FavoriteMusic.objects.create(user=request.user, music=music)
            return Response({"status": True}, status=status.HTTP_200_OK)


class MusicSearchView(APIView):
    """
    View for search  in (music, artist, user) fields
    """

    def paginate_queryset(self, queryset, per_page, page_number):
        paginator = Paginator(queryset, per_page)
        page = paginator.get_page(page_number)
        return {
            "count": paginator.count,
            "next": page.next_page_number() if page.has_next() else None,
            "previous": page.previous_page_number() if page.has_previous() else None,
            "results": page,
        }

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="search",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description="Search term for music, artist, or user",
                required=True,
            ),
            OpenApiParameter(
                name="music_page",
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
                description="Page number for music results",
                default=1,
            ),
            OpenApiParameter(
                name="user_page",
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
                description="Page number for user results",
                default=1,
            ),
            OpenApiParameter(
                name="artist_page",
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
                description="Page number for artist results",
                default=1,
            ),
        ],
        responses={
            200: {
                "type": "object",
                "properties": {
                    "music": {
                        "type": "object",
                        "properties": {
                            "count": {"type": "integer"},
                            "next": {"type": "integer", "nullable": True},
                            "previous": {"type": "integer", "nullable": True},
                            "results": {
                                "type": "array",
                                "items": {"$ref": "#/components/schemas/MusicList"},
                            },
                        },
                    },
                    "user": {
                        "type": "object",
                        "properties": {
                            "count": {"type": "integer"},
                            "next": {"type": "integer", "nullable": True},
                            "previous": {"type": "integer", "nullable": True},
                            "results": {
                                "type": "array",
                                "items": {"$ref": "#/components/schemas/User"},
                            },
                        },
                    },
                    "artist": {
                        "type": "object",
                        "properties": {
                            "count": {"type": "integer"},
                            "next": {"type": "integer", "nullable": True},
                            "previous": {"type": "integer", "nullable": True},
                            "results": {
                                "type": "array",
                                "items": {"$ref": "#/components/schemas/ArtistList"},
                            },
                        },
                    },
                },
            },
            (200, "no_search"): {
                "type": "object",
                "properties": {
                    "result": {"type": "string", "example": "there is no content"}
                },
            },
        },
    )
    def get(self, request):
        search = request.query_params.get("search", None)
        if not search:
            return Response({"result": "there is no content"})

        music = (
            Music.objects.published()
            .filter(Q(title__icontains=search) | Q(artist__name__icontains=search))
            .distinct()
        )
        music_data = self.paginate_queryset(
            music, per_page=15, page_number=request.query_params.get("music_page", 1)
        )
        music_serializer = serializers.MusicListSerializer(
            instance=music_data["results"], context={"request": request}, many=True
        )

        users = User.objects.filter(username__icontains=search).exclude(
            id=request.user.id
        )
        user_data = self.paginate_queryset(
            users, per_page=15, page_number=request.query_params.get("user_page", 1)
        )
        user_serializer = UserDetailSerializer(
            instance=user_data["results"], many=True, context={"request": request}
        )

        artists = Artist.objects.filter(name__icontains=search)
        artist_data = self.paginate_queryset(
            artists, per_page=15, page_number=request.query_params.get("artist_page", 1)
        )
        artist_serializer = ArtistListSerializer(
            instance=artist_data["results"], many=True, context={"request": request}
        )

        response_data = {"music": music_data, "user": user_data, "artist": artist_data}

        response_data["music"]["results"] = music_serializer.data
        response_data["user"]["results"] = user_serializer.data
        response_data["artist"]["results"] = artist_serializer.data

        return Response(response_data)
