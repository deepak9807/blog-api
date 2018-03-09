# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.conf import settings
# Create your models here.
#from posts.models import Post
# Generic Foreign Key relation 
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse

# Comment Model manager

class CommentManeger(models.Manager):
	def all(self):
		return super(CommentManeger,self).filter(parent=None)
	def instance_of_comment(self, instance):
		content_type = ContentType.objects.get_for_model(instance.__class__)
		obj_id   = instance.id
		qs = super(CommentManeger, self).filter(content_type = content_type, object_id= obj_id).filter(parent=None)
		return qs

class Comment(models.Model):

	user 		= models.ForeignKey(settings.AUTH_USER_MODEL,default=1)
	#post        = models.ForeignKey(Post)

	#Generic relation 
	content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
	object_id = models.PositiveIntegerField()
	content_object = GenericForeignKey('content_type', 'object_id')
	parent  = models.ForeignKey('self',blank=True,null=True)


	content 	= models.TextField()
	timestamp 	= models.DateTimeField(auto_now_add=True)

	objects = CommentManeger()

	class Meta:
		ordering =["-timestamp"]


	def get_absolute_url(self):
		return reverse("comments:thread",kwargs={"id":self.id})
		
	def __str__(self):
		return str(self.user.username)

	def __unique__(self):
		return str(self.user.username)

		# Children used for reply a comment
	def children(self):
		return Comment.objects.filter(parent=self)

	@property
	def is_parent(self):
		if self.parent is not None:
			return False
		return True
