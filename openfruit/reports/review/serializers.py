from rest_framework import serializers
from openfruit.reports.review import models


class FruitReviewSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = models.FruitReview
        fields = ('fruit_review_report_id', 'submitted_by', 'datetime', 'fruiting_plant', 'cultivar',
                  'sweet', 'sour', 'bitter', 'juicy', 'firm', 'was_picked_early', 'rating', 'text')

