from rest_framework.authtoken.models import Token


def create_token(user):
    token = Token.objects.create(user=user)
    token.save()


def get_token_from_user(user):
    token = Token.objects.get(user__username=user.username)
    return token

