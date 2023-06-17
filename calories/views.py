from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from . import models
from django.views.decorators.csrf import csrf_exempt
import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

# Create your views here.


@login_required
def index(request):
    return render(request, "index.html")


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username", "")
        password = request.POST.get("password", "")

        user = authenticate(request, username=username, password=password)
        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(
                request,
                "store/login.html",
                {"message": "Invalid username and/or password."},
            )
    else:
        return render(request, "login.html")


@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register_view(request):
    if request.method == "POST":
        pass
    else:
        return render(request, "register.html")


def register_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(
                request, "register.html", {"message": "Passwords must match."}
            )

        # Attempt to create new user
        try:
            user = models.User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(
                request, "register.html", {"message": "Username already taken."}
            )
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "register.html")


# @csrf_exempt
# @login_required
# def set_calories(request):
#     if request.method != "POST":
#         return JsonResponse({"error": "POST request required."}, status=400)

#     data = json.loads(request.body)

#     user = models.User.objects.get(username=request.user)
#     new_calories = data.get("new_calories")
#     user.per_day = new_calories
#     user.save()
#     return JsonResponse({"message": "Calories updated successfully..."}, status=201)


class set_calories(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Handle POST request
        data = json.loads(request.body)
        print(data)

        user = models.User.objects.get(username=request.user)
        new_calories = data.get("new_calories")
        user.per_day = new_calories
        user.save()

        resp = {"message": "Calories updated successfully..."}
        return Response(resp)
