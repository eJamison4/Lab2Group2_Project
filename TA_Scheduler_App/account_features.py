from TA_Scheduler_App.models import User


class AccountFeatures:
    @staticmethod
    def create_user(
        username: str, password: str,
        user_email: str, first_name: str, last_name: str,
        home_address="", account_type=2, phone_number=0,
    ):
        """
        Each account is required to have a username, password, email, first name, last name, and home address to start
        Account Type and phone number can be left blank and default to 0. `account_type=0` means the account will have TA perms.
        """
        user = User.objects.create_user(
            username=username, password=password,
            userEmail=user_email, phoneNumber=phone_number,
            firstName=first_name, lastName=last_name,
            homeAddress=home_address, accountType=account_type,
        )
        # new account is returned
        return user

    @staticmethod
    def delete_account(user_id):
        """
        The user id is the primary key of the User object.
        `delete_account()` returns `True` if the account is found and deleted, returning `False` otherwise
        """
        try:
            user = User.objects.get(pk=user_id)
            user.delete()
            return True
        # Error check if the account does not exist, likely not needed
        except User.DoesNotExist:
            return False

    @staticmethod
    def edit_account(
        user_id, username="", password="",
        user_email="", phone_number: int = None,
        first_name="", last_name="",
        account_type: int = None, home_address="",
    ):
        """
        Allows any amount of user fields to be changed at a time.
        Every parameter except `user_id` is optional.
        returns the updated user account.
        `user_id` should be a primary key.
        When calling `edit_account()`, it is recommended to pass arguments as KWARGS
        ex: `edit_account(username='<some_name>')`
        """
        try:
            # The primary key for the account is used to retrieve the appropriate account
            user = User.objects.get(pk=user_id)

            print("\n--- BEFORE CHANGES ---")
            print(f"Username: {user.username}")
            print(f"Email: {user.userEmail}")
            print(f"Account Type: {user.accountType}")

            # Checks which fields is desired to change
            # skipping each parameter that wasn't passed
            if username != "":
                user.username = username
            if password != "":
                user.set_password(password)
            if user_email != "":
                user.userEmail = user_email
            if phone_number is not None:
                user.phoneNumber = phone_number
            if first_name != "":
                user.firstName = first_name
            if last_name != "":
                user.lastName = last_name
            if account_type is not None:
                user.accountType = account_type
            if home_address != "":
                user.homeAddress = home_address

            user.save()

            print("\n--- AFTER CHANGES ---")
            print(f"Username: {user.username}")
            print(f"Email: {user.userEmail}")
            print(f"Account Type: {user.accountType}\n")
            return user.pk
        # Error check if the account does not exist, likely not needed
        except User.DoesNotExist:
            return None
