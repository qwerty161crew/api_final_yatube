from rest_framework import viewsets, pagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import filters
from rest_framework.exceptions import NotAuthenticated, ValidationError
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

    def list(self, request):
        # Note the use of `get_queryset()` instead of `self.queryset`
        queryset = self.get_queryset()
        serializer = GroupSerializer(queryset, many=True)
        return Response(serializer.data)


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


class FollowViewSet(viewsets.ModelViewSet):
    serializer_class = FollowSerializer
    permission_classes = (IsAuthenticated, )
    pagination_class = pagination.LimitOffsetPagination
    queryset = Follow.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['following__username', 'user__username']

    def get_queryset(self):
        return self.request.user.follower.all()

    def perform_create(self, serializer):
        if not serializer.is_valid() or (
                self.request.user ==
                serializer.validated_data['following']):
            raise ValidationError(
                'нельзя подписаться на самого себя')
        try:
            serializer.save(user=self.request.user)
        except IntegrityError as error:
            raise ValidationError(error)
