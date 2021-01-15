def user_must_be(request, view, action, field: str) -> bool:
    if not request.user or not request.user.is_authenticated:
        return False
    return getattr(request.user, field)
