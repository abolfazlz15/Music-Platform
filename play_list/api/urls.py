from django.urls import path

from play_list.api import views

app_name = "playlist"
urlpatterns = [
    path("approved", views.ApprovedPlaylistView.as_view(), name="approved_playlist"),
    path(
        "approved/detail/<int:pk>",
        views.ApprovedPlaylistDetailView.as_view(),
        name="approved_detail_playlist",
    ),
    path("user/<int:pk>", views.UserPlayListView.as_view(), name="user_playlist"),
    path(
        "detail/<int:pk>",
        views.UserDetailPlayListView.as_view(),
        name="detail_playlist",
    ),
    path("add/", views.UserCreatePlayListView.as_view(), name="add_playlist"),
    path(
        "update/<int:pk>",
        views.UserUpdatePlayListView.as_view(),
        name="update_playlist",
    ),
    path("delete/<int:pk>", views.DeletePlayListView.as_view(), name="delete_playlist"),
    path(
        "add-music/<int:pk>/",
        views.PlaylistAddMusicView.as_view(),
        name="add_music_to_playlist",
    ),
    path(
        "remove-music/<int:pk>/",
        views.PlaylistRemoveMusicView.as_view(),
        name="remove_music_from_playlist",
    ),
]
