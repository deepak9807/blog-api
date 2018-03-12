# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from urllib import quote_plus  # Python 3+
from django.contrib.contenttypes.models import ContentType

from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.shortcuts import render, get_object_or_404
from django.http import Http404

# import the form.py form use to store the data in database
from .forms import PostForm
from comments.models import Comment
from comments.forms import CommentForm
from .utils import get_read_time
# Create your views here.

from .models import Post

def post_create(request):
    if not request.user.is_staff  or not request.user.is_superuser:
        raise Http404("Please Login.")
    form = PostForm(request.POST or None,request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        instance.user=request.user
        #message success
        messages.success(request, "Successfuly created new item")
        return HttpResponseRedirect(instance.get_absolute_url())
    # if request.method == "POST":
    #     print request.POST
    context = {
        "form": form,
    }
    return render(request,'post_form.html',context)

def post_detail(request, slug=None):
    #instance = Post.objects.gets(id=1) Thsi throw error when data  does not exit in database
    instance = get_object_or_404(Post, slug=slug)
    share_string = quote_plus(instance.slug)# this is create string show while share url

    comments = instance.comments # using costum model manager and commnet @property
    print(get_read_time(instance.get_markdown()))
    initial_data = {
        "content_type": instance.get_content_type,
        "object_id": instance.id
    }
    form    = CommentForm(request.POST or None, initial= initial_data)
    if form.is_valid():
        c_type = form.cleaned_data.get("content_type")
        content_type = ContentType.objects.get(model=c_type)
        obj_id = form.cleaned_data.get("object_id")
        content_data = form.cleaned_data.get("content")
        parent_obj =None
        try:
            parent_id = int(request.POST.get("parent_id"))
        except:
            parent_id = None
        if parent_id:
            parent_qs = Comment.objects.filter(id=parent_id)
            if parent_qs.exists() and parent_qs.count()==1:
                parent_obj = parent_qs.first()

        new_comment, created = Comment.objects.get_or_create(
                            user = request.user,
                            content_type = content_type,
                            object_id = obj_id,
                            content = content_data,
                            parent = parent_obj,
            )
        return HttpResponseRedirect(new_comment.content_object.get_absolute_url())
    else:
        print("form not valid")

    context = {
    "title": instance.title,
    "instance": instance,
    "share_string":share_string,
    "comments":comments,
    "comment_form":form,
    }
    return render(request,'post_detail.html',context)

def post_list(request):
    queryset_list =Post.objects.active()

    if request.user.is_staff:
        queryset_list = Post.objects.all()        

    query = request.GET.get('q')

    if query:
        queryset_list = queryset_list.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(user__first_name__icontains=query) |
            Q(user__last_name__icontains=query) 
            ).distinct()

    paginator = Paginator(queryset_list, 2) # Show 25 contacts per page
    page_request_var='page'
    page = request.GET.get(page_request_var)
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        #page is not integer
        queryset = paginator.page(1)
    except EmptyPage:
        queryset = paginator.page(paginator.num_pages)
    context = {
     "objects_list": queryset,
     "title": "List",
     "page_request_var": page_request_var
    }
    return render(request, "post_list.html", context)

def post_update(request, slug=None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404("Please Login.")

    instance = get_object_or_404(Post, slug=slug)
    form = PostForm(request.POST or None,request.FILES or None,instance=instance,)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        instance.user=request.user
        messages.success(request, "Successfuly created new item")
        return HttpResponseRedirect(instance.get_absolute_url())

    context = {
    "title": instance.title,
    "instance": instance,
    "form":form,
    }
    return render(request,'post_form.html',context)

def post_delete(request, id=None):
    instance = get_object_or_404(Post, id=id)
    instance.delete()
    #messages.success(request, "Successfuly deleted old item")
    return redirect("post:list")
