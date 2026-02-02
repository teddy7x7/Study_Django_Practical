from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.views import View

from datetime import date

from .models import Post
from .forms import CommentForm

# old ver
# posts = [
#     {
#         "slug": "hike-in-the-mountains",
#         "image": "mountains.jpg",
#         "author": "Teddy",
#         "date": date(2026, 1, 21),
#         "title": "Mountain Hiking",
#         "excerpt": "Mountain Study new things just like climbing a mountain. Step by step, we reach new heights and gain new perspectives. Finally, we can enjoy the breathtaking view from the summit.",
#         "content": """
#             Quibusdam assumenda veritatis accusamus tempora tenetur quia qui autem, temporibus harum molestias modi adipisci tempore, suscipit adipisci aspernatur atque, quo quam veniam qui culpa vitae magnam voluptates, quibusdam laudantium obcaecati illo officiis non natus similique deserunt? 
#         """
#     },
#     {
#         "slug": "coding-coding",
#         "image": "coding.jpg",
#         "author": "Teddy",
#         "date": date(2026, 1, 1),
#         "title": "Coding",
#         "excerpt": "coding Study new things just like climbing a mountain. Step by step, we reach new heights and gain new perspectives. Finally, we can enjoy the breathtaking view from the summit.",
#         "content": """
#             Quibusdam assumenda veritatis accusamus tempora tenetur quia qui autem, temporibus harum molestias modi adipisci tempore, suscipit adipisci aspernatur atque, quo quam veniam qui culpa vitae magnam voluptates, quibusdam laudantium obcaecati illo officiis non natus similique deserunt? Quia voluptas odit adipisci eum nam suscipit, alias adipisci quia consectetur officiis voluptatem dolores quisquam harum hic, ab veritatis molestiae consectetur nesciunt numquam officiis maxime nisi quis fugit. 
#         """
#     },
#     {
#         "slug": "coding-coding",
#         "image": "coding.jpg",
#         "author": "Teddy",
#         "date": date(2026, 1, 12),
#         "title": "Coding",
#         "excerpt": "coding Study new things just like climbing a mountain. Step by step, we reach new heights and gain new perspectives. Finally, we can enjoy the breathtaking view from the summit.",
#         "content": """
#             Quia voluptas odit adipisci eum nam suscipit, alias adipisci quia consectetur officiis voluptatem dolores quisquam harum hic, ab veritatis molestiae consectetur nesciunt numquam officiis maxime nisi quis fugit. 
#         """
#     },
#     {
#         "slug": "woods-in-the-mountains",
#         "image": "woods.jpg",
#         "author": "Teddy",
#         "date": date(2026, 1, 2),
#         "title": "Wooooodsss",
#         "excerpt": "Woooo Study new things just like climbing a mountain. Step by step, we reach new heights and gain new perspectives. Finally, we can enjoy the breathtaking view from the summit.",
#         "content": """
#             Quibusdam assumenda veritatis accusamus tempora tenetur quia qui autem, temporibus harum molestias modi adipisci tempore, suscipit adipisci aspernatur atque, quo quam veniam qui culpa vitae magnam voluptates, quibusdam laudantium obcaecati illo officiis non natus similique deserunt? 
            
#             Quia voluptas odit adipisci eum nam suscipit, alias adipisci quia consectetur officiis voluptatem dolores quisquam harum hic, ab veritatis molestiae consectetur nesciunt numquam officiis maxime nisi quis fugit. 
#         """
#     },
# ]

# def index(request):
#     # old ver
#     # sorted_posts = sorted(posts, key=lambda post: post["date"])
#     # latest_posts = sorted_posts[-3:]

#     # new ver
#     # django would convert this into a sql commend rather than fetch all the data from the database 
#     latest_posts = Post.objects.all().order_by("-date")[:3] 
#     return render(request, "blog/index.html", {
#         "posts": latest_posts
#     })
class IndexView(ListView):
    template_name = "blog/index.html"
    model = Post
    ordering = ["-date"]
    context_object_name = "posts"

    def get_queryset(self):
        queryset = super().get_queryset()
        data = queryset[:3]
        return data

# def posts_list(request):
#     posts = Post.objects.all().order_by("-date")
#     return render(request, "blog/posts_list.html", {
#         "posts": posts
#     })

class PostsListView(ListView):
    template_name = "blog/posts_list.html"
    model = Post
    ordering = ["-date"]
    context_object_name = "posts"


# def post_detail(request, slug):
#     # identified_post = next(post for post in posts if post['slug'] == slug)
#     # identified_post = Post.objects.get(slug=slug)
#     identified_post = get_object_or_404(Post, slug=slug)
#     return render(request, "blog/post_detail.html", {
#         "post": identified_post,
#         "post_tags": identified_post.tags.all()
#     })

# class PostDetailView(DetailView):
#     template_name = "blog/post_detail.html"
#     model = Post

#     def get_context_data(self, **kwargs):
#         context =  super().get_context_data(**kwargs)
#         context["post_tags"] = self.object.tags.all()
#         context["comment_form"] = CommentForm()
#         return context

class PostDetailView(View):
    def get(self, request, slug):
        post = Post.objects.get(slug=slug)
        context = {
          "post": post,
          "post_tags": post.tags.all(),
          "comment_form": CommentForm()
        }
        return render(request, "blog/post_detail.html", context)

    def post(self, request, slug):
        comment_form = CommentForm(request.POST)
        post = Post.objects.get(slug=slug)

        if comment_form.is_valid():
          comment = comment_form.save(commit=False)
          comment.post = post
          comment.save()
          
        # be careful with the namespace of the url name
          return HttpResponseRedirect(reverse("blog:post_detail", args=[slug]))

        context = {
          "post": post,
          "post_tags": post.tags.all(),
          "comment_form": comment_form
        }
        return render(request, "blog/post_detail.html", context)
