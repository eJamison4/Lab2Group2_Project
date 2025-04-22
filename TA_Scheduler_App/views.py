from django.shortcuts import render  # , redirect
from django.views import View
from django.contrib.auth import authenticate, login

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
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return render(request, "dashboard.html", {"username": username})
        return render(
            request,
            "login.html",
            {"message": "Either username or password is incorrect!"}
        )
        # return redirect()
       


class Account(View):
    def get(self, request):
        ...

    def post(self, request):
        ...
