# from django.contrib.auth.decorators import login_required
# from django.shortcuts import render, redirect
# from django.contrib.auth import authenticate, login, logout
# from django.http import HttpResponseRedirect, JsonResponse
# from django.urls import reverse
# from . import models
# from django.views.decorators.csrf import csrf_exempt
# import json
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework.authentication import TokenAuthentication
# from rest_framework.permissions import IsAuthenticated
# from django.core.paginator import Paginator
# from rest_framework.permissions import IsAuthenticated, BasePermission
# from rest_framework.authtoken.models import Token
# from django.db.models.functions import Lower

# # Create your views here.


# class CanAddUserPermission(BasePermission):
#     def has_permission(self, request, view):
#         return request.user.has_perm("calories.add_user")


# class add_entry(APIView):
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]

#     def post(self, request):
#         data = json.loads(request.body)
#         user = models.User.objects.get(username=request.user)
#         if not data.get("add_meal_name"):
#             return JsonResponse({"message": "Empty entry not allowed..."}, status=400)

#         new_entry = models.Entry(
#             user=user,
#             name=data.get("add_meal_name"),
#             number=data.get("add_cal_num"),
#             expected=int(data.get("add_cal_num")) < user.per_day,
#         )

#         new_entry.save()
#         resp = {"message": "Entry added successfully..."}
#         return Response(resp)


# class delete_entry(APIView):
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]

#     def delete(self, request):
#         entry_id = request.data.get("entry_id")
#         to_delete = models.Entry.objects.get(id=entry_id)
#         if entry_id and to_delete:
#             to_delete.delete()
#             return Response({"message": "Delete successful"}, status=204)


# class delete_user(APIView):
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated, CanAddUserPermission]

#     def delete(self, request):
#         user_id = request.data.get("user_id")
#         to_delete = models.User.objects.get(id=user_id)
#         to_delete.delete()
#         return Response({"message": "Delete successful"}, status=204)


# class edit_entry(APIView):
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]

#     def post(self, request):
#         data = json.loads(request.body)

#         if data.get("edit_entry_user") != request.user.id and not request.user.has_perm(
#             "calories.change_entry"
#         ):
#             return JsonResponse({"message": "Unauthorized..."}, status=400)

#         user = models.User.objects.get(username=request.user)
#         if not data.get("edit_meal_name"):
#             return JsonResponse({"message": "Empty entry not allowed..."}, status=400)

#         to_edit = models.Entry.objects.get(id=int(data.get("edit_id")))

#         to_edit.name = data.get("edit_meal_name")
#         to_edit.number = data.get("edit_cal_num")

#         to_edit.expected = float(data.get("edit_cal_num")) < user.per_day
#         to_edit.save()

#         resp = {"message": "Entry edited successfully..."}
#         return Response(resp)


# class edit_user(APIView):
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated, CanAddUserPermission]

#     def post(self, request):
#         data = json.loads(request.body)
#         user = models.User.objects.get(username=request.user)

#         to_edit = models.User.objects.get(id=float(data.get("user_id")))

#         to_edit.email = data.get("user_email")
#         to_edit.per_day = data.get("user_per_day")

#         to_edit.save()

#         resp = {"message": "User edited successfully..."}
#         return Response(resp)


# class load_entries(APIView):
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         sort_by = page_number = request.GET.get("sort_by")
#         user_id = request.GET.get("user_id")
#         if user_id:
#             if not request.user.has_perm("calories.add_entry"):
#                 return JsonResponse({"message": "Unauthorized..."}, status=400)

#             entries = models.Entry.objects.filter(user=int(user_id))
#         else:
#             entries = models.Entry.objects.filter(user=request.user)

#         if sort_by != "default":
#             entries = entries.order_by(sort_by).all()
#         else:
#             entries = entries.order_by("-timestamp").all()
#         ret_entries = {}

#         paginator = Paginator(entries, 10)

#         page_number = request.GET.get("page")
#         page_obj = paginator.get_page(page_number)

#         ret_entries["entries"] = [entry.serialize() for entry in page_obj.object_list]

#         pagination_data = {
#             "count": paginator.count,
#             "num_pages": paginator.num_pages,
#             "current_page": page_obj.number,
#             "has_previous": page_obj.has_previous(),
#             "has_next": page_obj.has_next(),
#         }

#         ret_entries["pagination"] = pagination_data

#         paginator_data = {
#             "page_range": list(paginator.page_range),
#             "per_page": paginator.per_page,
#         }
#         ret_entries["pagination"]["paginator"] = paginator_data
#         return JsonResponse(ret_entries, safe=False, status=200)


# class load_users(APIView):
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated, CanAddUserPermission]

#     def get(self, request):
#         ret_users = {}
#         sort_by = request.GET.get("sort_by")
#         users = models.User.objects.all()
#         if sort_by != "default":
#             users = users.order_by(sort_by).all()
#         else:
#             users = users.order_by("-id").all()
#         paginator = Paginator(users, 10)

