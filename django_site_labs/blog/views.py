from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.


def index(request):
    return render(request, "blog/index.html")

def posts_list(request):
    return render(request, "blog/posts_list.html")


def post_detail(request, slug):
    return render(request, "blog/post_detail.html", {"slug": slug})
