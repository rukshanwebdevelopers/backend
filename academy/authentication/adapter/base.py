# Python imports
import uuid

from django.core.validators import validate_email
# Django imports
from django.utils import timezone
from rest_framework.exceptions import ValidationError
# Third party imports
from zxcvbn import zxcvbn

from academy.authentication.views.common import get_tokens_for_user
# Module imports
from academy.db.models import User


class Adapter:
    """Common interface for all auth providers"""

    def __init__(self, request, provider, callback=None):
        self.request = request
        self.provider = provider
        self.callback = callback
        self.token_data = None
        self.user_data = None

    def get_user_token(self, data, headers=None):
        raise NotImplementedError

    def get_user_response(self):
        raise NotImplementedError

    def set_token_data(self, data):
        self.token_data = data

    def set_user_data(self, data):
        self.user_data = data

    def create_update_account(self, user):
        raise NotImplementedError

    def authenticate(self):
        raise NotImplementedError

    def sanitize_email(self, email):
        # Check if email is present
        if not email:
            ...
            # raise AuthenticationException(
            #     error_code=AUTHENTICATION_ERROR_CODES["INVALID_EMAIL"],
            #     error_message="INVALID_EMAIL",
            #     payload={"email": email},
            # )

        # Sanitize email
        email = str(email).lower().strip()

        # validate email
        try:
            validate_email(email)
        except ValidationError:
            ...
            # raise AuthenticationException(
            #     error_code=AUTHENTICATION_ERROR_CODES["INVALID_EMAIL"],
            #     error_message="INVALID_EMAIL",
            #     payload={"email": email},
            # )
        # Return email
        return email

    def validate_password(self, email):
        """Validate password strength"""
        results = zxcvbn(self.code)
        if results["score"] < 3:
            ...
            # raise AuthenticationException(
            #     error_code=AUTHENTICATION_ERROR_CODES["INVALID_PASSWORD"],
            #     error_message="INVALID_PASSWORD",
            #     payload={"email": email},
            # )
        return

    def __check_signup(self, email):
        """Check if sign up is enabled or not and raise exception if not enabled"""

        # Get configuration value
        # (ENABLE_SIGNUP,) = get_configuration_value(
        #     [{"key": "ENABLE_SIGNUP", "default": os.environ.get("ENABLE_SIGNUP", "1")}]
        # )
        #
        # # Check if sign up is disabled and invite is present or not
        # if (
        #     ENABLE_SIGNUP == "0"
        #     and not WorkspaceMemberInvite.objects.filter(email=email).exists()
        # ):
        #     # Raise exception
        #     raise AuthenticationException(
        #         error_code=AUTHENTICATION_ERROR_CODES["SIGNUP_DISABLED"],
        #         error_message="SIGNUP_DISABLED",
        #         payload={"email": email},
        #     )

        return True

    def save_user_data(self, user):
        # Update user details
        user.last_login_medium = self.provider
        user.last_active = timezone.now()
        user.last_login_time = timezone.now()
        # user.last_login_ip = get_client_ip(request=self.request)
        user.last_login_uagent = self.request.META.get("HTTP_USER_AGENT")
        user.token_updated_at = timezone.now()
        # If user is not active, send the activation email and set the user as active
        # if not user.is_active:
        #     user_activation_email.delay(base_host(request=self.request), user.id)
        # Set user as active
        user.is_active = True
        user.save()
        return user

    def complete_login_or_signup(self):
        # Get email
        email = self.user_data.get("email")

        # Sanitize email
        email = self.sanitize_email(email)

        # Check if the user is present
        user = User.objects.filter(email=email).first()
        # Check if sign up case or login
        is_signup = bool(user)
        # If user is not present, create a new user
        if not user:
            # New user
            # self.__check_signup(email)

            # Initialize user
            user = User(email=email, username=uuid.uuid4().hex)

            # Check if password is autoset
            if self.user_data.get("user").get("is_password_autoset"):
                user.set_password(uuid.uuid4().hex)
                user.is_password_autoset = True
                user.is_email_verified = True

            # Validate password
            else:
                # Validate password
                self.validate_password(email)
                # Set password
                user.set_password(self.code)
                user.is_password_autoset = False

            # Set user details
            first_name = self.user_data.get("user", {}).get("first_name", "")
            last_name = self.user_data.get("user", {}).get("last_name", "")
            user.first_name = first_name if first_name else ""
            user.last_name = last_name if last_name else ""
            user.save()

            # Create profile
            # Profile.objects.create(user=user)

        # Save user data
        user = self.save_user_data(user=user)

        # Create or update account if token data is present
        if self.token_data:
            self.create_update_account(user=user)

        return user
