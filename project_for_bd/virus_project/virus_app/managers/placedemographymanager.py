from django.db import models
from ..models import *
from django_countries import countries

class PlaceDemographyManager(models.Manager):
    region_choices = (
        ('СА', 'Северная Америка'),
        ('ЮА', 'Южная Америка'),
        ('Аф', 'Африка'),
        ('Е', 'Европа'),
        ('Аз', 'Азия'),
        ('Ав', 'Австралия'),
        ('Ан', 'Антарктида'),
    )

    def get_places_demography_by_epidemic_pk(self, epidemic_pk):
        return self.filter(epidemic__pk=epidemic_pk)


    class Region:
        def __init__(self, name, period_from, period_to, infected, dead, recovered, population):
            self.name = name
            self.period_from = period_from
            self.period_to = period_to
            self.infected = infected
            self.dead = dead
            self.recovered = recovered
            self.population = population

    class Country:
        def __init__(self, name, period_from, period_to, infected, dead, recovered, population):
            self.name = name
            self.period_from = period_from
            self.period_to = period_to
            self.infected = infected
            self.dead = dead
            self.recovered = recovered
            self.population = population

    class Town:
        def __init__(self, name, period_from, period_to, infected, dead, recovered, population):
            self.name = name
            self.period_from = period_from
            self.period_to = period_to
            self.infected = infected
            self.dead = dead
            self.recovered = recovered
            self.population = population

    def get_long_name_by_short(self, short_name, names_dict):
        for pair in names_dict:
            if pair[0] == short_name:
                return pair[1]

    def get_regions_by_epidemic_pk(self, epidemic_pk):
        query = '''select min(dem.dem_id) as id, dem.ep_id as ep_id, dem.region,
		 sum(dem.population) as population, sum(dem.infected) as infected,
		 sum(dem.recovered) as recovered, sum(dem.dead) as dead,
		 min(dem.date_from) as date_from, max(dem.date_to) as date_to
		 from (
			select min(dem.dem_id) as dem_id, dem.ep_id as ep_id, dem.region, dem.country, dem.town,
				 max(dem.population) as population, max(dem.infected) as infected,
				 max(dem.recovered) as recovered, max(dem.dead) as dead,
				 min(dem.date_from) as date_from, max(dem.date_to) as date_to
				 from (
				 select dem.id as dem_id,
				 place.region as region,
				 place.country as country,
				 place.town as town,
				 place.population as population,
				 dem.infected as infected,
				 dem.recovered as recovered,
				 dem.dead as dead,
				 dem.epidemic_id as ep_id,
				 per.date_from as date_from,
				 per.date_to as date_to
				 from virus_app_placedemography as dem
				 JOIN virus_app_place as place on dem.place_id = place.id
				 JOIN virus_app_period as per on dem.period_id = per.id
				 where dem.epidemic_id = %s) as dem
			group by dem.ep_id, dem.region, dem.country, dem.town) as dem
group by dem.ep_id, dem.region;''' % epidemic_pk

        lst = self.raw(query)

        for raw in lst:
            raw.full_region = self.get_long_name_by_short(raw.region, self.region_choices)
        return lst

        #regions = self.Region(name, period_from, period_to, infected, dead, recovered, population)
        #return regions

    def get_countries_by_region_pk(self, epidemic_id, region_name):
        query = '''select min(dem.dem_id) as id, dem.ep_id as ep_id, dem.region, dem.country,
                 sum(dem.population) as population, sum(dem.infected) as infected,
                 sum(dem.recovered) as recovered, sum(dem.dead) as dead,
                 min(dem.date_from) as date_from, max(dem.date_to) as date_to
                 from (
                    select min(dem.dem_id) as dem_id, dem.ep_id as ep_id, dem.region, dem.country, dem.town,
                         max(dem.population) as population, max(dem.infected) as infected,
                         max(dem.recovered) as recovered, max(dem.dead) as dead,
                         min(dem.date_from) as date_from, max(dem.date_to) as date_to
                         from (
                         select dem.id as dem_id,
                         place.region as region,
                         place.country as country,
                         place.town as town,
                         place.population as population,
                         dem.infected as infected,
                         dem.recovered as recovered,
                         dem.dead as dead,
                         dem.epidemic_id as ep_id,
                         per.date_from as date_from,
                         per.date_to as date_to
                         from virus_app_placedemography as dem
                         JOIN virus_app_place as place on dem.place_id = place.id
                         JOIN virus_app_period as per on dem.period_id = per.id
                         where dem.epidemic_id = %s and place.region='%s') as dem
                    group by dem.ep_id, dem.region, dem.country, dem.town) as dem
        group by dem.ep_id, dem.region, dem.country;''' % (epidemic_id, region_name)
        lst = self.raw(query)

        for raw in lst:
            raw.full_country = dict(countries)[raw.country]

        return lst

        #regions = self.Country(name, period_from, period_to, infected, dead, recovered, population)
        #return regions

    def get_towns_by_country_pk(self, epidemic_id, region_name, country_name):
        query = '''select min(dem.dem_id) as id, dem.ep_id as ep_id, dem.region, dem.country, dem.town,
                max(dem.population) as population, max(dem.infected) as infected,
                max(dem.recovered) as recovered, max(dem.dead) as dead,
                min(dem.date_from) as date_from, max(dem.date_to) as date_to
                from (
                select dem.id as dem_id,
                place.region as region,
                place.country as country,
                place.town as town,
                place.population as population,
                dem.infected as infected,
                dem.recovered as recovered,
                dem.dead as dead,
                dem.epidemic_id as ep_id,
                per.date_from as date_from,
                per.date_to as date_to
                from virus_app_placedemography as dem
                JOIN virus_app_place as place on dem.place_id = place.id
                JOIN virus_app_period as per on dem.period_id = per.id
                where dem.epidemic_id = %s and place.region='%s' and place.country='%s') as dem
                group by dem.ep_id, dem.region, dem.country, dem.town;''' % (epidemic_id, region_name, country_name)
        return self.raw(query)



    def get_current_region_sql(self, epidemic_pk, region_name):
        query = '''select min(dem.id) as id,
                     dem.epidemic_id as ep_id,
                     place.region as region,
                     sum(place.population) as population,
                     sum(dem.infected) as infected,
                     sum(dem.recovered) as recovered,
                     sum(dem.dead) as dead,
                     per.date_from as date_from,
                     per.date_to as date_to
                from virus_app_placedemography as dem
                JOIN virus_app_place as place on dem.place_id = place.id
                JOIN virus_app_period as per on dem.period_id = per.id
                where dem.epidemic_id = %s and place.region='%s'
                group by dem.epidemic_id, place.region, date_from, date_to
                order by date_from
        ''' % (epidemic_pk, region_name)
        return self.raw(query)


    def get_current_country_sql(self, epidemic_pk, region_name, country_name):
        query = '''select min(dem.id) as id,
                     dem.epidemic_id as ep_id,
                     place.region as region,
                     place.country as country,
                     sum(place.population) as population,
                     sum(dem.infected) as infected,
                     sum(dem.recovered) as recovered,
                     sum(dem.dead) as dead,
                     per.date_from as date_from,
                     per.date_to as date_to
                from virus_app_placedemography as dem
                JOIN virus_app_place as place on dem.place_id = place.id
                JOIN virus_app_period as per on dem.period_id = per.id
                where dem.epidemic_id = %s and place.region='%s' and place.country='%s'
                group by dem.epidemic_id, place.region, place.country, date_from, date_to
                order by date_from
        ''' % (epidemic_pk, region_name, country_name)
        return self.raw(query)

    def get_current_town_sql(self, epidemic_pk, region_name, country_name, town_name):
        query = '''select dem.id as id,
                         place.region as region,
                         place.country as country,
                         place.town as town,
                         place.population as population,
                         dem.infected as infected,
                         dem.recovered as recovered,
                         dem.dead as dead,
                         dem.epidemic_id as ep_id,
                         per.date_from as date_from,
                         per.date_to as date_to
                    from virus_app_placedemography as dem
                    JOIN virus_app_place as place on dem.place_id = place.id
                    JOIN virus_app_period as per on dem.period_id = per.id
                    where dem.epidemic_id = %s and place.region='%s' and place.country='%s' and place.town='%s'
                    order by per.date_from
        ''' % (epidemic_pk, region_name, country_name, town_name)
        return self.raw(query)
