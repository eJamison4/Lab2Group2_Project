from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render  # , redirect
from django.views import View
from django.urls import re_path
from TA_Scheduler_App.models import User
from TA_Scheduler_App.account_features import AccountFeatures



# Create your views here.
class Login(View):
    def get(self, request):
        return render(request, "login.html", {})

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']

        if username.strip() == "" or password.strip() == "":  # do nothing if either field is empty
            return render(request, "login.html")
        print(username)
        print(password)
        return render(
            request,
            "login.html",
            {"message": "Either username or password is incorrect!"}
        )
        # return redirect()


class Account(View):
    def get(self, request):
        users = User.objects.all()
        return render(request, "accounts.html", {"users": users})

    def post(self, request):
        action = request.POST['action']

        if action == "create":

            AccountFeatures.create_user(username=request.POST['username'], password=request.POST['password']
                                        , user_email=request.POST['userEmail'], first_name=request.POST['firstName'],
                                        last_name=request.POST['lastName'], home_address=request.POST['homeAddress'],
                                        account_type=request.POST['accountType'],)

        elif action == "edit":
            AccountFeatures.edit_account(username=request.POST['username'], password=request.POST['password'], user_email=request.POST['userEmail'],
                                         first_name=request.POST['firstName'], last_name=request.POST['lastName'], home_address=request.POST['homeAddress'],
                                         account_type=request.POST['accountType'],)