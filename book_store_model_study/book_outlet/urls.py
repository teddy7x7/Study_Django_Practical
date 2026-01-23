from django.urls import path
from . import views

app_name = "book_outlet"

urlpatterns = [
    path("", views.index), 
    # path("<int:id>", views.book_detail, name="book_detail")
    path("<slug:slug>", views.book_detail, name="book_detail")
]
