from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.urls import reverse
# Create your views here.

monthly_challenges = {
    "january": "Complete first django tutorial",
    "february": "Complete second django tutorial",
    "march": "complete first AI engineer tutorial",
    "april": "complete postgresql tutorial ",
    "may": "complete second AI engineer tutorial ",
    "june": "complete first unreal engine tutorial",
    "july": "complete second unreal engine tutorial",
    "august": "complete third unreal engine tutorial",
    "september": "complete fourth unreal engine tutorial",
    "october": "complete first animation tutorial",
    "november": "complete second animation tutorial",
    "december": "Start my first game development",
}


def index(request):
    list_items = ""
    months = list(monthly_challenges.keys())
    
    for month in months:
        month_path = reverse("month-challenge", args=[month])
        capitalized_month = month.capitalize()
        list_items += f"<li><a href = \"{month_path}\">{capitalized_month}</a></li>"

    response_data = f"<ul>{list_items}</ul>"
    return HttpResponse(response_data)


def monthly_challenge_by_number(request, month: int):
    try:
        months = list(monthly_challenges.keys())
        redirect_month = months[month - 1]
        # hard coded path is no good
        # return HttpResponseRedirect("/challenges/" + redirect_month)
        # use django.urls.reverse function and a named path with dynamic segment(ie. redirected_month) to dynamicly build path is better
        redirect_path = reverse("month-challenge", args=[redirect_month])
        return HttpResponseRedirect(redirect_path)
    except IndexError:
        return HttpResponseNotFound("This month is not supported!")


def monthly_challenge(request, month):
    # implementation 1
    # if month in monthly_challenges:
    #     return HttpResponse(monthly_challenges[month])
    # else:
    #     return HttpResponseNotFound("month not supported")

    # implementation 2
    # challenge_text = monthly_challenges.get(month)
    # if challenge_text:
    #     return HttpResponse(challenge_text)
    # else:
    #     return HttpResponseNotFound("This month is not supported!")

    # implementation 3
    try:
        challenge_text = monthly_challenges[month]
        response_data = f"<h1>{challenge_text}</h1>"
        return HttpResponse(response_data)
    except KeyError:
        return HttpResponseNotFound("<h1>This month is not supported!</h1>")
