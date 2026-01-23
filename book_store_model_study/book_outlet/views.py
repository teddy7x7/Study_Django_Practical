from django.shortcuts import render, get_object_or_404
from .models import Book
from django.http import Http404
# aggregate functions
from django.db.models import Avg, Max, Min

# Create your views here.

def index(request):
    # books = Book.objects.all()
    # add '-' to ger decending order
    books = Book.objects.all().order_by("-rating")

    # aggregate functions
    num_books = books.count()
    avg_rating = books.aggregate(Avg("rating"))

    return render(request, "book_outlet/index.html", {
        "books": books,
        "total_number_of_books": num_books,
        "averaging_rating": avg_rating,
    })

# def book_detail(request, id):
#     # #  implementation 1
#     # try:
#     #     book = Book.objects.get(pk=id)
#     # except:
#     #     raise Http404()

#     #  implementation 2
#     book = get_object_or_404(Book, id=id)

#     return render(request, "book_outlet/book_detail.html", {
#         "title": book.title,
#         "author": book.author,
#         "rating": book.rating,
#         "is_bestseller": book.is_bestselling
#     })

def book_detail(request, slug):

    book = get_object_or_404(Book, slug=slug)

    return render(request, "book_outlet/book_detail.html", {
        "title": book.title,
        "author": book.author,
        "rating": book.rating,
        "is_bestseller": book.is_bestselling
    })