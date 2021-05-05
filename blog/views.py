from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from .models import Post
from .forms import PostForm
from .serializers import PostSerializer
from rest_framework import status


# Create your views here.
@api_view(["GET", "POST"])
def api_post_list(request):
    if request.method == "GET":
        post_list = Post.objects.all()
        serializer = PostSerializer(post_list, many=True)
        return Response(serializer.data)
    elif request.method == "POST":
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            serializer.instance.publish()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "DELETE"])
def api_post_detail(request, *args, **kwargs):
    pk = kwargs['pk']
    try:
        post = Post.objects.get(pk=pk)
    except Post.DoesNotExist:
        return Response("Post is not present", status=status.HTTP_404_NOT_FOUND)
    if request.method == "GET":
        serializer = PostSerializer(post)
        return Response(serializer.data)
    elif request.method == "PUT":
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            serializer.instance.publish()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == "DELETE":
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


def post_details(request, **kwargs):
    pk = kwargs['pk']
    post = Post.objects.get(pk=pk)
    return render(request, 'blog/post_details.html', {'post': post})


def post_new(request, *args, **kwargs):
    if request.POST:
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.text = request.POST['text']
            post.title = request.POST['title']
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})


def post_edit(request, *args, **kwargs):
    pk = kwargs['pk']
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})


def post_list(request):
    posts = Post.objects.all()
    return render(request, 'blog/index.html', {"posts": posts})
