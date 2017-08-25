from django.db.models import Q

from openfruit.taxonomy.models import FruitingPlant
from openfruit.taxonomy.services import TAXONOMY_DAL
from openfruit.reports.event.services import EVENT_DAL
from openfruit.reports.review.services import FRUIT_REVIEW_DAL


class UserActivityDataAccessLayer:

    def get_all_plants_interacted_by(self, user):
        fruiting_plants = FruitingPlant.objects.filter(Q(eventreport__submitted_by=user) |
                                                       Q(created_by=user) |
                                                       Q(fruitreview__submitted_by=user))
        return sorted(fruiting_plants.select_related('species').distinct(), key=lambda x: x.get_name())

    def get_all_living_plants_interacted_by(self, user):
        return [plant for plant in self.get_all_plants_interacted_by(user) if plant.date_died is None]


USER_ACTIVITY_DAL = UserActivityDataAccessLayer()