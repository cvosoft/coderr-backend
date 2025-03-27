import django_filters
from offers_app.models import Offer
from django.db.models import Min


class OfferFilter(django_filters.FilterSet):
    # ich muss creator_id mappen auf "user"
    creator_id = django_filters.NumberFilter(field_name='user')

    # methoden basierter filter
    min_price = django_filters.NumberFilter(method='filter_min_price')

    class Meta:
        model = Offer
        fields = ['creator_id', 'min_price']

    def filter_min_price(self, queryset, name, value):
        return queryset.annotate(min_price=Min('details__price')).filter(min_price__gte=value)
