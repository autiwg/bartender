from rest_framework.exceptions import APIException


class InvalidInviteError(APIException):
    status_code = 401
    default_code = "invalid_invite"
    default_detail = "Invalid invite code given"
