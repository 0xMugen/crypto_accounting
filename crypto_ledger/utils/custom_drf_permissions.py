from rest_framework import filters, permissions

from api.models import Ledgers, Wallets, Reports, Transactions, UserProfile


class IsObjectOwner(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        try:
            user = UserProfile.objects.get(user=request.user)
            return queryset.filter(user=user)
        except:
            return queryset.none()
        
class IsVerified(permissions.BasePermission):

    def has_permission(self, request, view):
        user = UserProfile.objects.get(user=request.user)
        if user.is_verified:
            return True
        else:
            return False