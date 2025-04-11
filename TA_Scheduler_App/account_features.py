from TA_Scheduler_App.models import User

class AccountFeatures:

    @staticmethod
    def create_user(username, password, userEmail,
                    firstName, lastName, accountType = 0, phoneNumber=0):
        user = User.objects.create(username=username,
                                   password=password, userEmail=userEmail,
                                   phoneNumber=phoneNumber, firstName=firstName,
                                   lastName=lastName, accountType=accountType)
        return user

    @staticmethod
    def  delete_account(user_id):
        try:
            user = User.objects.get(pk=user_id)
            user.delete()
            return True
        except User.DoesNotExist:
            return False

    @staticmethod
    def edit_account(user_id, username=None, password=None, userEmail=None,
                     phoneNumber=None, firstName=None, lastName=None, accountType=None):

        try:
            user = User.objects.get(pk = user_id)

            if username is not None:
                user.username = username
            if password is not None:
                user.password = password
            if userEmail is not None:
                user.userEmail = userEmail
            if phoneNumber is not None:
                user.phoneNumber = phoneNumber
            if firstName is not None:
                user.firstName = firstName
            if lastName is not None:
                user.lastName = lastName
            if accountType is not None:
                user.accountType = accountType

            user.save()
            return user
        except User.DoesNotExist:
            return None