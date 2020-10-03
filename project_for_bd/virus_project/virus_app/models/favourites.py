from django.db import models
from .virus import Virus
from django_countries.fields import CountryField
from .placedemography import PlaceDemography
import copy

class RegionManager(models.Manager):
    def get_regions_by_username(self, username):
        return self.filter(favourite__profile__user__username=username)

class CountryManager(models.Manager):
    def get_countries_by_username(self, username):
        return self.filter(favourite__profile__user__username=username)

class TownManager(models.Manager):
    def get_towns_by_username(self, username):
        return self.filter(favourite__profile__user__username=username)


class FavouritesManager(models.Manager):

    def get_all_viruses_by_username(self, username):
        query = self.get(profile__user__username=username)
        return query.virus.all()


    def get_all_epidemics_by_username(self, username):
        query = self.get(profile__user__username=username)
        return query.epidemic.all()

    def get_all_regions_by_username(self, username):
        res = []
        #favourite = self.get(profile__user__username=username)
        favourite_regions = Region.objects.get_regions_by_username(username=username)
        #проходим по всем именам регионов, которые есть в избранном
        for region in favourite_regions:
            # находим все регионы, у которых epidemic_pk совпадает с epidemic_pk из favourite.region
            sql_regions = PlaceDemography.objects.get_regions_by_epidemic_pk(region.epidemic_id)
            # проходим по всем регионам из sql запроса
            for sql_region in sql_regions:
                if sql_region.region == region.region:
                    res.append(sql_region)
        return res

    def get_all_countries_by_username(self, username):
        res = []
        #favourite = self.get(profile__user__username=username)
        favourite_countries = Country.objects.get_countries_by_username(username=username)
        # проходим по всем именам регионов, которые есть в избранном
        for country in favourite_countries:
            # находим все регионы, у которых epidemic_pk совпадает с epidemic_pk из favourite.region
            sql_countries = PlaceDemography.objects.get_countries_by_region_pk(country.epidemic_id, country.region)
            # проходим по всем регионам из sql запроса
            for sql_country in sql_countries:
                if sql_country.country == country.country:
                    res.append(sql_country)
        return res

    def get_all_towns_by_username(self, username):
        res = []
        #favourite = self.get(profile__user__username=username)
        favourite_towns = Town.objects.get_towns_by_username(username=username)
        # проходим по всем именам регионов, которые есть в избранном
        for town in favourite_towns:
            # находим все регионы, у которых epidemic_pk совпадает с epidemic_pk из favourite.region
            sql_towns = PlaceDemography.objects.get_towns_by_country_pk(town.epidemic_id, town.region, town.country)
            # проходим по всем регионам из sql запроса
            for sql_town in sql_towns:
                if sql_town.town == town.town:
                    res.append(sql_town)
        return res

    def add_region(self, epidemic_pk, region_name, user):
        region = Region()
        region.epidemic_id = epidemic_pk
        region.region = region_name
        region.favourite = user.profile.favourite
        region.save()

    def delete_region(self, epidemic_pk, region_name, username):
        Region.objects.filter(epidemic_id=epidemic_pk).filter(region=region_name).filter(favourite__profile__user__username=username).delete()

    def add_country(self, epidemic_pk, region_name, country_name, user):
        country = Country()
        country.epidemic_id = epidemic_pk
        country.region = region_name
        country.country = country_name
        country.favourite = user.profile.favourite
        country.save()

    def delete_country(self, epidemic_pk, region_name, country_name, username):
        Country.objects.filter(epidemic_id=epidemic_pk).filter(region=region_name).filter(country=country_name).filter(favourite__profile__user__username=username).delete()

    def add_town(self, epidemic_pk, region_name, country_name, town_name, user):
        town = Town()
        town.epidemic_id = epidemic_pk
        town.region = region_name
        town.country = country_name
        town.town = town_name
        town.favourite = user.profile.favourite
        town.save()

    def delete_town(self, epidemic_pk, region_name, country_name, town_name, username):
        Town.objects.filter(epidemic_id=epidemic_pk).filter(region=region_name).filter(country=country_name).filter(town=town_name).filter(favourite__profile__user__username=username).delete()

    def delete_all_regions(self):
        Region.objects.filter().delete()

    def delete_all_countries(self):
        Country.objects.filter().delete()

    def delete_all_towns(self):
        Town.objects.filter().delete()

    def create_names_for_regions(self, regions_info, region_infected):
        for region_info in regions_info:
            region_infected[0].append(region_info[1])
        return region_infected

    def create_names_for_countries(self, countries_info, country_infected):
        for country_info in countries_info:
            country_infected[0].append(country_info[2])
        return country_infected

    def create_names_for_towns(self, towns_info, town_infected):
        for town_info in towns_info:
            town_infected[0].append(town_info[3])
        return town_infected

    def create_dates_for_lst(self, query, lst):
        regions_count = len(lst[0])
        for raw in query:
            raw_in_lst = [0 for i in range(regions_count)]
            raw_in_lst[0] = str(raw.date_to)
            lst.append(raw_in_lst)
        return lst

    def create_values_for_lst(self, query, lst):
        regions_count = len(lst[0])
        iter = 1
        for raw in query:
            raw_in_lst = [0 for i in range(regions_count)]
            raw_in_lst[0] = str(iter)
            lst.append(raw_in_lst)
            iter += 1
        return lst

    def get_date_region_graphics_data(self, regions_info):
        region_infected = [['Года']]

        region_infected = self.create_names_for_regions(regions_info, region_infected)
        first_region_query = PlaceDemography.objects.get_current_region_sql(epidemic_pk=regions_info[0][0],
                                                                            region_name=regions_info[0][1])

        region_infected = self.create_dates_for_lst(first_region_query, region_infected)

        region_recovered = copy.deepcopy(region_infected)
        region_dead = copy.deepcopy(region_infected)

        region_iter = 1
        for region_info in regions_info:
            query = PlaceDemography.objects.get_current_region_sql(epidemic_pk=region_info[0],
                                                                   region_name=region_info[1])
            raw_iter = 1
            for raw in query:
                population = raw.population
                region_infected[raw_iter][region_iter] = float(raw.infected) / float(population)
                region_recovered[raw_iter][region_iter] = float(raw.recovered) / float(population)
                region_dead[raw_iter][region_iter] = float(raw.dead) / float(population)
                raw_iter += 1
            region_iter += 1

        return [region_infected, region_recovered, region_dead]

    def get_max_values_region(self,  regions_info):

        queries = []
        max_values_region_query = PlaceDemography.objects.get_current_region_sql(epidemic_pk=regions_info[0][0],
                                                                   region_name=regions_info[0][1])

        for region_info in regions_info:
            query = PlaceDemography.objects.get_current_region_sql(epidemic_pk=region_info[0],
                                                                   region_name=region_info[1])
            queries.append(query)
            if (len(max_values_region_query) < len(query)):
                max_values_region_query = query

        return max_values_region_query, queries

    def get_region_graphics_data(self, regions_info):
        region_infected = [['Динамика']]

        region_infected = self.create_names_for_regions(regions_info, region_infected)
        max_values_region_query, queries = self.get_max_values_region(regions_info)

        region_infected = self.create_values_for_lst(max_values_region_query, region_infected)

        region_recovered = copy.deepcopy(region_infected)
        region_dead = copy.deepcopy(region_infected)

        region_iter = 1
        for query in queries:
            # определение шага, через который будут записываться не None значения
            h = int(len(max_values_region_query) / len(query))
            raw_iter = 1
            for raw in query:
                if ((raw_iter - 1) % h == 0):
                    population = raw.population
                    region_infected[raw_iter][region_iter] = float(raw.infected) / float(population)
                    region_recovered[raw_iter][region_iter] = float(raw.recovered) / float(population)
                    region_dead[raw_iter][region_iter] = float(raw.dead) / float(population)
                else:
                    region_infected[raw_iter][region_iter] = None
                    region_recovered[raw_iter][region_iter] = None
                    region_dead[raw_iter][region_iter] = None
                raw_iter += 1
            region_iter += 1

        return [region_infected, region_recovered, region_dead], self.get_date_region_graphics_data(regions_info)



    def get_date_country_graphics_data(self, countries_info):
        country_infected = [['Года']]

        country_infected = self.create_names_for_countries(countries_info, country_infected)
        first_country_query = PlaceDemography.objects.get_current_country_sql(epidemic_pk=countries_info[0][0],
                                                                              region_name=countries_info[0][1],
                                                                              country_name=countries_info[0][2])

        country_infected = self.create_dates_for_lst(first_country_query, country_infected)

        country_recovered = copy.deepcopy(country_infected)
        country_dead = copy.deepcopy(country_infected)

        country_iter = 1
        for country_info in countries_info:
            query = PlaceDemography.objects.get_current_country_sql(epidemic_pk=country_info[0],
                                                                    region_name=country_info[1],
                                                                    country_name=country_info[2])
            raw_iter = 1
            for raw in query:
                population = raw.population
                country_infected[raw_iter][country_iter] = float(raw.infected) / float(population)
                country_recovered[raw_iter][country_iter] = float(raw.recovered) / float(population)
                country_dead[raw_iter][country_iter] = float(raw.dead) / float(population)
                raw_iter += 1
            country_iter += 1

        return [country_infected, country_recovered, country_dead]


    def get_max_values_country(self, countries_info):

        queries = []
        max_values_country_query = PlaceDemography.objects.get_current_country_sql(epidemic_pk=countries_info[0][0],
                                                                   region_name=countries_info[0][1],
                                                                    country_name=countries_info[0][2])

        for country_info in countries_info:
            query = PlaceDemography.objects.get_current_country_sql(epidemic_pk=country_info[0],
                                                                   region_name=country_info[1],
                                                                    country_name=country_info[2])
            queries.append(query)
            if (len(max_values_country_query) < len(query)):
                max_values_country_query = query

        return max_values_country_query, queries

    def get_country_graphics_data(self, countries_info):
        country_infected = [['Динамика']]

        country_infected = self.create_names_for_countries(countries_info, country_infected)
        max_values_country_query, queries = self.get_max_values_country(countries_info)

        country_infected = self.create_values_for_lst(max_values_country_query, country_infected)

        country_recovered = copy.deepcopy(country_infected)
        country_dead = copy.deepcopy(country_infected)

        region_iter = 1
        for query in queries:
            # определение шага, через который будут записываться не None значения
            h = int(len(max_values_country_query) / len(query))
            raw_iter = 1
            for raw in query:
                if ((raw_iter - 1) % h == 0):
                    population = raw.population
                    country_infected[raw_iter][region_iter] = float(raw.infected) / float(population)
                    country_recovered[raw_iter][region_iter] = float(raw.recovered) / float(population)
                    country_dead[raw_iter][region_iter] = float(raw.dead) / float(population)
                else:
                    country_infected[raw_iter][region_iter] = None
                    country_recovered[raw_iter][region_iter] = None
                    country_dead[raw_iter][region_iter] = None
                raw_iter += 1
            region_iter += 1

        return [country_infected, country_recovered, country_dead], self.get_date_country_graphics_data(countries_info)

    def get_date_town_graphics_data(self, towns_info):
        town_infected = [['Года']]

        town_infected = self.create_names_for_towns(towns_info, town_infected)
        first_town_query = PlaceDemography.objects.get_current_town_sql(epidemic_pk=towns_info[0][0],
                                                                              region_name=towns_info[0][1],
                                                                              country_name=towns_info[0][2],
                                                                                town_name=towns_info[0][3])

        town_infected = self.create_dates_for_lst(first_town_query, town_infected)

        town_recovered = copy.deepcopy(town_infected)
        town_dead = copy.deepcopy(town_infected)

        town_iter = 1
        for town_info in towns_info:
            query = PlaceDemography.objects.get_current_town_sql(epidemic_pk=town_info[0],
                                                                   region_name=town_info[1],
                                                                 country_name=town_info[2],
                                                                 town_name=town_info[3])
            raw_iter = 1
            for raw in query:
                population = raw.population
                town_infected[raw_iter][town_iter] = float(raw.infected) / float(population)
                town_recovered[raw_iter][town_iter] = float(raw.recovered) / float(population)
                town_dead[raw_iter][town_iter] = float(raw.dead) / float(population)
                raw_iter += 1
            town_iter += 1

        return [town_infected, town_recovered, town_dead]


    def get_max_values_town(self, towns_info):

        queries = []
        max_values_town_query = PlaceDemography.objects.get_current_town_sql(epidemic_pk=towns_info[0][0],
                                                                   region_name=towns_info[0][1],
                                                                    country_name=towns_info[0][2],
                                                                             town_name=towns_info[0][3])

        for town_info in towns_info:
            query = PlaceDemography.objects.get_current_town_sql(epidemic_pk=town_info[0],
                                                                   region_name=town_info[1],
                                                                    country_name=town_info[2],
                                                                 town_name=town_info[3])
            queries.append(query)
            if (len(max_values_town_query) < len(query)):
                max_values_town_query = query

        return max_values_town_query, queries

    def get_town_graphics_data(self, towns_info):
        town_infected = [['Динамика']]

        town_infected = self.create_names_for_towns(towns_info, town_infected)
        max_values_town_query, queries = self.get_max_values_town(towns_info)

        town_infected = self.create_values_for_lst(max_values_town_query, town_infected)

        town_recovered = copy.deepcopy(town_infected)
        town_dead = copy.deepcopy(town_infected)

        region_iter = 1
        for query in queries:
            # определение шага, через который будут записываться не None значения
            h = int(len(max_values_town_query) / len(query))
            raw_iter = 1
            for raw in query:
                if ((raw_iter - 1) % h == 0):
                    population = raw.population
                    town_infected[raw_iter][region_iter] = float(raw.infected) / float(population)
                    town_recovered[raw_iter][region_iter] = float(raw.recovered) / float(population)
                    town_dead[raw_iter][region_iter] = float(raw.dead) / float(population)
                else:
                    town_infected[raw_iter][region_iter] = None
                    town_recovered[raw_iter][region_iter] = None
                    town_dead[raw_iter][region_iter] = None
                raw_iter += 1
            region_iter += 1

        return [town_infected, town_recovered, town_dead], self.get_date_town_graphics_data(towns_info)



