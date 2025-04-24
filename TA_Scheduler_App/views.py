from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
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


        try:
            if action == "create":
                # Handle account creation with validation
                new_data ={
                    "new_username" : request.POST.get('username'),
                    "new_password" : request.POST.get('password'),
                    "new_email" : request.POST.get('userEmail'),
                    "new_first_name" : request.POST.get('firstName'),
                    "new_last_name" : request.POST.get('lastName'),
                    "new_home_address" : request.POST.get('homeAddress'),
                }

                if (new_data["new_username"] is None or new_data["new_password"] is None or
                        new_data["new_email"] is None or
                        new_data["new_first_name"] is None or new_data["new_last_name"] is None or
                        new_data["new_home_address"] is None):
                    messages.error(request, "Creation Error: Please fill all fields")
                    return redirect('accounts')

                new_data["new_username"] = new_data["new_username"].strip()
                new_data["new_password"] = new_data["new_password"].strip()
                new_data["new_email"] = new_data["new_email"].strip()
                new_data["new_first_name"] = new_data["new_first_name"].strip()
                new_data["new_last_name"] = new_data["new_last_name"].strip()
                new_data["new_home_address"] = new_data["new_home_address"].strip()

                new_account_type = request.POST.get('accountType', '2')  # Default to '2' if missing
                try:
                    new_account_type = int(new_account_type)
                except ValueError:
                    messages.error(request, "Creation Error: Please choose a valid account type")
                    return redirect('accounts')

                AccountFeatures.create_user(
                    username=new_data["new_username"],
                    password=new_data["new_password"],
                    user_email=new_data["new_email"],
                    first_name=new_data["new_first_name"],
                    last_name=new_data["new_last_name"],
                    home_address=new_data["new_home_address"],
                    account_type=new_account_type  # Now guaranteed to be an integer
                )
                messages.success(request, "User created successfully")

            elif action == "edit":
                # Handle account editing
                primary_key = request.POST.get("pk")

                updates = {
                    'username': request.POST.get('username', '').strip(),
                    'password': request.POST.get('password', '').strip(),
                    'user_email': request.POST.get('userEmail', '').strip(),
                    'first_name': request.POST.get('firstName', '').strip(),
                    'last_name': request.POST.get('lastName', '').strip(),
                    'home_address': request.POST.get('homeAddress', '').strip(),
                    'phone_number': request.POST.get('phoneNumber', '').strip() or None,
                    'account_type': request.POST.get('accountType'),
                    'user_id': primary_key
                }

                print("converting account type")
                # Convert accountType to integer
                if updates['account_type']:
                    try:
                        updates['account_type'] = int(updates['account_type'])
                    except ValueError:
                        messages.error(request, "Edit Error: Invalid role selection")
                        return redirect('accounts')

                if updates['phone_number']:
                    try:
                        updates['phone_number'] = int(updates['phone_number'])
                    except ValueError:
                        messages.error(request, "Edit Error: Invalid phone number")
                        return redirect('accounts')

                if updates:
                    try:
                        AccountFeatures.edit_account(user_id = primary_key, username=updates['username']
                                                               , password=updates['password']
                                                               , user_email=updates['user_email']
                                                               , first_name=updates['first_name']
                                                               , last_name=updates['last_name']
                                                               , home_address=updates['home_address']
                                                               , phone_number=updates['phone_number']
                                                               , account_type=updates['account_type'])
                        messages.success(request,"Account Updated Successfully")
                    except Exception as e:
                        messages.error(request, "Edit Error: " + str(e))

            elif action == "delete":
                # Handle deletion
                primary_key = request.POST.get('pk')
                if AccountFeatures.delete_account(user_id= primary_key) is True:
                    messages.success(request, "User deleted successfully")
                else:
                    messages.error(request, "Deletion Error: User not found")

        except IntegrityError as e:
            messages.error(request, f"Database error: {str(e)}")
        except Exception as e:
            messages.error(request, f"Error: {str(e)}")

        return redirect('accounts')