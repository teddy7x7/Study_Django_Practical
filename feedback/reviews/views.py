from django.http import HttpResponseRedirect
from django.shortcuts import render

from .forms import ReviewForm

# Create your views here.

def review(request):
    ### Old ver.
    # if request.method == 'POST':
    #     entered_name = request.POST["username"]
    #     if entered_name == "":
    #         return render(request, "reviews/review.html", {
    #             "has_error": True
    #         })
    #     ## we tend to not return a page or send back html vode for a POST request, because it is meant to submit data to the server not to get come page.
    #     # return render(request, "reviews/thank_you.html")

    #     ## Therefore we typically do upon a POST request is instead of returning a rendered template, we redirect to a different url with a GET request, and that url will then render the template.
    #     return HttpResponseRedirect("/thank-you")
    # return render(request, "reviews/review.html", {
    #     "has_error": False
    # })
    
    ### New ver.
    if request.method == 'POST':
        form = ReviewForm(request.POST)

        if form.is_valid():
            print(form.cleaned_data)
            return HttpResponseRedirect("/thank-you")
        # if is invalid, send this form which has been validate(invalid) to the render function, and let the template generate hints of invalid inputs and preserve other valid inputs.

    else:
        # only create a new form when request.method == 'GET'
        form = ReviewForm()
    
    return render(request, "reviews/review.html", {
        "form": form
    })


def thank_you(request):
    return render(request, "reviews/thank_you.html")