#         page_number = request.GET.get("page")
#         page_obj = paginator.get_page(page_number)

#         ret_users["users"] = [user.serialize() for user in page_obj.object_list]

#         pagination_data = {
#             "count": paginator.count,
#             "num_pages": paginator.num_pages,
#             "current_page": page_obj.number,
#             "has_previous": page_obj.has_previous(),
#             "has_next": page_obj.has_next(),
#         }

#         ret_users["pagination"] = pagination_data

#         paginator_data = {
#             "page_range": list(paginator.page_range),
#             "per_page": paginator.per_page,
#         }
#         ret_users["pagination"]["paginator"] = paginator_data
#         return JsonResponse(ret_users, safe=False, status=200)


# @login_required
# def index(request):
#     return render(request, "index.html")


# def login_view(request):
#     if request.method == "POST":
#         username = request.POST.get("username", "")
#         password = request.POST.get("password", "")

#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             login(request, user)
#             return HttpResponseRedirect(reverse("index"))
#         else:
#             return render(
#                 request,
#                 "login.html",
#                 {"message": "Invalid username and/or password."},
#             )
#     else:
#         return render(request, "login.html")


# def logout_view(request):
#     logout(request)
#     return HttpResponseRedirect(reverse("login"))


# def register_view(request):
#     if request.method == "POST":
#         username = request.POST["username"].title()
#         email = request.POST["email"]

#         password = request.POST["password"]
#         confirmation = request.POST["confirmation"]
#         if password != confirmation:
#             return render(
#                 request, "register.html", {"message": "Passwords must match."}
#             )

#         user, created = models.User.objects.get_or_create(
#             username=username, email=email
#         )
#         if created:
#             user.set_password(password)
#             user.save()
#             Token.objects.get_or_create(user=user)
#             login(request, user)
#             return HttpResponseRedirect(reverse("index"))
#         else:
#             return render(
#                 request, "register.html", {"message": "Username already taken."}
#             )
#     else:
#         return render(request, "register.html")


# class set_calories(APIView):
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]

#     def post(self, request):
#         data = json.loads(request.body)
#         user = models.User.objects.get(username=request.user)
#         new_calories = data.get("new_calories")
#         user.per_day = new_calories
#         user.save()

#         resp = {"message": "Calories updated successfully..."}
#         return Response(resp)

# views.py

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
import json
from django.db import IntegrityError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, BasePermission
from django.core.paginator import Paginator
from rest_framework.authtoken.models import Token
from django.db.models.functions import Lower
from . import models


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
        resp = {"message": "Entry added successfully..."}
        return Response(resp)


class delete_entry(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        entry_id = request.data.get("entry_id")
        to_delete = models.Entry.objects.get(id=entry_id)

        if entry_id and to_delete:
            to_delete.delete()
            return Response({"message": "Delete successful"}, status=204)


class delete_user(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, CanAddUserPermission]

    def delete(self, request):
        user_id = request.data.get("user_id")
        to_delete = models.User.objects.get(id=user_id)
        to_delete.delete()
        return Response({"message": "Delete successful"}, status=204)


class edit_entry(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = json.loads(request.body)

        if data.get("edit_entry_user") != request.user.id and not request.user.has_perm(
            "calories.change_entry"
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

        if user_id:
            if not request.user.has_perm("calories.add_entry"):
                return JsonResponse({"message": "Unauthorized..."}, status=400)

            entries = models.Entry.objects.filter(user=int(user_id))
        else:
            entries = models.Entry.objects.filter(user=request.user)

        if sort_by != "default":
            entries = entries.order_by(sort_by).all()
        else:
            entries = entries.order_by("-timestamp").all()

        ret_entries = {}

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
        sort_by = request.GET.get("sort_by")

        users = models.User.objects.all()

        if sort_by != "default":
            users = users.order_by(sort_by).all()
        else:
            users = users.order_by("-id").all()

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


class set_calories(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = json.loads(request.body)
        user = models.User.objects.get(username=request.user)
        new_calories = data.get("new_calories")
        user.per_day = new_calories
        user.save()

        resp = {"message": "Calories updated successfully..."}
        return Response(resp)


@login_required
def index(request):
    return render(request, "index.html")


@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("login"))


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


def register_view(request):
    if request.method == "POST":
        username = request.POST.get("username", "")
        email = request.POST.get("email", "")
        password = request.POST.get("password", "")
        confirmation = request.POST.get("confirmation", "")

        # Ensure password matches confirmation
        if password != confirmation:
            return render(
                request,
                "register.html",
                {"message": "Passwords must match."},
            )

        # Attempt to create new user
        try:
            user = models.User.objects.create_user(
                username=username, email=email, password=password
            )
            Token.objects.get_or_create(user=user)
            user.save()
        except IntegrityError:
            return render(
                request,
                "register.html",
                {"message": "Username already taken."},
            )
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "register.html")
