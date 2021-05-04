from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Post
from .forms import PostForm
from .serializers import PostSerializer


# Create your views here.

def home(request):
    tmpl_vars = {'form': PostForm()}
    return render(request, 'blog/index.html', tmpl_vars)


@api_view(['GET'])
def post_collection(request):
    if request.method == 'GET':
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)


@api_view(['GET'])
def post_element(request, pk):
    try:
        post = Post.objects.get(pk=pk)
    except Post.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = PostSerializer(post)
        return Response(serializer.data)


def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/index.html', {'posts': posts})


def post_detail(request, *args, **kwargs):
    pk = kwargs['pk']
    post = get_object_or_404(Post, pk=pk)
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
