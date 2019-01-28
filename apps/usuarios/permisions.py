from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.models import Group
from django.shortcuts import redirect

denied_message = 'Acceso denegado'

class OnlyAdminMixin(UserPassesTestMixin):
    raise_exception = False
    permission_denied_message = denied_message

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_admin()


class UserInGroupsMixin(UserPassesTestMixin):
    """
    Mixin para permitir 1 o varios grupos de usuarios para una vista,
    Se utiliza el atributo de la clase user_groups el cual es una lista con los nombres de los grupos permitidos
    """
    raise_exception = False
    permission_denied_message = denied_message

    def test_func(self):
        user = self.request.user
        allowGroups = Group.objects.filter(name__in=self.user_groups)
        if user.groups.all().first() in allowGroups:
            return True
        if self.request.user.is_superuser:
            return True
        return False
