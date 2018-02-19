# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db.models.signals import pre_save


from django.db import models
from django.core.urlresolvers import reverse
from django.utils.text import slugify

# Create your models here.

#MVC models view controller
# define location of image where to upload_to and who it store
def upload_location(instance, filename):
    return "%s/%s" %(instance.id, filename)

# creating models for store the post of a users.
class Post(models.Model):
    image   = models.ImageField(upload_to= upload_location,
    null=True, blank=True,
    height_field="height_field",
    width_field="width_field")
    slug = models.SlugField(max_length = 120)
    height_field = models.IntegerField(default= 0)
    width_field = models.IntegerField(default= 0)
    # image   = models.FileField(null=True, blank=True)
    title   = models.CharField(max_length = 30)
    content = models.TextField()
    update  =  models.DateTimeField(auto_now = True, auto_now_add = False)
    timestamp  =  models.DateTimeField(auto_now = False, auto_now_add = True)

    #python2*
    def __unicode__(self):
        return self.title

    # python3.*
    def __str__(self):
        return self.title

# more dynamic the urls using reverse
    def get_absolute_url(self):
        #first parameter is name of url
        # return reverse("detail", kwargs={"id": self.id })
        # destinct multiple url name as same in different app then
        # we use namespace with url name
        return reverse("post:detail", kwargs={"slug": self.slug})

    class Meta:
        ordering=["-timestamp", "-update"]


def create_slug(instance, new_slug=None):
    slug = slugify(instance.title)
    if new_slug is not None:
        slug = new_slug
    qs = Post.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" %(slug,qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug

def pre_save_post_reciver(sender, instance, *arg, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)



pre_save.connect(pre_save_post_reciver, sender=Post)
