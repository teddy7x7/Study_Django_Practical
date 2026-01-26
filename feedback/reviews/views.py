from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.

def review(request):
    if request.method == 'POST':
        entered_name = request.POST["username"]
        print(entered_name)

        ## we tend to not return a page or send back html vode for a POST request, because it is meant to submit data to the server not to get come page.
        # return render(request, "reviews/thank_you.html")

        ## Therefore we typically do upon a POST request is instead of returning a rendered template, we redirect to a different url with a GET request, and that url will then render the template.
        return HttpResponseRedirect("/thank-you")
    
    return render(request, "reviews/review.html")

def thank_you(request):
    return render(request, "reviews/thank_you.html")