from rest_framework import filters
from content.models import UserPost,PostMedia

class CurrentUserFollowingFilterBackend(filters.BaseFilterBackend):

    def filter_queryset(self, request, queryset, view):
        followed_users =  [edge.to_user for edge in request.user.profile.following.all()]

        return queryset.filter(author__in = followed_users)