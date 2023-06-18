from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError, transaction
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


class add_entry(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = json.loads(request.body)
        print(data)

        if not data.get("add_meal_name"):
            return JsonResponse({"message": "Empty entry not allowed..."}, status=400)

        new_entry = models.Entry(
            user=request.user,
            name=data.get("add_meal_name"),
            number=data.get("add_cal_num"),
        )

        new_entry.save()
        print(new_entry.serialize())
        resp = {"message": "Entry added successfully..."}
        return Response(resp)


class load_entries(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, sort_by):
        print(sort_by)

        if sort_by == "default":
            entries = models.Entry.objects.filter(user=request.user)

        # Return emails in reverse chronologial order
        entries = entries.order_by("-timestamp").all()
        return JsonResponse(
            [entry.serialize() for entry in entries], safe=False, status=200
        )

        return JsonResponse({"hello": "hello"}, status=200)


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
                "login.html",
                {"message": "Invalid username and/or password."},
            )
    else:
        return render(request, "login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("login"))


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

        user, created = models.User.objects.get_or_create(
            username=username, email=email
        )
        if created:
            user.set_password(password)
            user.save()
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(
                request, "register.html", {"message": "Username already taken."}
            )
    else:
        return render(request, "register.html")


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
