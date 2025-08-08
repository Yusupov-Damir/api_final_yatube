from django.shortcuts import get_object_or_404
from rest_framework import viewsets, filters, mixins
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated

from posts.models import Post, Comment, Group, Follow
from .serializers import PostSerializer, CommentSerializer, GroupSerializer, FollowSerializer
from .permissions import AuthorOrReadOnly


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (AuthorOrReadOnly,IsAuthenticatedOrReadOnly)
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        """При создании объекта заполняем поле author значением из request """
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (AuthorOrReadOnly, IsAuthenticatedOrReadOnly)

    def __get_post(self):
        """Взятие поста по переданному в запросе post_id"""
        return get_object_or_404(Post, pk=self.kwargs.get('post_id'))

    def get_queryset(self):
        """
        Возвращает queryset с комментариями к текущему посту, (вместо queryset = Comment.objects.all())
        """
        post = self.__get_post()
        return post.comments.all()  # post.comments — это как Comment.objects.filter(post='post_id')

    def perform_create(self, serializer):
        """При создании объекта заполняем поля author и post значениями из request """
        serializer.save(author=self.request.user, post=self.__get_post())


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class FollowViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = FollowSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = (filters.SearchFilter,)
    # Поиск по конкретному полю связанной модели, по полю username модели пользователя, связанной через поле following.
    search_fields = ('=following__username',)


    def get_queryset(self):
        """Возвращает queryset с подписчиками к текущему пользователю, (вместо queryset = Follow.objects.all())"""
        return self.request.user.follower.all()

    def perform_create(self, serializer):
        """ user берем из request - то есть кто сделал запрос. А following ожидаем в POST запросе """
        serializer.save(user=self.request.user)