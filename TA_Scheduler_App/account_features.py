from TA_Scheduler_App.models import User
#file depends on the models provided by models.py
#AccountFeatures works with the User model provided in the file


#This class features functions that create new accounts,
# deletes existing accounts via userID, and edits any account information
class AccountFeatures:

    #Function that creates account.  Takes in the necessary data to create account.
    #Each account is required to have a username, password, email, first name, last name, and home address to start
    #Account Type and phone number can be left blank and default to 0
    @staticmethod
    def create_user(username : str, password : str, user_email: str,
                    first_name: str, last_name: str, home_address: str, account_type: int= 0, phone_number: int =0):
        #Account creation happens here
        user = User.objects.create(username=username,
                                   password=password, userEmail=user_email,
                                   phoneNumber=phone_number, firstName=first_name,
                                   lastName=last_name, homeAddress = home_address, accountType=account_type)
        #new account is returned
        return user

    #Function that deletes an existing account.  The user id of the account has to be used to find the account
    #The user id is the primary key of the User object
    @staticmethod
    def  delete_account(user_id):
        #The function either returns true if the account is found and deleted
        #If the account does not exist, it returns false
        try:
            user = User.objects.get(pk=user_id)
            user.delete()
            return True
        #Error check if the account does not exist, likely not needed
        except User.DoesNotExist:
            return False

    #edits an existing account, allowing any amount of user fields to be changed at a time.
    #Every parameter for this function is entirely optional
    #The function returns the updated user account
    #user_id should be a primary key
    #When calling this function, it is recommended to specify the parameter being passed
    # ex: edit_account(username='some fake name')
    @staticmethod
    def edit_account(user_id, username: str ="", password: str ="", user_email: str="",
                     phone_number: int =None, first_name: str="", last_name: str ="", account_type: int =None
                     , home_address: str = ""):

        try:
            #The primary key for the account is used to retrieve the appropriate account
            user = User.objects.get(pk = user_id)

            print("\n--- BEFORE CHANGES ---")
            print(f"Username: {user.username}")
            print(f"Email: {user.userEmail}")
            print(f"Account Type: {user.accountType}")

            #This chain of if statements check which fields is desired to change
            #For example, if no new username is given,
            # it skips that field and focuses on other fields that need to be changed
            if username is not "":
                user.username = username
            if password is not "":
                user.password = password
            if user_email is not "":
                user.userEmail = user_email
            if phone_number is not None:
                user.phoneNumber = phone_number
            if first_name is not "":
                user.firstName = first_name
            if last_name is not "":
                user.lastName = last_name
            if account_type is not None:
                user.accountType = account_type
            if home_address is not "":
                user.homeAddress = home_address

            #saves the current user instance
            user.save()

            print("\n--- AFTER CHANGES ---")
            print(f"Username: {user.username}")
            print(f"Email: {user.userEmail}")
            print(f"Account Type: {user.accountType}\n")
            return user.pk
        #Error check if the account does not exist, likely not needed
        except User.DoesNotExist:
            return None