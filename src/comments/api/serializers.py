from rest_framework.serializers import (
	ModelSerializer, 
	SerializerMethodField,
	)

from comments.models import Comment



class CommentListSerializer(ModelSerializer):
	user = SerializerMethodField()
	class Meta:
		model = Comment 
		fields = [
			'user',
			'id',
			'content_type',
			'content',
		]
	def get_user(self,obj):
		return str(obj.user.username)

class CommentChildSerializer(ModelSerializer):
	user = SerializerMethodField()
	class Meta:
		model = Comment 
		fields = [
			'user',
			'id',
			'content',
		]
	def get_user(self,obj):
		return str(obj.user.username)

class CommentDetailSerializer(ModelSerializer):
	user = SerializerMethodField()
	replies = SerializerMethodField()
	class Meta:
		model = Comment 
		fields = [
			'user',
			'id',
			'content',
		]
	def get_user(self,obj):
		return str(obj.user.username)
