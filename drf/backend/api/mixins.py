from .permissions import IsStaffEditorPermisson
from rest_framework import permissions

class StaffEditorPermissonMixin():
    Permission_classes = [permissions.IsAdminUser,IsStaffEditorPermisson]


class UserQuerySetMixin():
    user_field = 'user'
    allow_staff_view = False
    def get_queryset(self,*args,**kwargs): # show data to relevant user
        user = self.request.user
        lookup_data = {}
        lookup_data[self.user_field] = user
        qs = super().get_queryset(*args,**kwargs)

        if self.allow_staff_view and user.is_staff:
            return qs
        
        return qs.filter(**lookup_data)
       