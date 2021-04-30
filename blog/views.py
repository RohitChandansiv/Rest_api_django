from django.shortcuts import render, get_object_or_404
from django.utils import timezone

from .models import Post


# Create your views here.

def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/index.html', {'posts': posts})


def post_detail(request, *args, **kwargs):
    pk = kwargs['pk']
    post = get_object_or_404(Post, pk=pk)
    return render(request,'blog/post_details.html',{'post':post})
