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
        print(users)
        return render(request, self.template_name, {"users": users})

    def post(self, request):
        print("Start of post")

        action = request.POST.get('action')

        print(action)

        try:
            if action == "create":
                print("Create new account")
                # Handle account creation with validation
                new_username = request.POST.get('username')
                account_type = request.POST.get('accountType', '0')  # Default to '0' if missing
                try:
                    account_type = int(account_type)
                except ValueError:
                    messages.error(request, "Invalid account type")
                    return redirect('accounts')

                AccountFeatures.create_user(
                    username=request.POST.get('username', '').strip(),
                    password=request.POST.get('password', '').strip(),
                    user_email=request.POST.get('userEmail', '').strip(),
                    first_name=request.POST.get('firstName', '').strip(),
                    last_name=request.POST.get('lastName', '').strip(),
                    home_address=request.POST.get('homeAddress', '').strip(),
                    account_type=account_type  # Now guaranteed to be an integer
                )
                messages.success(request, "User created successfully")

            elif action == "edit":
                # Handle account editing
                print("Start of edit")
                primarykey = request.POST.get("pk")

                # Match EXACT model field names (case-sensitive)
                print("getting updates")
                updates = {
                    'username': request.POST.get('username', '').strip(),
                    'password': request.POST.get('password', '').strip(),
                    'user_email': request.POST.get('userEmail', '').strip(),  # Changed to userEmail
                    'first_name': request.POST.get('firstName', '').strip(),  # Changed to firstName
                    'last_name': request.POST.get('lastName', '').strip(),  # Changed to lastName
                    'home_address': request.POST.get('homeAddress', '').strip(),  # Changed to homeAddress
                    'phone_number': request.POST.get('phoneNumber', '').strip() or None,  # Changed to phoneNumber
                    'account_type': request.POST.get('accountType'),  # Changed to accountType
                    'user_id': primarykey
                }

                print("converting account type")
                # Convert accountType to integer
                if updates['account_type']:
                    try:
                        updates['account_type'] = int(updates['account_type'])
                    except ValueError:
                        messages.error(request, "Invalid role selection")
                        return redirect('accounts')
                print("converting phone number")
                if updates['phone_number']:
                    try:
                        updates['phone_number'] = int(updates['phone_number'])
                    except ValueError:
                        messages.error(request, "Invalid phone number")
                        return redirect('accounts')

                # Remove empty values

                user_id = primarykey

                print("prep to update user")
                if updates:
                    try:
                        print("updating user")
                        user_id = AccountFeatures.edit_account(user_id = primarykey, username=updates['username']
                                                               , password=updates['password']
                                                               , user_email=updates['user_email']
                                                               , first_name=updates['first_name']
                                                               , last_name=updates['last_name']
                                                               , home_address=updates['home_address']
                                                               , phone_number=updates['phone_number']
                                                               , account_type=updates['account_type'])
                        print("done updating")
                    except Exception as e:
                        print(e)

                user = User.objects.get(pk = user_id)

                print("DEBUG: Edit form submitted with data:", request.POST)
                print("Processed updates:", updates)
                print("DEBUG: new username:\n", user.username)
                print("DEBUG: new password:\n", user.password)
                print("DEBUG: new email:\n", user.userEmail)
                print("DEBUG: new phone number:\n", user.phoneNumber)
                print("DEBUG: new ROLE:\n", user.accountType)
                print("DEBUG: new address:\n", user.homeAddress)

            elif action == "delete":
                # Handle deletion
                print("Start of delete")
                primarykey = request.POST.get('pk')
                print(primarykey)
                if AccountFeatures.delete_account(user_id= primarykey) is True:
                    messages.success(request, "User deleted successfully")
                    print("DEBUG: User deleted successfully")
                else:
                    messages.error(request, "User not found")

        except IntegrityError as e:
            messages.error(request, f"Database error: {str(e)}")
            print(e)
        except Exception as e:
            messages.error(request, f"Error: {str(e)}")
            print(e)

        print("end of post")
        return redirect('accounts')