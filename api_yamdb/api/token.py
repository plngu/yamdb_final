from rest_framework_simplejwt.tokens import RefreshToken


def get_token_or_code(user):
    refresh = RefreshToken.for_user(user)
    return str(refresh.access_token)
