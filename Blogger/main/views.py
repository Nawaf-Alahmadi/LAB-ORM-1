from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from .models import Post, Category

# Create your views here.

# Home Page
def home_view(request:HttpRequest):
  if "filter" in request.GET and request.GET['filter'] == 'published':
    posts = Post.objects.filter(is_published__contains = 1)
  elif "filter" in request.GET and request.GET['filter'] == 'date':
    posts = Post.objects.all().order_by('-published_at')
  else:
    posts = Post.objects.all()
  return render(request, "main/index.html", {"posts":posts})

# Create page
def create_view(request:HttpRequest):
  all_categories = Category.objects.all()
  if request.method == "POST":
        if request.POST["published_at"] == "" and request.POST["is_published"] == "":
          new_post = Post(title= request.POST['title'], content= request.POST['content'], post = request.FILES['post'])
          new_post.save()
          new_post.categories.set(request.POST.getlist("categories"))
          # request.POST['categories']
        elif request.POST["published_at"] == "":
          new_post = Post(title= request.POST['title'], content= request.POST['content'], is_published= request.POST['is_published'], post = request.FILES['post'])
          new_post.save()
        elif request.POST["is_published"] == "":
          new_post = Post(title= request.POST['title'], content= request.POST['content'], published_at= request.POST['published_at'], post = request.FILES['post'])
          new_post.save()
        else:
          new_post = Post(title= request.POST['title'], content= request.POST['content'], published_at= request.POST['published_at'], post = request.FILES['post'])
          new_post.save()
        return redirect("main:Home")
  return render(request, "main/create_post.html", {'all_categories':all_categories})

# View 
def detail_view(request:HttpRequest, post_id):
  post = Post.objects.get(pk = post_id)
  print(post.categories.name)
  return render(request, "main/details.html", {"post":post})

# Modify
def modify_view(request:HttpRequest, post_id):
  post = Post.objects.get(pk = post_id)
  if request.method == "POST":
    post.title = request.POST['title']
    post.content = request.POST['content']
    post.is_published = request.POST['is_published']
    post.published_at = request.POST['published_at']
    post.save()
  return render(request, "main/modify.html", {"post":post})

# Delete
def delete_view(request:HttpRequest, post_id):
  post = Post.objects.get(pk = post_id)
  post.delete()
  return redirect("main:Home")

# Search
def search_view(request:HttpRequest):
  # and request.GET["search"] != ""
  if "search" in request.GET and request.GET["search"] != "":
    posts = Post.objects.filter(title__contains = request.GET["search"])
    return render(request,"main/search.html", {"posts":posts})
  else:
    return redirect("main:Home")
