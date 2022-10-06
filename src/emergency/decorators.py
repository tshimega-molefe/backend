try:
    from functools import wraps
except:
    from django.utils.functional import wraps

from channels import exceptions
from user.models import User

roles = User.Roles.choices

def role_required(*roles):
    def decorator(func):
            @wraps(func)
            def wrapped_func(self, request, *args, **kwargs):
                if self.user.role not in roles:
                    raise exceptions.DenyConnection('You do not have access to this endpoint.')
                return func(self, request, *args, **kwargs)
            return wrapped_func
    return decorator