from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_403_FORBIDDEN
from rest_framework.viewsets import ModelViewSet

from api.models import Follow, Group, Post, User
from api.permissions import IsAuthorOrReadOnly
from api.serializers import (
    CommentSerializer, FollowSerializer, GroupSerializer, PostSerializer,
)


class TextArticlesViewSet(ModelViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly)


class PostsViewSet(TextArticlesViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    filterset_fields = ('group',)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentsViewSet(TextArticlesViewSet):
    serializer_class = CommentSerializer

    def get_queryset(self):
        post = get_object_or_404(Post, id=self.kwargs.get('post_id'))
        return post.comments

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            post=get_object_or_404(Post, id=self.kwargs.get('post_id'))
        )


class FollowViewSet(ModelViewSet):
    serializer_class = FollowSerializer
    queryset = Follow.objects.all()
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filterset_fields = ('user',)
    search_fields = ('=user__username', '=following__username')

    def create(self, request, *args, **kwargs):
        following = request.POST.get('following')
        if not following:
            return super().create(request, *args, **kwargs)
        if request.user.username == following:
            return Response(
                status=HTTP_403_FORBIDDEN,
                data={'detail': 'It is forbidden to follow the own profile.'}
            )
        if Follow.objects.filter(
                user=request.user,
                following=get_object_or_404(
                    User,
                    username=following
                )
        ):
            return Response(
                status=HTTP_400_BAD_REQUEST,
                data={'detail': 'Such record already exists.'}
            )
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(
            user=self.request.user,
            following=get_object_or_404(
                User,
                username=self.request.POST.get('following')
            )
        )


class GroupViewSet(ModelViewSet):
    serializer_class = GroupSerializer
    queryset = Group.objects.all()

    def perform_create(self, serializer):
        serializer.save(
            title=self.request.POST.get('title'),
        )
