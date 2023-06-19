from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout

# from django.db import IntegrityError, transaction
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from . import models
from django.views.decorators.csrf import csrf_exempt
import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.core.paginator import Paginator
from rest_framework.permissions import IsAuthenticated, BasePermission
from rest_framework.authtoken.models import Token

# Create your views here.


class CanAddUserPermission(BasePermission):
    def has_permission(self, request, view):
        # Check if the user has the 'can_add_user' permission on the model
        return request.user.has_perm("calories.add_user")


class add_entry(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = json.loads(request.body)
        user = models.User.objects.get(username=request.user)
        if not data.get("add_meal_name"):
            return JsonResponse({"message": "Empty entry not allowed..."}, status=400)

        new_entry = models.Entry(
            user=user,
            name=data.get("add_meal_name"),
            number=data.get("add_cal_num"),
            expected=int(data.get("add_cal_num")) < user.per_day,
        )

        new_entry.save()
        print(new_entry.serialize())
        resp = {"message": "Entry added successfully..."}
        return Response(resp)


class delete_entry(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        entry_id = request.data.get("entry_id")
        print(entry_id)
        to_delete = models.Entry.objects.get(id=entry_id)
        if entry_id and to_delete:
            to_delete.delete()
            return Response({"message": "Delete successful"}, status=204)


class delete_user(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, CanAddUserPermission]

    def delete(self, request):
        user_id = request.data.get("user_id")
        print(user_id)
        to_delete = models.User.objects.get(id=user_id)
        to_delete.delete()
        return Response({"message": "Delete successful"}, status=204)


class edit_entry(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = json.loads(request.body)
        print(data)

        if data.user_id != request.user.id and not request.user.has_perm(
            "calories.edit_user"
        ):
            return JsonResponse({"message": "Unauthorized..."}, status=400)

        user = models.User.objects.get(username=request.user)
        if not data.get("edit_meal_name"):
            return JsonResponse({"message": "Empty entry not allowed..."}, status=400)

        to_edit = models.Entry.objects.get(id=int(data.get("edit_id")))

        to_edit.name = data.get("edit_meal_name")
        to_edit.number = data.get("edit_cal_num")

        to_edit.expected = float(data.get("edit_cal_num")) < user.per_day
        to_edit.save()

        resp = {"message": "Entry edited successfully..."}
        return Response(resp)


class edit_user(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, CanAddUserPermission]

    def post(self, request):
        data = json.loads(request.body)
        print(data)
        user = models.User.objects.get(username=request.user)

        to_edit = models.User.objects.get(id=float(data.get("user_id")))

        to_edit.email = data.get("user_email")
        to_edit.per_day = data.get("user_per_day")

        to_edit.save()

        resp = {"message": "User edited successfully..."}
        return Response(resp)


class load_entries(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        sort_by = page_number = request.GET.get("sort_by")

        user_id = request.GET.get("user_id")
        print(user_id)
        if user_id:
            if not request.user.has_perm("calories.add_entry"):
                return JsonResponse({"message": "Unauthorized..."}, status=400)

            entries = models.Entry.objects.filter(user=int(user_id))
        else:
            entries = models.Entry.objects.filter(user=request.user)

        # Return emails in reverse chronologial order
        ret_entries = {}
        entries = entries.order_by("-timestamp").all()
        paginator = Paginator(entries, 10)

        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        ret_entries["entries"] = [entry.serialize() for entry in page_obj.object_list]

        pagination_data = {
            "count": paginator.count,
            "num_pages": paginator.num_pages,
            "current_page": page_obj.number,
            "has_previous": page_obj.has_previous(),
            "has_next": page_obj.has_next(),
        }

        ret_entries["pagination"] = pagination_data

        paginator_data = {
            "page_range": list(paginator.page_range),
            "per_page": paginator.per_page,
        }
        ret_entries["pagination"]["paginator"] = paginator_data
        return JsonResponse(ret_entries, safe=False, status=200)


class load_users(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, CanAddUserPermission]

    def get(self, request):
        ret_users = {}
        users = models.User.objects.all().order_by("id")
        paginator = Paginator(users, 10)

        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        ret_users["users"] = [user.serialize() for user in page_obj.object_list]

        pagination_data = {
            "count": paginator.count,
            "num_pages": paginator.num_pages,
            "current_page": page_obj.number,
            "has_previous": page_obj.has_previous(),
            "has_next": page_obj.has_next(),
        }

        ret_users["pagination"] = pagination_data

        paginator_data = {
            "page_range": list(paginator.page_range),
            "per_page": paginator.per_page,
        }
        ret_users["pagination"]["paginator"] = paginator_data
        return JsonResponse(ret_users, safe=False, status=200)


@login_required
def index(request):
    print(request.user.id)
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
            Token.objects.get_or_create(user=user)
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
        user = models.User.objects.get(username=request.user)
        new_calories = data.get("new_calories")
        user.per_day = new_calories
        user.save()

        resp = {"message": "Calories updated successfully..."}
        return Response(resp)
