from rest_framework import generics
from rest_framework.exceptions import ValidationError, PermissionDenied
from django.utils.translation import gettext as _
from rest_framework.filters import SearchFilter

from base import serializers
from base import models
from base import permissions
from base import libs




'''##############################SubscriptionAPIs######################################'''





class RoleAccessList:
    role_access_list    = ['owner', 'admin']






class CreateSubscriptionAPI(RoleAccessList, generics.CreateAPIView):
    queryset           = models.Subscription.objects.all()
    serializer_class   = serializers.SubscriptionSerializer
    permission_classes = [permissions.Authenticated, permissions.RoleAccess]

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        response.data['message'] = _("Subscription Created successfully")
        return response
Create_Subscription = CreateSubscriptionAPI.as_view()






class UpdateSubscriptionAPI(RoleAccessList, generics.UpdateAPIView):
    queryset           = models.Subscription.objects.all()
    serializer_class   = serializers.SubscriptionSerializer
    permission_classes = [permissions.Authenticated, permissions.RoleAccess]
    lookup_field       = "pk"

    def update(self, request, *args, **kwargs):
        kwargs['partial'] = True if request.method == "PATCH" else False
        response = super().update(request, *args, **kwargs)
        response.data['message'] = _("Subscription Updated successfully")
        return response
Update_Subscription = UpdateSubscriptionAPI.as_view()




class GetSubscriptionAPI(RoleAccessList, generics.RetrieveAPIView):
    queryset           = models.Subscription.objects.all()
    serializer_class   = serializers.SubscriptionSerializer
    role_access_list   = ['owner', 'admin', 'manager']
    permission_classes = [permissions.Authenticated, permissions.RoleAccess]
    lookup_field       = "pk"

Get_Subscription = GetSubscriptionAPI.as_view()







class ListSubscriptionAPI(RoleAccessList, generics.ListAPIView):
    queryset           = models.Subscription.objects.all()
    serializer_class   = serializers.SubscriptionSerializer
    role_access_list   = ['owner', 'admin', 'manager']
    permission_classes = [permissions.Authenticated, permissions.RoleAccess]
    filter_backends    = [SearchFilter]
    search_fields      = ['name'] 

List_Subscription = ListSubscriptionAPI.as_view()










'''##############################SubscriptionInstanceAPIs######################################'''



class RoleAccessList:
    role_access_list    = ['owner', 'admin', 'manager', 'reception']






class CreateSubscriptionInstanceAPI(RoleAccessList, generics.CreateAPIView):
    queryset           = models.SubscriptionInstance.objects.all()
    serializer_class   = serializers.SubscriptionInstanceSerializer
    permission_classes = [permissions.Authenticated, permissions.RoleAccess]

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        response.data['message'] = _("SubscriptionInstance Created successfully")
        return response
Create_SubscriptionInstance = CreateSubscriptionInstanceAPI.as_view()






class UpdateSubscriptionInstanceAPI(RoleAccessList, generics.UpdateAPIView):
    queryset           = models.SubscriptionInstance.objects.all()
    serializer_class   = serializers.SubscriptionInstanceSerializer
    role_access_list    = ['owner', 'admin', 'manager']
    permission_classes = [permissions.Authenticated, permissions.RoleAccess]
    lookup_field       = "pk"

    def update(self, request, *args, **kwargs):
        kwargs['partial'] = True if request.method == "PATCH" else False
        response = super().update(request, *args, **kwargs)
        response.data['message'] = _("SubscriptionInstance Updated successfully")
        return response
Update_SubscriptionInstance = UpdateSubscriptionInstanceAPI.as_view()




class GetSubscriptionInstanceAPI(RoleAccessList, generics.RetrieveAPIView):
    queryset           = models.SubscriptionInstance.objects.all()
    serializer_class   = serializers.SubscriptionInstanceSerializer
    permission_classes = [permissions.Authenticated, permissions.RoleAccess]
    lookup_field       = "pk"

    def get_object(self):
        obj = super().get_object()
        if self.request.user.branch    and   obj.branch != self.request.user.branch:
            raise PermissionDenied(_("You do not have the permission to access this data"))
        return obj

Get_SubscriptionInstance = GetSubscriptionInstanceAPI.as_view()







class ListSubscriptionInstanceAPI(RoleAccessList, generics.ListAPIView):
    queryset           = models.SubscriptionInstance.objects.all()
    serializer_class   = serializers.SubscriptionInstanceSerializer
    permission_classes = [permissions.Authenticated, permissions.RoleAccess]
    filter_backends    = [SearchFilter]
    search_fields      = ['child__name', 'child__child_phone_numbers_set__phone_number__value', 'subscription__name'] 

    def get_queryset(self):
        branches = libs.get_branch_ids(self)
        query    = super().get_queryset().filter(branch__in = branches) if branches != ['all'] else super().get_queryset()
        start_date, end_date, is_date_range = libs.get_date_range(self)
        if is_date_range   and   start_date == end_date:
            query = libs.get_all_instances_in_a_day_query(query, start_date)
        elif is_date_range:
            query = libs.get_all_instances_in_a_date_range_query(query, start_date, end_date)
        return query
List_SubscriptionInstance = ListSubscriptionInstanceAPI.as_view()