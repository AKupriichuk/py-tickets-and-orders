from typing import Optional, List, Dict

from django.db import transaction
from django.db.models import QuerySet
from datetime import datetime

from django.utils import timezone

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
    order_create_at = None
    if date:
        dt_naive = datetime.strptime(date, "%Y-%m-%d %H:%M")
        order_create_at = timezone.make_aware(dt_naive)
    order = Order.objects.create(
            user=user,
            created_at=order_create_at
            )
    for _ in tickets:
        movie_session = MovieSession.objects.get(id=_["movie_session"])

        Ticket.objects.create(
                order=order,
                movie_session=movie_session,
                row=_["row"],
                seat=_["seat"]
        )
    if order_create_at:
        aware_time = order.created_at
        order.created_at = aware_time.replace(tzinfo=None)
    return order


def get_orders(username: Optional[str] = None) -> QuerySet[Order, Order]:
    queryset = Order.objects.all()
    if username is not None:
        queryset = queryset.filter(user__username=username)

    return queryset