class Favourites(models.Model):
    #user = models.OneToOneField(User, on_delete = models.PROTECT, blank = False)
    virus = models.ManyToManyField(Virus,  blank=True)
    epidemic = models.ManyToManyField('Epidemic', blank=True)

    objects = FavouritesManager()

    def __str__(self):
        return '{} {}'.format(self.pk, self.virus)



class Town(models.Model):
    epidemic_id = models.PositiveIntegerField(default=1, blank=True)
    region_choices = (
        ('СА', 'Северная Америка'),
        ('ЮА', 'Южная Америка'),
        ('Аф', 'Африка'),
        ('Е', 'Европа'),
        ('Аз', 'Азия'),
        ('Ав', 'Австралия'),
        ('Ан', 'Антарктида'),
    )
    region = models.CharField(max_length=2, choices=region_choices)
    country = CountryField()
    town = models.CharField(max_length=100)
    favourite = models.ForeignKey(Favourites, on_delete=models.PROTECT, blank=True)

    objects = TownManager()

    def __str__(self):
        return '{} {}'.format(self.pk, self.town)

class Country(models.Model):
    epidemic_id = models.PositiveIntegerField(default=1, blank=True)
    region_choices = (
        ('СА', 'Северная Америка'),
        ('ЮА', 'Южная Америка'),
        ('Аф', 'Африка'),
        ('Е', 'Европа'),
        ('Аз', 'Азия'),
        ('Ав', 'Австралия'),
        ('Ан', 'Антарктида'),
    )
    region = models.CharField(max_length=2, choices=region_choices)
    country = CountryField()
    favourite = models.ForeignKey(Favourites, on_delete=models.PROTECT, blank=True)

    objects = CountryManager()

    def __str__(self):
        return '{} {}'.format(self.pk, self.country.name)

class Region(models.Model):
    epidemic_id = models.PositiveIntegerField(default=1, blank=True)
    region_choices = (
        ('СА', 'Северная Америка'),
        ('ЮА', 'Южная Америка'),
        ('Аф', 'Африка'),
        ('Е', 'Европа'),
        ('Аз', 'Азия'),
        ('Ав', 'Австралия'),
        ('Ан', 'Антарктида'),
    )
    region = models.CharField(max_length=2, choices=region_choices)

    favourite = models.ForeignKey(Favourites, on_delete=models.PROTECT, blank=True)

    objects = RegionManager()

    def __str__(self):
        return '{} {}'.format(self.pk, self.region)