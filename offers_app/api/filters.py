import django_filters
from offers_app.models import Offer

class OfferFilter(django_filters.FilterSet):
    # ich muss creator_id mappen auf "user"
    creator_id = django_filters.NumberFilter(field_name='user')

    class Meta:
        model = Offer
        fields = ['creator_id']
