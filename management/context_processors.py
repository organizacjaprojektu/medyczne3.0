from .models import Staff


def user_role_context(request):
    if request.user.is_authenticated:
        try:
            staff_member = Staff.objects.get(user=request.user)
            return {'user_role': staff_member.role}
        except Staff.DoesNotExist:
            return {'user_role': None}
    else:
        return {'user_role': None}
