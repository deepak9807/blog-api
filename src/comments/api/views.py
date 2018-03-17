from __future__ import unicode_literals

from django.db.models import Q
from rest_framework.filters import (
	SearchFilter,
	OrderingFilter,
	)
#from django_filters.rest_framework import DjangoFilterBackend, SearchFilter

# custom pagination 
from posts.api.paginations import PostLimitOffsetPagination, PostPageNumberPagination

from rest_framework.permissions import (
	AllowAny,
	IsAuthenticated,
	IsAdminUser,
	IsAuthenticatedOrReadOnly
	)
from rest_framework.generics import (
	DestroyAPIView,
	ListAPIView, 
	UpdateAPIView,
	RetrieveAPIView,
	RetrieveUpdateAPIView,
	CreateAPIView,

	)
from posts.api.permissions import IsOwnerOrReadOnly
from comments.models import Comment 
from .serializers import (
	CommentListSerializer,)

# class PostCreateUpdateAPIView(CreateAPIView):
# 	queryset = Post.objects.all()
# 	serializer_class = PostCreateUpdateSerializer
# 	#update user associtated with post
# 	permission_classes = [IsAuthenticated]
# 	def perform_create(self, serializer):
# 		serializer.save(user = self.request.user)


class CommentDetailAPIView(RetrieveAPIView):
	queryset = Comment.objects.all()
	serializer_class = CommentListSerializer


# class PostDeleteAPIView(DestroyAPIView):
# 	queryset = Post.objects.all()
# 	serializer_class = PostDetailSerializer
# 	lookup_field = 'slug'


class CommentListAPIView(ListAPIView):
	
	serializer_class = CommentListSerializer
	filter_backends = [SearchFilter,]
	search_fields = ['title','content','user__first_name']
	# pagination stuf
	pagination_class = PostPageNumberPagination

	def get_queryset(self,*args, **Kwargs):
		queryset_list = Comment.objects.all()
		query = self.request.GET.get("q")
		if query:
			queryset_list = queryset_list.filter(
				Q(content__icontains=query) |
				Q(user__first_name__icontains=query) |
				Q(user__last_name__icontains=query) 
				).distinct()
		return queryset_list

