from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):

        if request.method in permissions.SAFE_METHODS:
            return True

        return bool(
            request.user.is_authenticated and request.user.is_superuser or
            request.user.is_authenticated and obj.user == request.user
        )


class PlaylistSubscriber(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            if request.user.subscription.is_active:
                return True 
            else:
                self.message = 'Your subscription has expired'
                return request.user.playlists.count() < 3
        except:
            if request.user.playlists.count() >= 3:
                self.message = 'you cant make more palylist please use subscription'
                return False
            else:
                return True


class AddMusicToPlaylistSubscriber(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        print()
        try:
            if request.user.subscription.is_active:
                return True 
            else:
                self.message = 'Your subscription has expired'
                return obj.songs.count() < 3
        except:
            if obj.songs.count() >= 3:
                self.message = 'you cant add more msuic to playlist please use subscription'
                return False
            else:
                return True