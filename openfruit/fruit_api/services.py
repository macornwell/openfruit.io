from django.db import connection
from openfruit.taxonomy.models import RIPENING_MONTH_CHOICES, RIPENING_MODIFIER, FruitUsageType

class FruitAPIService:

    def full_cultivar_query(self, species_name, cultivar_name, addons=None, review_types=None, review_metrics=None):
        return self.full_cultivar_query_many([(species_name, cultivar_name)], addons=addons,
                                             review_types=review_types, review_metrics=review_metrics)

    def full_cultivar_query_many(self, species_and_cultivar_list, addons=None, review_types=None, review_metrics=None):
        """
        Queries a cultivar fully for all relevant information.
        :param species_name:
        :param cultivar_name:
        :return:
        """
        if not addons:
            addons = []
        if not review_types:
            review_types = [
            ]
        if not review_metrics:
            review_metrics = [
            ]

        query_selects = """
        SELECT c.*, c.name as cultivar_name, species.latin_name as species_latin_name,
        (SELECT TRUE
            FROM taxonomy_cultivar_uses as uses
            LEFT JOIN taxonomy_fruitusagetype usage_type on uses.fruitusagetype_id = usage_type.cultivar_usage_type_id
            WHERE uses.cultivar_id = c.cultivar_id and usage_type.type = 'Baking'
            limit 1
          ) as baking,
          (
            SELECT TRUE
            FROM taxonomy_cultivar_uses as uses
            LEFT JOIN taxonomy_fruitusagetype usage_type on uses.fruitusagetype_id = usage_type.cultivar_usage_type_id
            WHERE uses.cultivar_id = c.cultivar_id and usage_type.type = 'Cider'
            limit 1
          ) as cider,
          (
            SELECT TRUE
            FROM taxonomy_cultivar_uses as uses
            LEFT JOIN taxonomy_fruitusagetype usage_type on uses.fruitusagetype_id = usage_type.cultivar_usage_type_id
            WHERE uses.cultivar_id = c.cultivar_id and usage_type.type = 'Cooking'
            limit 1
          ) as cooking,
          (
            SELECT TRUE
            FROM taxonomy_cultivar_uses as uses
            LEFT JOIN taxonomy_fruitusagetype usage_type on uses.fruitusagetype_id = usage_type.cultivar_usage_type_id
            WHERE uses.cultivar_id = c.cultivar_id and usage_type.type = 'Drying'
            limit 1
          ) as drying,
          (
            SELECT TRUE
            FROM taxonomy_cultivar_uses as uses
            LEFT JOIN taxonomy_fruitusagetype usage_type on uses.fruitusagetype_id = usage_type.cultivar_usage_type_id
            WHERE uses.cultivar_id = c.cultivar_id and usage_type.type = 'Fresh Eating'
            limit 1
          ) as fresh_eating,
          (
            SELECT TRUE
            FROM taxonomy_cultivar_uses as uses
            LEFT JOIN taxonomy_fruitusagetype usage_type on uses.fruitusagetype_id = usage_type.cultivar_usage_type_id
            WHERE uses.cultivar_id = c.cultivar_id and usage_type.type = 'Preserves'
            limit 1
          ) as preserves,
          (
            SELECT TRUE
            FROM taxonomy_cultivar_uses as uses
            LEFT JOIN taxonomy_fruitusagetype usage_type on uses.fruitusagetype_id = usage_type.cultivar_usage_type_id
            WHERE uses.cultivar_id = c.cultivar_id and usage_type.type = 'Storage'
            limit 1
          ) as storage,"""

        query_from = """
        FROM taxonomy_cultivar as c """

        query_joins = """
        INNER JOIN taxonomy_species as species on species.species_id = c.species_id 
        INNER JOIN django_geo_db_location as location on location.location_id=c.origin_location_id """

        query_where = "WHERE "
        length = len(species_and_cultivar_list)
        for idx in range(length):
            query_where += """species.latin_name like %s and c.name like %s """
            if idx < length - 1:
                query_where += ' OR '

        query_group_bys = """
        GROUP BY
        c.name, 
        c.cultivar_id,"""

        if addons and 'review' in addons:
            if not review_types:
                review_types = [
                    'sweet',
                    'sour',
                    'firm',
                    'juicy',
                    'bitter',
                    'rating',
                ]
            if not review_metrics:
                review_metrics = [
                    'avg',
                    'max',
                    'min',
                ]

            for m in review_metrics:
                metric = self.__get_metric(m)
                for review_type in review_types:
                    query_segment = """
                        (SELECT {0}(review.{1}) as {2}
                        FROM review_fruitreview as review
                        left join taxonomy_cultivar cu on cu.cultivar_id = review.cultivar_id
                        where review.cultivar_id = c.cultivar_id
                        ) as {2},
                    """
                    query_segment = query_segment.format(metric, review_type, self.__get_review_key(metric, review_type))
                    query_selects += query_segment

        if addons and 'location' in addons:
            query_selects += """
            city.name as city_name, county.name as county_name, 
            state.name as state_name, country.name as country_name,
            map.map_file_url as map_file_url,
            zipcode.zipcode,
            county_g.generated_name as county_geo,
            state_g.generated_name as state_geo,
            zipcode_g.generated_name as zipcode_geo,
            location_g.generated_name as location_geo,
            country_g.generated_name as country_geo,
            city_g.generated_name as city_geo,"""

            query_joins += """
            LEFT JOIN django_geo_db_state as state on location.state_id = state.state_id
            LEFT JOIN django_geo_db_country as country on location.country_id = country.country_id
            LEFT JOIN django_geo_db_county as county on location.county_id=county.county_id
            LEFT JOIN django_geo_db_city as city on location.city_id = city.city_id
            LEFT JOIN django_geo_db_zipcode as zipcode on location.city_id = zipcode.zipcode
            LEFT JOIN django_geo_db_geocoordinate as state_g on state.geocoordinate_id = state_g.geocoordinate_id
            LEFT JOIN django_geo_db_geocoordinate as county_g on county.geocoordinate_id = county_g.geocoordinate_id
            LEFT JOIN django_geo_db_geocoordinate as country_g on country.geocoordinate_id = country_g.geocoordinate_id
            LEFT JOIN django_geo_db_geocoordinate as location_g on location.geocoordinate_id = country_g.geocoordinate_id
            LEFT JOIN django_geo_db_geocoordinate as city_g on city.geocoordinate_id = city_g.geocoordinate_id
            LEFT JOIN django_geo_db_geocoordinate as zipcode_g on zipcode.geocoordinate_id = zipcode_g.geocoordinate_id
            LEFT JOIN django_geo_db_locationmap as map on location.location_id = map.location_id """

            query_group_bys += """
            map.location_map_id,
            state_g.geocoordinate_id,
            county_g.geocoordinate_id,
            country_g.geocoordinate_id,
            location_g.geocoordinate_id,
            city_g.geocoordinate_id,
            zipcode_g.geocoordinate_id,"""

        full_query = self.__preprocess_query_segment(query_selects)
        full_query += self.__preprocess_query_segment(query_from)
        full_query += self.__preprocess_query_segment(query_joins)
        full_query += self.__preprocess_query_segment(query_where)
        full_query += self.__preprocess_query_segment(query_group_bys)

        value_list = []
        for species, cultivar in species_and_cultivar_list:
            value_list.append(species)
            value_list.append(cultivar)
        results = []
        with connection.cursor() as cursor:
            cursor.execute(full_query, value_list)
            columns = [col[0] for col in cursor.description]
            rows = cursor.fetchall()
            for r in rows:
                inner_result = {}
                for idx in range(len(columns)):
                    c = columns[idx]
                    val = r[idx]
                    inner_result[c] = val
                results.append(inner_result)

        final_result = []
        for result in results:
            data = {
                'cultivar_id': result['cultivar_id'],
                'name': result['cultivar_name'],
                'generated_name': result['generated_name'],
                'ripens_early_mod': self.__parse_mod(result['ripens_early_mod']),
                'ripens_late_mod': self.__parse_mod(result['ripens_late_mod']),
                'ripens_late': self.__parse_month(result['ripens_late']),
                'ripens_early': self.__parse_month(result['ripens_early']),
                'latin_name': result['species_latin_name'],
                'origin_year': result['origin_year'],
                'brief_description': result['brief_description'],
                'chromosome_count': result['chromosome_count'],
                'uses': self.__parse_uses(result),
            }
            if 'location' in addons:
                data['location'] = self.__parse_location(result)
            if 'review' in addons:
                data['review'] = self.__parse_review(review_types, review_metrics, result)
            final_result.append(data)
        return final_result

    def __parse_uses(self, result):
        uses = []
        if result['drying']:
            uses.append('Drying')
        if result['baking']:
            uses.append('Baking')
        if result['cooking']:
            uses.append('Cooking')
        if result['preserves']:
            uses.append('Preserves')
        if result['fresh_eating']:
            uses.append('Fresh Eating')
        if result['storage']:
            uses.append('Storage')
        if result['cider']:
            uses.append('Cider')
        return uses

    def __parse_location(self, result):
        data = {
            'country': result['country_name'],
            'state': result['state_name'],
            'county': result['county_name'],
            'city': result['city_name'],
            'zipcode': result['zipcode'],
            'geocoordinate': self.__parse_coordinate(result),
            'map_file_url': result['map_file_url'],
        }
        return data

    def __get_metric(self, metric_friendly):
        metric = ''
        if metric_friendly == 'avg':
            metric = 'AVG'
        elif metric_friendly == 'max':
            metric = 'MAX'
        elif metric_friendly == 'min':
            metric = 'MIN'
        else:
            raise Exception('Unknown review_metric: ' + str(metric_friendly))
        return metric

    def __get_review_key(self, metric, review_type):
        return '{0}_{1}'.format(metric, review_type)

    def __parse_review(self, review_types, review_metrics, result):
        data = {}
        for metric in review_metrics:
            metric_db = self.__get_metric(metric)
            data[metric] = {}
            for r_type in review_types:
                key = self.__get_review_key(metric_db, r_type)
                data[metric][r_type.lower()] = self.__parse_float(result[key])
        return data

    def __preprocess_query_segment(self, segment):
        if segment.endswith(','):
            segment = segment[0:-1]
        return segment + ' '

    def __parse_mod(self, value):
        for key, val in RIPENING_MODIFIER:
            if value == key:
                return val
        return None

    def __parse_month(self, month_number):
        for key, val in RIPENING_MONTH_CHOICES:
            if month_number == key:
                return val
        return None

    def __parse_coordinate(self, result):
        values_in_order = [
            'location_geo',
            'zipcode_geo',
            'city_geo',
            'county_geo',
            'state_geo',
            'country_geo',
        ]
        for value in values_in_order:
            val = result[value]
            if val:
                return val
        return None

    def __parse_float(self, value):
        if value:
            return float(value)
        else:
            return None

FRUIT_API_SERVICE = FruitAPIService()