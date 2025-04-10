from base.serializers import TokenSerializer
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework import status
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.views import TokenRefreshView
from django.utils import timezone
from django.utils.translation import gettext as _
from rest_framework.exceptions import ValidationError

from base import permissions






Refresh_Token = TokenRefreshView.as_view()




class TokenCustomObtainAPI(TokenObtainPairView):
    serializer_class = TokenSerializer
Obtain_Token = TokenCustomObtainAPI.as_view()









class TokenLogoutAPI(APIView):
    permission_classes = [permissions.Authenticated]

    def post(self, request):
        refresh_token = request.data.get('refresh')
        user          = request.user
        
        if refresh_token:
            try :
                refresh_token = RefreshToken(refresh_token)
                refresh_token.blacklist()
            except TokenError as e: 
                return Response({"message " : f"token error : {e}"}, status = status.HTTP_400_BAD_REQUEST)
 
            user.last_logout = timezone.now()
            user.save()
            return Response({
                "message": _("You have been logged out successfully.")
            }, status=status.HTTP_200_OK)

        #if the refresh is not fetched
        raise ValidationError(_("Valid Refresh Token is Required"))

    

Logout_Token = TokenLogoutAPI.as_view()



