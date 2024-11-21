from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import user_passes_test


def role_required(role):
    def decorator(view_func):
        @user_passes_test(lambda u: u.is_authenticated and hasattr(u, 'staff') and u.staff.role == role)
        def _wrapped_view(request, *args, **kwargs):
            if request.user.is_authenticated and hasattr(request.user, 'staff') and request.user.staff.role == role:
                return view_func(request, *args, **kwargs)
            return HttpResponseForbidden()

        return _wrapped_view

    return decorator
