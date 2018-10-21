from django.db import connection
from openfruit.taxonomy.models import RIPENING_MONTH_CHOICES, RIPENING_MODIFIER


class FruitAPIService:
    """
    Provides services for the Fruit API

    Cultivar Data Structure
    {
        'cultivar_id': 0,
        'name': 'Red Delicious',
        'generated_name': 'Red Delicious (Apple)',
        'ripens_early_mod': 'Early',
        'ripens_late_mod': 'Late',
        'ripens_early': 9,
        'ripens_late': 10,
        'latin_name': 'Malus domestica',
        'origin_year': 1980,
        'brief_description': 'A brief description',
        'chromosome_count': 3,
        'uses': [
            'Drying',
            'Fresh Eating',
            'Preserves',
        ],
        'location': {
            'country': 'United States',
            'state': 'Virginia',
            'county': 'Montgomery County',
            'city': 'Blacksburg',
            'zipcode': 24060,
            'region': None,
            'geocoordinate': 30.123 -90.1234,
            'map_file_url': 'http://xyz.com',
        },
        'resistances': {
            'Cedar Apple Rust',
        }

    }
    """

    def full_cultivar_query(self, species_name, cultivar_name, addons=None, review_types=None, review_metrics=None):
        """
        Queries for a single cultivar.
        :param species_name: The species name.
        :param cultivar_name:  The cultivar name.
        :param addons: Array with the desired results. ['location','review','resistances']
        :param review_types: Array with the desired review types. ['sweet','sour','firm','bitter','juicy','rating']
        :param review_metrics: Array with desired metric types. ['avg','max','min']
        :return: A single cultivar result. See above.
        """
        as_list = self.full_cultivar_query_many([(species_name, cultivar_name)], addons=addons,
                                             review_types=review_types, review_metrics=review_metrics)
        if len(as_list):
            return as_list[0]
        return None

    def full_cultivar_query_many(self, species_and_cultivar_list, addons=None, review_types=None, review_metrics=None):
        """
        Queries for many cultivars.
        :param species_and_cultivar_list: Tuple pairs inside a list. ('Malus domestica', 'Red Delicious')
        :param addons: Array with the desired results. ['location','review','resistances']
        :param review_types: Array with the desired review types. ['sweet','sour','firm','bitter','juicy','rating']
        :param review_metrics: Array with desired metric types. ['avg','max','min']
        :return: Multiple cultivar results. See above.
        """

        def get_params():
            value_list = []
            for species, cultivar in species_and_cultivar_list:
                value_list.append(species)
                value_list.append(cultivar)
            return value_list

        def get_where_clause():
            query_where = "WHERE "
            length = len(species_and_cultivar_list)
            for idx in range(length):
                query_where += """species.latin_name like %s and c.name like %s """
                if idx < length - 1:
                    query_where += ' OR '
            return query_where

        return self._query_generic(get_where_clause, get_params, addons=addons, review_types=review_types, review_metrics=review_metrics)

    def full_cultivar_query_geo(self, country, region=None, state=None, city=None, county=None,
                                species=None, addons=None, review_types=None, review_metrics=None):
        """
        Queries for many cultivars inside of a geographic space.
        :param country: The country where the cultivar originates.
        :param region: The region where the cultivar originates.
        :param state: The state where the cultivar originates.
        :param county: The county where the cultivar originates.
        :param species: The species of plant.
        :param addons: Array with the desired results. ['location','review','resistances']
        :param review_types: Array with the desired review types. ['sweet','sour','firm','bitter','juicy','rating']
        :param review_metrics: Array with desired metric types. ['avg','max','min']
        :return: Multiple cultivar results. See above.
        """
        def get_params():
            value_list = []
            value_list.append(country.name)
            if region:
                value_list.append(region.name)
            if state:
                value_list.append(state.name)
            if county:
                value_list.append(county.name)
            if city:
                value_list.append(city.name)
            if species:
                value_list.append(species.latin_name)
            return value_list

        def get_where_clause():
            query_where = "WHERE country.name like %s "
            if region:
                query_where += " AND region.name like %s "
            if state:
                query_where += " AND state.name like %s "
            if county:
                query_where += " AND county.name like %s "
            if city:
                query_where += " AND city.name like %s "
            if species:
                query_where += " AND species.latin_name like %s "
            return query_where
        return self._query_generic(get_where_clause, get_params, addons=addons, review_types=review_types, review_metrics=review_metrics)

    def _query_generic(self, get_where_clause, get_query_params, addons=None, review_types=None, review_metrics=None):
        if not get_where_clause:
            raise Exception('get_where_clause')
        if not get_query_params:
            raise Exception('get_query_params')

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

        query_where = get_where_clause()

        query_joins = """
        INNER JOIN taxonomy_species as species on species.species_id = c.species_id 
        INNER JOIN django_geo_db_location as location on location.location_id=c.origin_location_id """

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
            state.name as state_name, country.name as country_name, region.name as region_name,
            map.map_file_url as map_file_url,
            zipcode.zipcode,
            county_g.generated_name as county_geo,
            region_g.generated_name as region_geo,
            state_g.generated_name as state_geo,
            zipcode_g.generated_name as zipcode_geo,
            location_g.generated_name as location_geo,
            country_g.generated_name as country_geo,
            city_g.generated_name as city_geo,"""

            query_joins += """
            LEFT JOIN django_geo_db_state as state on location.state_id = state.state_id
            LEFT JOIN django_geo_db_country as country on location.country_id = country.country_id
            LEFT JOIN django_geo_db_region as region on location.region_id = region.region_id
            LEFT JOIN django_geo_db_county as county on location.county_id=county.county_id
            LEFT JOIN django_geo_db_city as city on location.city_id = city.city_id
            LEFT JOIN django_geo_db_zipcode as zipcode on location.city_id = zipcode.zipcode
            LEFT JOIN django_geo_db_geocoordinate as state_g on state.geocoordinate_id = state_g.geocoordinate_id
            LEFT JOIN django_geo_db_geocoordinate as county_g on county.geocoordinate_id = county_g.geocoordinate_id
            LEFT JOIN django_geo_db_geocoordinate as country_g on country.geocoordinate_id = country_g.geocoordinate_id
            LEFT JOIN django_geo_db_geocoordinate as region_g on region.geocoordinate_id = region_g.geocoordinate_id
            LEFT JOIN django_geo_db_geocoordinate as location_g on location.geocoordinate_id = country_g.geocoordinate_id
            LEFT JOIN django_geo_db_geocoordinate as city_g on city.geocoordinate_id = city_g.geocoordinate_id
            LEFT JOIN django_geo_db_geocoordinate as zipcode_g on zipcode.geocoordinate_id = zipcode_g.geocoordinate_id
            LEFT JOIN django_geo_db_locationmap as map on location.location_id = map.location_id 
            LEFT JOIN django_geo_db_locationmaptype as map_type on map.type_id = map_type.location_map_type_id
            """
            query_where = "WHERE map_type.type = 'simple' AND (" + query_where[len("WHERE "):] + ")"

            query_group_bys += """
            map.location_map_id,
            state_g.geocoordinate_id,
            county_g.geocoordinate_id,
            region_g.geocoordinate_id,
            country_g.geocoordinate_id,
            location_g.geocoordinate_id,
            city_g.geocoordinate_id,
            map_type.location_map_type_id,
            zipcode_g.geocoordinate_id,"""

        if 'resistances' in addons:
            query_selects += """
            (SELECT TRUE
            FROM disease_diseaseresistancereport AS disease
            LEFT JOIN disease_diseasetype disease_type ON disease.disease_type_id = disease_type.disease_type_id
            WHERE disease.resistance_level = 'e'
                  AND disease.cultivar_id = c.cultivar_id
                  AND disease_type.type = 'Cedar Apple Rust'
            LIMIT 1
          ) AS car_resistance,
          (
            SELECT TRUE
            FROM disease_diseaseresistancereport AS disease
            LEFT JOIN disease_diseasetype disease_type ON disease.disease_type_id = disease_type.disease_type_id
            WHERE disease.resistance_level = 'e'
                  AND disease.cultivar_id = c.cultivar_id
                  AND disease_type.type = 'Fireblight'
            LIMIT 1
          ) AS fireblight_resistance 
          """

        full_query = self.__preprocess_query_segment(query_selects)
        full_query += self.__preprocess_query_segment(query_from)
        full_query += self.__preprocess_query_segment(query_joins)
        full_query += self.__preprocess_query_segment(query_where)
        full_query += self.__preprocess_query_segment(query_group_bys)

        value_list = [p for p in get_query_params()]

        results = []
        print(full_query)
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
            if 'resistances' in addons:
                data['resistances'] = self.__parse_resistances(result)
            final_result.append(data)
        return final_result

    def __parse_resistances(self, result):
        resistances = []
        if result['fireblight_resistance']:
            resistances.append('Fireblight')
        if result['car_resistance']:
            resistances.append('Cedar Apple Rust')
        return resistances

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
            'region': result['region_name'],
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
            'region_geo',
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
