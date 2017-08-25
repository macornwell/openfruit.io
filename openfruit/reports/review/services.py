from openfruit.reports.review.models import FruitReview

class FruitReviewDataAccessLayer:

    def get_all_fruiting_plants_reviewed_by(self, user):
        return FruitReview.objects.filter(submitted_by=user).values('fruiting_plant').distinct()


FRUIT_REVIEW_DAL = FruitReviewDataAccessLayer()
