from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import IntegrityError
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.http import HttpResponseForbidden


from TA_Scheduler_App.assignment_features import assignment_features
from TA_Scheduler_App.models import User, Course, Section, teacherToTA  # , Assignment
from TA_Scheduler_App.account_features import AccountFeatures
from TA_Scheduler_App.courseFeatures import CourseFeatures
# from TA_Scheduler_App.relation_features import teacher_to_TA_features as relationFeatures
from TA_Scheduler_App.skills_features import SkillsFeatures


# Create your views here.
class Login(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect("my_acc_info")
        return render(request, "login.html", {})

    def post(self, request):
        username = request.POST["username"]
        password = request.POST["password"]

        if username.strip() == "" or password.strip() == "":  # do nothing if either field is empty
            return render(request, "login.html")

        user = authenticate(request, username=username, password=password)

        print(username)
        print(password)
        if user is not None:
            login(request, user)
            return render(request, "my_acc_info.html", context={"username": username})

        return render(request, "login.html", {"message": "Either username or password is incorrect!"})
        # return redirect()


class Dashboard(LoginRequiredMixin, View):
    login_url = "/"

    def get(self, request):
        # Add any dashboard context data here
        return render(request, "dashboard.html", {"user": request.user, "is_admin": request.user.accountType == 2})


class Account(LoginRequiredMixin, View):
    login_url = "/"
    template_name = "accounts.html"

    def get(self, request):
        users = User.objects.all().order_by("id")
        is_admin = request.user.is_authenticated and getattr(request.user, "accountType", 0) == 2
        return render(request, self.template_name, {"users": users, "is_admin": is_admin})

    def post(self, request):
        if not request.user.is_authenticated or request.user.accountType != 2:
            return HttpResponseForbidden("Admins only.")

        action = request.POST.get("action")

        try:
            if action == "create":
                # Handle account creation with validation
                new_data = {
                    "new_username": request.POST.get("username"),
                    "new_password": request.POST.get("password"),
                    "new_email": request.POST.get("userEmail"),
                    "new_first_name": request.POST.get("firstName"),
                    "new_last_name": request.POST.get("lastName"),
                    "new_home_address": request.POST.get("homeAddress"),
                    "new_phone_number": request.POST.get("phoneNumber"),
                }

                try:
                    new_data["new_username"] = new_data["new_username"].strip()
                except Exception:
                    new_data["new_username"] = ""

                try:
                    new_data["new_password"] = new_data["new_password"].strip()
                except Exception:
                    new_data["new_password"] = ""

                try:
                    new_data["new_email"] = new_data["new_email"].strip()
                except Exception:
                    new_data["new_email"] = ""

                try:
                    new_data["new_first_name"] = new_data["new_first_name"].strip()
                except Exception:
                    new_data["new_first_name"] = ""

                try:
                    new_data["new_last_name"] = new_data["new_last_name"].strip()
                except Exception:
                    new_data["new_last_name"] = ""

                try:
                    new_data["new_home_address"] = new_data["new_home_address"].strip()
                except Exception:
                    new_data["new_home_address"] = ""

                try:
                    new_data["new_phone_number"] = new_data["new_phone_number"].strip()
                except Exception:
                    new_data["new_phone_number"] = ""

                if (
                    new_data["new_username"] == ""
                    or new_data["new_password"] == ""
                    or new_data["new_email"] == ""
                    or new_data["new_first_name"] == ""
                    or new_data["new_last_name"] == ""
                ):
                    messages.error(request, "Creation Error: Please fill all fields")
                    return redirect("accounts")

                new_account_type = request.POST.get("accountType", "2")  # Default to '2' if missing
                try:
                    new_account_type = int(new_account_type)
                except ValueError:
                    messages.error(request, "Creation Error: Please choose a valid account type")
                    return redirect("accounts")
                if new_data["new_phone_number"] != "":
                    try:
                        new_data["new_phone_number"] = int(new_data["new_phone_number"])
                    except ValueError:
                        messages.error(request, "Invalid phone number format")
                        return redirect("accounts")
                else:
                    new_data["new_phone_number"] = 0

                AccountFeatures.create_user(
                    username=new_data["new_username"],
                    password=new_data["new_password"],
                    user_email=new_data["new_email"],
                    first_name=new_data["new_first_name"],
                    last_name=new_data["new_last_name"],
                    home_address=new_data["new_home_address"],
                    phone_number=new_data["new_phone_number"],
                    account_type=new_account_type,  # Now guaranteed to be an integer
                )
                messages.success(request, "User created successfully")

            elif action == "edit":
                # Handle account editing
                primary_key = request.POST.get("pk")

                updates = {
                    "username": request.POST.get("username", ""),
                    "password": request.POST.get("password", ""),
                    "user_email": request.POST.get("userEmail", ""),
                    "first_name": request.POST.get("firstName", ""),
                    "last_name": request.POST.get("lastName", ""),
                    "home_address": request.POST.get("homeAddress", ""),
                    "phone_number": request.POST.get("phoneNumber", "") or None,
                    "account_type": request.POST.get("accountType"),
                    "user_id": primary_key,
                }

                try:
                    updates["username"] = updates["username"].strip()
                except Exception:
                    updates["username"] = ""
                try:
                    updates["password"] = updates["password"].strip()
                except Exception:
                    updates["password"] = ""
                try:
                    updates["user_email"] = updates["user_email"].strip()
                except Exception:
                    updates["user_email"] = ""
                try:
                    updates["first_name"] = updates["first_name"].strip()
                except Exception:
                    updates["first_name"] = ""
                try:
                    updates["last_name"] = updates["last_name"].strip()
                except Exception:
                    updates["last_name"] = ""
                try:
                    updates["home_address"] = updates["home_address"].strip()
                except Exception:
                    updates["home_address"] = ""

                print("converting account type")
                # Convert accountType to integer
                if updates["account_type"]:
                    try:
                        updates["account_type"] = int(updates["account_type"])
                    except ValueError:
                        messages.error(request, "Edit Error: Invalid role selection")
                        return redirect("accounts")

                if updates["phone_number"]:
                    try:
                        updates["phone_number"] = int(updates["phone_number"])
                        print("Phone number: ", updates["phone_number"])
                    except ValueError:
                        messages.error(request, "Edit Error: Invalid phone number")
                        return redirect("accounts")

                if updates:
                    try:
                        AccountFeatures.edit_account(
                            user_id=primary_key,
                            username=updates["username"],
                            password=updates["password"],
                            user_email=updates["user_email"],
                            first_name=updates["first_name"],
                            last_name=updates["last_name"],
                            home_address=updates["home_address"],
                            phone_number=updates["phone_number"],
                            account_type=updates["account_type"],
                        )
                        messages.success(request, "Account Updated Successfully")
                    except Exception as e:
                        messages.error(request, "Edit Error: " + str(e))

            elif action == "delete":
                # Handle deletion
                primary_key = request.POST.get("pk")
                if AccountFeatures.delete_account(user_id=primary_key) is True:
                    messages.success(request, "User deleted successfully")
                    if request.user.is_authenticated and request.user.pk == int(primary_key):
                        logout(request)
                        return redirect("login")
                else:
                    messages.error(request, "Deletion Error: User not found")

        except IntegrityError as e:
            messages.error(request, f"Database error: {str(e)}")
        except Exception as e:
            messages.error(request, f"Error: {str(e)}")

        return redirect("accounts")


class Courses(View):
    def get(self, request):
        courses = Course.objects.all()
        # prefetch sections so the template can loop efficiently
        print("COURSES:", courses)
        return render(request, "courses.html", {"courses": courses})

    def post(self, request):

        userType = request.user.accountType
        if userType < 2:
            requestStuff = request.POST.copy()
            requestStuff.update({'errorCode':'User is not an admin and has no edit permissions'})
            return render(request,template_name='courses.html',context=requestStuff,status=403)

        action = request.POST.get("action")

        if action == "logout":
            logout(request)
            return redirect("login")

        if action == 'create':
            name = request.POST.get("courseName")
            if name:
                CourseFeatures.create_course(courseName=name)

        if action == 'edit':
            courseID = int(request.POST.get("courseId"))
            newCourseName = request.POST.get("newCourseName")
            if courseID:
                CourseFeatures.edit_course(courseKey=courseID, newCourseName=newCourseName)

        if action == 'delete':
            courseID = int(request.POST.get("courseId"))
            if courseID:
                CourseFeatures.delete_course(courseKey=courseID)

        return redirect("courses")


class AddSection(View):
    def post(self, request, course_id):
        course = get_object_or_404(Course, pk=course_id)
        code = request.POST.get("sectionCode")
        instructor = request.POST.get("instructor")
        if code:
            Section.objects.create(course=course, sectionCode=code, instructor=instructor or "")
        return redirect("courses")


class Assignments(View):
    def get(self, request):
        courses = Course.objects.all()
        relations = teacherToTA.objects.all().filter(teacherIDF=request.user)
        return render(request, "courses.html", {"relations": relations, "courses": courses})

    def post(self, request, section=None, assignment=None):
        action = request.POST.get("action")
        if action == "create":
            assignment_features.create_assignment(self, section, request.user)
            return redirect("courses")
        if action == "delete":
            if assignment is not None:
                assignment_features.delete_assignment(self, assignment.pk)

        return redirect("course")


class Skills(View):
    def get(self, request):
        skill = Skills.objects.all().filter(userId=request.user.pk)
        return render(request, "accounts.html", {"skills": skill})

    def post(self, request, skillId=None, skillString=None):
        action = request.POST.get("action")

        if action == "logout":
            logout(request)
            return redirect("login")

        if action == "create":
            if skillString is not None:
                SkillsFeatures.create_skill(request.user, skillString)

        if action == "edit":
            if skillId is not None and skillString is not None:
                SkillsFeatures.edit_skill(skillId, skillString)

        if action == "delete":
            if skillId is not None:
                SkillsFeatures.delete_skill(skillId)


class MyAccount(View):
    def get(self, request):
        acc_info = request.user
        is_admin = request.user.is_authenticated and getattr(request.user, "accountType", 0) == 2
        return render(request, "my_acc_info.html", context={"u": acc_info, "is_admin": is_admin})

    def post(self, request):
        action = request.POST.get("action")

        if action == "logout":
            logout(request)
            return redirect("login")
        else:
            mod_keys = {
                "firstName": "first_name", "lastName": "last_name",
                "username": "username", "password":"password",
                "userEmail": "user_email", "phoneNumber": "phone_number",
                "homeAddress": "home_address"
            }  # keys are the model variable names, vals are the corresponding arg names for `edit_account()`
            user_acc = request.user
            for var, arg_name in mod_keys.items():
                form_return = request.POST.get(var)
                if form_return and form_return != getattr(User.objects.get(pk=user_acc.pk), var):
                    if form_return is not None and var == "phoneNumber":
                        print(f"'{form_return}' and var = {var}")
                        AccountFeatures.edit_account(user_acc.pk, phone_number=int(form_return))
                    else:
                        exec(f'AccountFeatures.edit_account({user_acc.pk}, {arg_name}="{form_return}")')
            return redirect("my_acc_info")

class Feedback(View):
    def get(self, request):
        return render(request, "feedback.html", context={})

    def post(self, request):
        return redirect("feedback")


class SendNotifs(View):
    def get(self, request):
        return render(request, "send_notifs.html", context={})

    def post(self, request):
        return redirect("send_notifs")
