from typing import Optional, List, Dict

from django.db import transaction
from django.db.models import QuerySet
from datetime import datetime

from db.models import Order, Ticket, User, MovieSession


@transaction.atomic
def create_order(
        tickets: List[Dict[str, int]],
        username: str,
        date: Optional[str] = None
) -> Order:
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        raise User.DoesNotExist("Username not found")
    order = Order.objects.create(user=user)
    if date:
        order.created_at = datetime.strptime(date, "%Y-%m-%d %H:%M")
        order.save()
    for _ in tickets:
        movie_session = MovieSession.objects.get(id=_["movie_session"])

        Ticket.objects.create(
            order=order,
            movie_session=movie_session,
            row=_["row"],
            seat=_["seat"]
        )
    return order


def get_orders(username: Optional[str] = None) -> QuerySet[Order, Order]:
    queryset = Order.objects.all()
    if username is not None:
        queryset = queryset.filter(user__username=username)

    return queryset
