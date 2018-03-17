from rest_framework.serializers import (
	ModelSerializer, 
	SerializerMethodField,
	)

from posts.models import Post


class PostCreateUpdateSerializer(ModelSerializer):
	class Meta:
		model = Post 
		fields = [
			'title',
			'content',
		]


class PostListSerializer(ModelSerializer):
	user = SerializerMethodField()
	class Meta:
		model = Post 
		fields = [
			'user',
			'id',
			'title',
			'slug',
			'content',
		]
	def get_user(self,obj):
		return str(obj.user.username)

class PostDetailSerializer(ModelSerializer):
	user = SerializerMethodField()
	image = SerializerMethodField()
	class Meta:
		model = Post 
		fields = [
			'title',
			'image',
			'user',
			'content',
		]
	def get_user(self,obj):
		return str(obj.user.username)

	def get_image(self,obj):
		try:
			image = obj.image.url
		except:
			image = None
		return image


"""
Way to serializer is working 


data = {
        "content": "new content",
        "title": "Yeahhh buddy",
    	"slug":"new-content",
	}

item = PostSerializer(data=data)
if item.is_valid():
	item.save()
else:
	print(item.errors)

"""
