from django.db import transaction
from django.utils import timezone
from django.utils.translation import gettext as _
from rest_framework import generics
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.response import Response

from base import models, permissions, serializers


class RoleAccessList:
    role_access_list = ['owner', 'admin', 'manager', 'reception']


class CreateBillTimePauseAPI(RoleAccessList, generics.CreateAPIView):
    queryset           = models.BillTimePause.objects.all()
    serializer_class   = serializers.BillTimePauseSerializer
    permission_classes = [permissions.Authenticated, permissions.RoleAccess]

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        response.data['message'] = _("Bill pause created successfully")
        return response


Create_Bill_Time_Pause = CreateBillTimePauseAPI.as_view()


class CloseBillTimePauseAPI(RoleAccessList, generics.UpdateAPIView):
    queryset           = models.BillTimePause.objects.select_related('bill')
    serializer_class   = serializers.BillTimePauseSerializer
    permission_classes = [permissions.Authenticated, permissions.RoleAccess]
    lookup_field       = 'pk'

    def update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        with transaction.atomic():
            self.queryset = self.get_queryset().select_for_update()
            pause = self.get_object()
            user = request.user
            if user.branch and user.branch != pause.bill.branch:
                raise PermissionDenied(_("You do not have the permission to access this time pause"))
            if not pause.is_active:
                raise ValidationError(_("This bill pause is already closed"))

            pause.finished = timezone.now()
            pause.finished_by = user
            pause.save(update_fields=['finished', 'finished_by', 'updated'])

        data = self.get_serializer(pause).data
        data['message'] = _("Bill pause closed successfully")
        return Response(data)


Close_Bill_Time_Pause = CloseBillTimePauseAPI.as_view()


class GetBillTimePauseAPI(RoleAccessList, generics.RetrieveAPIView):
    queryset           = models.BillTimePause.objects.select_related(
        'bill', 'created_by', 'finished_by'
    )
    serializer_class   = serializers.BillTimePauseSerializer
    permission_classes = [permissions.Authenticated, permissions.RoleAccess]
    lookup_field       = 'pk'

    def get_object(self):
        instance = super().get_object()
        user = self.request.user
        if user.branch and user.branch != instance.bill.branch:
            raise PermissionDenied(_("You do not have the permission to access this time pause"))
        return instance


Get_Bill_Time_Pause = GetBillTimePauseAPI.as_view()
