# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from urllib import quote_plus  # Python 3+
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.shortcuts import render, get_object_or_404
from django.http import Http404

# import the form.py form use to store the data in database
from .forms import PostForm
# Create your views here.

from .models import Post

def post_create(request):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404("Please Login.")
    form = PostForm(request.POST or None,request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
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
    #instance = Post.objects.gets(id=1) Thsi throw wrror when data  does not exit in database
    instance = get_object_or_404(Post, slug=slug)
    share_string = quote_plus(instance.content)# this is create string show while share url
    context = {
    "title": instance.title,
    "instance": instance,
    "share_string":share_string
    }
    return render(request,'post_detail.html',context)

def post_list(request):
    queryset_list = Post.objects.all()
    paginator = Paginator(queryset_list, 5) # Show 25 contacts per page
    page_request_var='page'
    page = request.GET.get('page_request_var')
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
