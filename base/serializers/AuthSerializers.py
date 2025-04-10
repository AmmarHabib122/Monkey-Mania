from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.exceptions import AuthenticationFailed
from django.utils.translation import gettext as _

from base import models
from base import serializers

class TokenSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        user = models.User.objects.get(phone_number=attrs['phone_number'])
        if self.user.is_active == False: 
            raise AuthenticationFailed(_("This User is not active any more"))
        data['user']     = serializers.UserSerializer(user).data
        data['message']  = _("Logged in successfully")
        return data