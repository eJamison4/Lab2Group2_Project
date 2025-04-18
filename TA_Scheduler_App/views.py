from django.shortcuts import render  # , redirect
from django.views import View
from .models import User


# Create your views here.
class Login(View):
    def get(self, request):
        return render(request, "login.html", {})

    def post(self, request):
        username = request.POST["username"]
        password = request.POST["password"]

        if username.strip() == "" or password.strip() == "":  # do nothing if either field is empty
            return render(request, "login.html")
        print(username)
        print(password)
        return render(request, "login.html", {"message": "Either username or password is incorrect!"})
        # return redirect()


class Account(View):
    def get(self, request):
        # session_user = request.session["username"]
        account_set = list(map(str, User.objects.all()))
        # session_auth = map(str, User.objects.filter(username=session_user))
        # print(session_auth)
        return render(request, "accounts.html", {"accounts": account_set})

    def post(self, request):
        ...


class Courses(View):
    def get(self, request):
        return render(request, "courses.html", {})

    def post(self, request):
        ...


class Feedback(View):
    def get(self, request):
        return render(request, "feedback.html", {})

    def post(self, request):
        ...


class MyAccount(View):
    def get(self, request):
        return render(request, "my_acc_info.html", {})

    def post(self, request):
        ...


class SendNotifs(View):
    def get(self, request):
        return render(request, "send_notifs.html", {})

    def post(self, request):
        ...


# class Dashboard(View):
#     def get(self, request):
#         return render(request, "dashboard.html", {})
#
#     def post(self, request):
#         ...
