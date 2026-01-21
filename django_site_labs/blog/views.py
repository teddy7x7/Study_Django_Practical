from django.http import HttpResponse
from django.shortcuts import render
from datetime import date

posts = [
    {
        "slug": "hike-in-the-mountains",
        "image": "mountains.jpg",
        "author": "Teddy",
        "date": date(2026, 1, 21),
        "title": "Mountain Hiking",
        "excerpt": "Mountain Study new things just like climbing a mountain. Step by step, we reach new heights and gain new perspectives. Finally, we can enjoy the breathtaking view from the summit.",
        "content": """
            Quibusdam assumenda veritatis accusamus tempora tenetur quia qui autem, temporibus harum molestias modi adipisci tempore, suscipit adipisci aspernatur atque, quo quam veniam qui culpa vitae magnam voluptates, quibusdam laudantium obcaecati illo officiis non natus similique deserunt? 
        """
    },
    {
        "slug": "coding-coding",
        "image": "coding.jpg",
        "author": "Teddy",
        "date": date(2026, 1, 1),
        "title": "Coding",
        "excerpt": "coding Study new things just like climbing a mountain. Step by step, we reach new heights and gain new perspectives. Finally, we can enjoy the breathtaking view from the summit.",
        "content": """
            Quibusdam assumenda veritatis accusamus tempora tenetur quia qui autem, temporibus harum molestias modi adipisci tempore, suscipit adipisci aspernatur atque, quo quam veniam qui culpa vitae magnam voluptates, quibusdam laudantium obcaecati illo officiis non natus similique deserunt? Quia voluptas odit adipisci eum nam suscipit, alias adipisci quia consectetur officiis voluptatem dolores quisquam harum hic, ab veritatis molestiae consectetur nesciunt numquam officiis maxime nisi quis fugit. 
        """
    },
    {
        "slug": "coding-coding",
        "image": "coding.jpg",
        "author": "Teddy",
        "date": date(2026, 1, 12),
        "title": "Coding",
        "excerpt": "coding Study new things just like climbing a mountain. Step by step, we reach new heights and gain new perspectives. Finally, we can enjoy the breathtaking view from the summit.",
        "content": """
            Quia voluptas odit adipisci eum nam suscipit, alias adipisci quia consectetur officiis voluptatem dolores quisquam harum hic, ab veritatis molestiae consectetur nesciunt numquam officiis maxime nisi quis fugit. 
        """
    },
    {
        "slug": "woods-in-the-mountains",
        "image": "woods.jpg",
        "author": "Teddy",
        "date": date(2026, 1, 2),
        "title": "Wooooodsss",
        "excerpt": "Woooo Study new things just like climbing a mountain. Step by step, we reach new heights and gain new perspectives. Finally, we can enjoy the breathtaking view from the summit.",
        "content": """
            Quibusdam assumenda veritatis accusamus tempora tenetur quia qui autem, temporibus harum molestias modi adipisci tempore, suscipit adipisci aspernatur atque, quo quam veniam qui culpa vitae magnam voluptates, quibusdam laudantium obcaecati illo officiis non natus similique deserunt? 
            
            Quia voluptas odit adipisci eum nam suscipit, alias adipisci quia consectetur officiis voluptatem dolores quisquam harum hic, ab veritatis molestiae consectetur nesciunt numquam officiis maxime nisi quis fugit. 
        """
    },
]

def index(request):
    sorted_posts = sorted(posts, key=lambda post: post["date"])
    latest_posts = sorted_posts[-3:]
    return render(request, "blog/index.html", {
        "posts": latest_posts
    })

def posts_list(request):
    return render(request, "blog/posts_list.html", {
        "posts": posts
    })


def post_detail(request, slug):
    identified_post = next(post for post in posts if post['slug'] == slug)
    return render(request, "blog/post_detail.html", {
        "post": identified_post
    })
