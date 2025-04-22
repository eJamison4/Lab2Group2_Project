from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, reverse
from django.views import View
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
        user = authenticate(request, username=username, password=password)

        print(username)
        print(password)
        if user is not None:
            login(request, user)
            return render(request, "dashboard.html", context={"username": username})

        return render(
            request,
            "login.html",
            {"message": "Either username or password is incorrect!"}
        )
        # return redirect()


class Account(View):
    template_name = "accounts.html"

    def get(self, request):
        users = User.objects.all().order_by("id")
        return render(request, self.template_name, {"users": users})

    def post(self, request):
        action = request.POST.get('action')

        if action == "create":

            AccountFeatures.create_user(username=request.POST.get('username'), password=request.POST.get('password')
                                        , user_email=request.POST.get('userEmail'), first_name=request.POST.get('firstName'),
                                        last_name=request.POST.get('lastName'), home_address=request.POST.get('homeAddress'),
                                        account_type=int(request.POST.get('accountType')) or 0,)

        elif action == "edit":

            user_id = request.POST.get("user_id")

            AccountFeatures.edit_account(username=request.POST.get('username') or None, password=request.POST.get('password') or None
                                         ,user_email=request.POST.get('userEmail') or None,
                                         first_name=request.POST.get('firstName') or None,
                                         last_name=request.POST.get('lastName') or None
                                         ,home_address=request.POST.get('homeAddress') or None,
                                         account_type=request.POST.get('accountType') or None, user_id=user_id)
        elif action == "delete":
            user_id = request.POST.get('user_id')

            AccountFeatures.delete_account(user_id=user_id)

        return redirect(reverse("accounts"))