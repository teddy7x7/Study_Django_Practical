from django.urls import path
from . import views

urlpatterns = [
    # path("", views.review),
    path("", views.ReviewView.as_view()),
    # path("thank-you", views.thank_you)
    path("thank-you", views.ThankYouView.as_view())
]