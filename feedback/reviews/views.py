from typing import Any
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View
from django.views.generic.base import TemplateView

from .forms import ReviewForm
from .models import Review
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormView, CreateView

# Create your views here.


# class ReviewView(View):
#     def get(self, request):
#         form = ReviewForm()

#         return render(request, "reviews/review.html", {
#             "form": form
#         })

#     def post(self, request):
#         form = ReviewForm(request.POST)

#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect("/thank-you")

#         return render(request, "reviews/review.html", {
#             "form": form
#         })

# class ReviewView(FormView):
#     # which form class should be used to render the form in the template
#     form_class = ReviewForm
#     template_name = "reviews/review.html"
#     # must provide
#     success_url = "/thank-you"

#     def form_valid(self, form):
#         # since we have designate which form class to deal with
#         form.save()
#         # must return parent's function to let django do it's work
#         return super().form_valid(form)
    
class ReviewView(CreateView):
    # May no need a form class
    # form_class = ReviewForm 
    # just directly set the corresponding model to let django know how to create data, just like in the ListView
    model = Review

    # Or can set the form class here inorder to do more detail settings
    form_class = ReviewForm
    template_name = "reviews/review.html"
    success_url = "/thank-you"


# def review(request):
#     ### Old ver.
#     # if request.method == 'POST':
#     #     entered_name = request.POST["username"]
#     #     if entered_name == "":
#     #         return render(request, "reviews/review.html", {
#     #             "has_error": True
#     #         })
#     #     ## we tend to not return a page or send back html vode for a POST request, because it is meant to submit data to the server not to get come page.
#     #     # return render(request, "reviews/thank_you.html")

#     #     ## Therefore we typically do upon a POST request is instead of returning a rendered template, we redirect to a different url with a GET request, and that url will then render the template.
#     #     return HttpResponseRedirect("/thank-you")
#     # return render(request, "reviews/review.html", {
#     #     "has_error": False
#     # })

#     ### New ver.
#     if request.method == 'POST':
#         form = ReviewForm(request.POST)
#         ### save the Form class data
#         # if form.is_valid():
#         #     # print(form.cleaned_data)
#         #     review = Review(
#         #         user_name = form.cleaned_data['user_name'],
#         #         review_text = form.cleaned_data['review_text'],
#         #         rating = form.cleaned_data['rating']
#         #     )
#         #     review.save()
#         #     return HttpResponseRedirect("/thank-you")
#         # # if is invalid, send this form which has been validate(invalid) to the render function, and let the template generate hints of invalid inputs and preserve other valid inputs.

#         ### save the ModelForm class data
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect("/thank-you")

#     else:
#         # only create a new form when request.method == 'GET'
#         form = ReviewForm()

#     return render(request, "reviews/review.html", {
#         "form": form
#     })


# def thank_you(request):
#     return render(request, "reviews/thank_you.html")

# class ThankYouView(View):
#     def get(self, request):
#         return render(request, "reviews/thank_you.html")


# from django.views.generic.base import TemplateView
class ThankYouView(TemplateView):
    template_name = "reviews/thank_you.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # corresponding to the tag in thank_you.html template
        context["message"] = "This Works"
        return context

# class ReviewsListView(TemplateView):
#     template_name = "reviews/review_list.html"
    
#     def get_context_data(self, **kwargs: Any):
#         context = super().get_context_data(**kwargs)
#         reviews = Review.objects.all()
#         context["reviews"] = reviews 
#         return context
class ReviewsListView(ListView):
    template_name = "reviews/review_list.html"
    # a specific variable point to the model class where to fetch the list of data
    model = Review
    # reset the name of list exposed to the template from default name object_list to what we want, ig. "reviews"
    context_object_name = "reviews"

    # def get_queryset(self):
    #     base_query = super().get_queryset()
    #     data = base_query.filter(rating__gt=4)
    #     return data

# class SingleReviewView(TemplateView):
#     template_name = "reviews/single_review.html"

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         review_id = kwargs["id"]
#         selected_review = Review.objects.get(pk=review_id)
#         context["review"] = selected_review
#         return context

class SingleReviewView(DetailView):
    template_name = "reviews/single_review.html"
    # model which to fetch the single instance
    model = Review

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # in the DetailView class, self.object would return the automatically fetched model
        loaded_review = self.object
        request = self.request
        favorite_id = request.session["favorite_review"]
        context["is_favorite"] = favorite_id == str(loaded_review.id)
        return context
    



class AddFavoriteView(View):
    def post(self, request):
        review_id = request.POST["review_id"]
        fav_review = Review.objects.get(pk=review_id)
        ## wrong! we shall not to save a whole object to a session. We only save simple value in a session.
        # request.session["favorite_review"] = fav_review
        request.session["favorite_review"] = review_id
        return HttpResponseRedirect("/reviews/" + review_id)