from typing import Optional, Any

from db.models import User


def create_user(username: str,
                password: str,
                email: Optional[str] = None,
                first_name: Optional[str] = None,
                last_name: Optional[str] = None
    ) -> User:
    user = User.objects.create_user(
        username=username,
        email=email,
        password=password,
    )

    if first_name is not None:
        user.first_name = first_name
    if last_name is not None:
        user.last_name = last_name

    if first_name is not None or last_name is not None:
        user.save()

    return user

def get_user(user_id: int) -> Optional[User]:
    return User.objects.get(id=user_id)

def update_user(
    user_id: int,
    username: Optional[str] = None,
    password: Optional[str] = None,
    email: Optional[str] = None,
    first_name: Optional[str] = None,
    last_name: Optional[str] = None
) -> Optional[User]:
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return None

    if username is not None:
        user.username = username
    if email is not None:
        user.email = email
    if first_name is not None:
        user.first_name = first_name
    if last_name is not None:
        user.last_name = last_name
    if password is not None:
        user.set_password(password)

    user.save()
    return user