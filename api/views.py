from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from api.models import Follow, Group, Post, User
from api.permissions import FollowingNonSelfProfile, IsAuthorOrReadOnly
from api.serializers import (
    CommentSerializer, FollowSerializer, GroupSerializer, PostSerializer,
)


class PostsViewSet(ModelViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly)
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('group',)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentsViewSet(ModelViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly)
    serializer_class = CommentSerializer

    def get_queryset(self):
        post = get_object_or_404(Post, id=self.kwargs.get('post_id'))
        return post.comments.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            post=get_object_or_404(Post, id=self.kwargs.get('post_id'))
        )


class FollowViewSet(GenericViewSet, CreateModelMixin, ListModelMixin):
    permission_classes = (IsAuthenticatedOrReadOnly, FollowingNonSelfProfile)
    serializer_class = FollowSerializer
    queryset = Follow.objects.all()
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filterset_fields = ('user',)
    search_fields = ('=user__username', '=following__username')

    def perform_create(self, serializer):
        serializer.save(
            user=self.request.user,
            following=get_object_or_404(
                User,
                username=self.request.POST.get('following')
            )
        )


class GroupViewSet(GenericViewSet, CreateModelMixin, ListModelMixin):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = GroupSerializer
    queryset = Group.objects.all()
