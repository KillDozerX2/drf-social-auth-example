from rest_framework.permissions import AllowAny
from rest_framework.viewsets import GenericAPIView


class SocialAuthorizeView(GenericAPIView):
    """
    This view is used to generate an authorization Url

    **URL**: `/auth/social/authorize`

    """
