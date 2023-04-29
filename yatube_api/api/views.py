from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .pagination import Pagination
from django_filters.rest_framework import DjangoFilterBackend

from posts.models import Post, Group, User, Follow
from api.serializers import PostSerializer, GroupSerializer, CommentSerializer, FollowSerializer
from api.permissions import AuthorDeleteOnly


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (AuthorDeleteOnly, )
    pagination_class = Pagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def list(self, request):
        # Note the use of `get_queryset()` instead of `self.queryset`
        queryset = self.get_queryset()
        serializer = PostSerializer(queryset, many=True)

        return Response(serializer.data)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (AuthorDeleteOnly, )
    pagination_class = Pagination

    def list(self, request):
        # Note the use of `get_queryset()` instead of `self.queryset`
        queryset = self.get_queryset()
        serializer = GroupSerializer(queryset, many=True)
        return Response(serializer.data)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (AuthorDeleteOnly, )
    pagination_class = Pagination

    def get_queryset(self):
        post = get_object_or_404(Post, pk=self.kwargs.get('post_id'))
        return post.comments.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user.username,
                        post=get_object_or_404(
                            Post, pk=self.kwargs.get('post_id')))


class FollowViewSet(viewsets.ModelViewSet):
    serializer_class = FollowSerializer
    permission_classes = (IsAuthenticated, )
    pagination_class = Pagination
    queryset = Follow.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('following', )
    

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, following=get_object_or_404(
            User, pk=self.kwargs.get('following_id')))
