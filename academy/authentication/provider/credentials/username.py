from rest_framework.exceptions import ValidationError

from academy.authentication.adapter.credential import CredentialAdapter
from academy.authentication.views.common import get_tokens_for_user
from academy.db.models import User


class UsernameProvider(CredentialAdapter):
    provider = "username"

    def __init__(self, request, key=None, code=None, is_signup=False, callback=None):
        super().__init__(request=request, provider=self.provider, callback=callback)
        self.key = key
        self.code = code
        self.is_signup = is_signup

    def set_user_data(self):
        if self.is_signup:
            ...
        else:
            user = User.objects.filter(username=self.key).first()

            if not user:
                # Todo -> refactor error message
                raise ValidationError(
                    detail="Invalid credentials"
                )

            if not user.check_password(self.code):
                # Todo -> refactor error message
                raise ValidationError(
                    detail="Invalid credentials"
                )

            super().set_user_data(
                {
                    "username": self.key,
                    "user": {
                        "first_name": "",
                        "last_name": "",
                        "provider_id": "",
                        "is_password_autoset": False,
                    }
                }
            )
            return

    def get_user_token(self, data, headers=None):
        return get_tokens_for_user(data)
