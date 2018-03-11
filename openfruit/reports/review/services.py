from django.db.models import Q, Avg, Max, Min
from openfruit.reports.review.models import FruitReview
from openfruit.taxonomy.services import TAXONOMY_DAL


class FruitReviewDataAccessLayer:


    def __get_average(self, cultivar, field):
        reviews = FruitReview.objects.filter(Q(fruiting_plant__cultivar=cultivar) | Q(cultivar=cultivar))
        #average = reviews.aggregate(Avg(field), Max(field), Min(field))
        values = [
            Avg('bitter'),
            Avg('sweet'),
            Max('bitter'),
            Avg('sweet'),
        ]
        average = reviews.aggregate(*values)
        return average

    def __get_max(self, cultivar, field):
        reviews = FruitReview.objects.filter(Q(fruiting_plant__cultivar=cultivar) | Q(cultivar=cultivar))
        average = reviews.aggregate(Max(field))
        return average

    def __get_min(self, cultivar, field):
        reviews = FruitReview.objects.filter(Q(fruiting_plant__cultivar=cultivar) | Q(cultivar=cultivar))
        average = reviews.aggregate(Min(field))
        return average

    def get_all_fruiting_plants_reviewed_by(self, user):
        return FruitReview.objects.filter(submitted_by=user).values('fruiting_plant').distinct()

    def get_averages_for_cultivar(self, species, cultivar_name, types=None, metrics=None):
        """
        Gets the averages for a particular cultivar.
        If no parameters are provided for mins, maxes and averages everything is returned. (Not generally recommended)
        If any parameter is supplied, ONLY that value will be calculated and returned.
        :param species:
        :param cultivar_name:
        :param mins:
        :param maxes:
        :param averages:
        :return:
        """
        possible_types = [
            'sweet',
            'sour',
            'firm',
            'bitter',
            'juicy',
            'rating',
        ]
        cultivar = TAXONOMY_DAL.get_cultivar(species, cultivar_name)
        if not cultivar:
            raise Exception('No cultivar found')
        do_average = False
        do_max = False
        do_min = False
        if not types:
            types = list(possible_types)
        if not metrics:
            do_average = True
            do_max = True
            do_min = True
        else:
            for metric in metrics:
                if metric.lower() == 'average':
                    do_average = True
                elif metric.lower() == 'max':
                    do_max = True
                elif metric.lower() == 'min':
                    do_min = True

        queries = []
        for type in types:
            if do_average:
                queries.append(Avg(type))
            if do_max:
                queries.append(Max(type))
            if do_min:
                queries.append(Min(type))
        reviews = FruitReview.objects.filter(Q(fruiting_plant__cultivar=cultivar) | Q(cultivar=cultivar))
        result = reviews.aggregate(*queries)
        results = {}
        for key in result:
            typeKey, metric = key.split('__')
            if metric not in results:
                results[metric] = {}
            results[metric][typeKey] = result[key]
        return results


FRUIT_REVIEW_DAL = FruitReviewDataAccessLayer()
