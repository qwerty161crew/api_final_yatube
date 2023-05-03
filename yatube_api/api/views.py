from rest_framework import filters, mixins, permissions, viewsets, pagination
from rest_framework.permissions import IsAuthenticated
from rest_framework import filters
from rest_framework.exceptions import NotAuthenticated, ValidationError

from django.shortcuts import get_object_or_404
from django.db.utils import IntegrityError

from posts.models import Post, Group, Follow
from api.serializers import (PostSerializer, GroupSerializer,
                             CommentSerializer, FollowSerializer)
from api.permissions import AuthorDeleteOnly


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (AuthorDeleteOnly, )
    pagination_class = pagination.LimitOffsetPagination

    def perform_create(self, serializer):
        if not self.request.user.is_authenticated:
            raise NotAuthenticated
        serializer.save(author=self.request.user)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (AuthorDeleteOnly, )
    pagination_class = pagination.LimitOffsetPagination


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (AuthorDeleteOnly, )
    pagination_class = pagination.LimitOffsetPagination

    def get_queryset(self):
        post = get_object_or_404(Post, pk=self.kwargs.get('post_id'))
        return post.comments.all()

    def perform_create(self, serializer):
        if not self.request.user.is_authenticated:
            raise NotAuthenticated
        serializer.save(author=self.request.user,
                        post=get_object_or_404(
                            Post, pk=self.kwargs.get('post_id')))


class FollowViewSet(mixins.CreateModelMixin,
                    mixins.ListModelMixin,
                    viewsets.GenericViewSet):
    serializer_class = FollowSerializer
    permission_classes = (IsAuthenticated, )
    pagination_class = pagination.LimitOffsetPagination
    queryset = Follow.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['following__username', 'user__username']

    def get_queryset(self):
        return self.request.user.follower.all()

    def perform_create(self, serializer):
        try:
            serializer.save(user=self.request.user)
        except IntegrityError as error:
            raise ValidationError(error)
