from django.db import models
from ..models.transmissionways import TransmissionWays
from ..models.placeofbeating import PlaceOfBeating

class EpidemiologyManager(models.Manager):

    class StrEpidemiology:
        def __init__(self, structure,
                     source_of_infection,
                     transmission_mechanism,
                     transmission_ways,
                     place_of_beatings,
                     symptoms,
                     more_info):
            self.structure = structure
            self.source_of_infection = source_of_infection
            self.transmission_mechanism = transmission_mechanism
            self.transmission_ways = transmission_ways
            self.place_of_beatings = place_of_beatings
            self.symptoms = symptoms
            self.more_info = more_info

    #то что не вошло в эпидемиологию
    class OtherEpidemiology:
        def __init__(self, other_structure,
                     other_source_of_infection,
                     other_transmission_mechanism,
                     other_transmission_ways,
                     other_place_of_beatings):
            self.other_structure = other_structure
            self.other_source_of_infection = other_source_of_infection
            self.other_transmission_mechanism = other_transmission_mechanism
            self.other_transmission_ways = other_transmission_ways
            self.other_place_of_beatings = other_place_of_beatings


    def base_information(self):
        return self

    def current_epidemiology(self, pk):
        return self.get(pk=pk)

    def convert_lst_to_str_appearance(self, lst):
        return '; '.join(lst)

    #возвращает совпадение
    def get_long_name_by_short(self, short_name, names_dict):
        for pair in names_dict:
            if pair[0] == short_name:
                return pair[1]

    def get_short_name_by_long(self, long_name, names_dict):
        for pair in names_dict:
            if pair[1] == long_name:
                return pair[0]

    #возвращает все кроме совпадения
    def get_other_long_name_by_short(self, short_name, names_dict):
        lst = []
        for pair in names_dict:
            if pair[0] != short_name:
                lst.append(pair[1])
        return lst


    def get_str_long_names_by_short(self, short_names, choices):
        return self.convert_lst_to_str_appearance(self.get_long_names_by_short(short_names, choices))

    def get_long_names_by_short(self, short_names, choices):
        return [self.get_long_name_by_short(short_name, choices) for short_name in short_names]

    def get_short_names_by_long(self, long_names, choices):
        return [self.get_short_name_by_long(long_name, choices) for long_name in long_names]

    #возвращает все кроме совпаденИЙ
    def get_other_long_names_by_short(self, short_names, choices):
        short_choices = [choice[0] for choice in choices]
        #получает список таких short_choices, которыхи нет в short_names
        other_short_names = list(set(short_choices).difference(set(short_names)))
        return [self.get_long_name_by_short(other_short_name, choices) for other_short_name in other_short_names]

    def get_printable_data(self, pk):

        cur_ep = self.current_epidemiology(pk)

        structure = self.get_long_name_by_short(cur_ep.structure, cur_ep.structure_choices)

        source_of_infection = self.get_long_name_by_short(cur_ep.source_of_infection, cur_ep.source_choices)

        transmission_mechanism = self.get_long_name_by_short(cur_ep.transmission_mechanism, cur_ep.transmission_choices)

        transmission_ways = self.get_str_long_names_by_short([
            way.transmission_way for way in cur_ep.transmission_way.all()],
            cur_ep.transmission_way.model.transmission_way_choices)

        place_of_beatings = self.get_str_long_names_by_short([
            place.place_of_beating for place in cur_ep.place_of_beating.all()],
            cur_ep.place_of_beating.model.system_choices)


        str_epidemiology = self.StrEpidemiology(structure,
                                                source_of_infection,
                                                transmission_mechanism,
                                                transmission_ways,
                                                place_of_beatings,
                                                cur_ep.symptoms,
                                                cur_ep.more_info)

        return str_epidemiology

    def get_edit_data(self, pk):

        cur_ep = self.current_epidemiology(pk)

        structure = self.get_long_name_by_short(cur_ep.structure, cur_ep.structure_choices)
        other_structure = self.get_other_long_name_by_short(cur_ep.structure, cur_ep.structure_choices)

        source_of_infection = self.get_long_name_by_short(cur_ep.source_of_infection, cur_ep.source_choices)
        other_source_of_infection = self.get_other_long_name_by_short(cur_ep.source_of_infection, cur_ep.source_choices)

        transmission_mechanism = self.get_long_name_by_short(cur_ep.transmission_mechanism, cur_ep.transmission_choices)
        other_transmission_mechanism = self.get_other_long_name_by_short(cur_ep.transmission_mechanism,
                                                                         cur_ep.transmission_choices)

        transmission_ways = self.get_long_names_by_short([
            way.transmission_way for way in cur_ep.transmission_way.all()],
            cur_ep.transmission_way.model.transmission_way_choices)

        other_transmission_ways = self.get_other_long_names_by_short([
            way.transmission_way for way in cur_ep.transmission_way.all()],
            cur_ep.transmission_way.model.transmission_way_choices)

        place_of_beatings = self.get_long_names_by_short([
            place.place_of_beating for place in cur_ep.place_of_beating.all()],
            cur_ep.place_of_beating.model.system_choices)

        other_place_of_beatings = self.get_other_long_names_by_short([
            place.place_of_beating for place in cur_ep.place_of_beating.all()],
            cur_ep.place_of_beating.model.system_choices)

        edit_epidemiology = self.StrEpidemiology(structure,
                                                source_of_infection,
                                                transmission_mechanism,
                                                transmission_ways,
                                                place_of_beatings,
                                                cur_ep.symptoms,
                                                cur_ep.more_info)

        other_edit_epidemiology = self.OtherEpidemiology(other_structure,
                                                other_source_of_infection,
                                                other_transmission_mechanism,
                                                other_transmission_ways,
                                                other_place_of_beatings)

        return edit_epidemiology, other_edit_epidemiology


    def post_changes_in_epidemiology(self, pk, new_data):
        cur_ep = self.current_epidemiology(pk)

        cur_ep.structure = self.get_short_name_by_long(new_data['select-structure'], cur_ep.structure_choices)
        cur_ep.source_of_infection = self.get_short_name_by_long(new_data['select-source-of-infection'],
                                                                 cur_ep.source_choices)

        cur_ep.transmission_mechanism = self.get_short_name_by_long(new_data['select-transmission-mechanism'],
                                                                    cur_ep.transmission_choices)

        transmission_way = TransmissionWays(transmission_way='Ал')


        short_ways = self.get_short_names_by_long(new_data.getlist('select-transmission-ways'),
                                                  transmission_way.transmission_way_choices)


        cur_ep.transmission_way.clear()

        for short_way in short_ways:
            transmission_way = TransmissionWays(transmission_way=short_way)
            transmission_way.save()
            cur_ep.transmission_way.add(transmission_way)

        place_of_beating = PlaceOfBeating(place_of_beating='Одс')
        short_places = self.get_short_names_by_long(new_data.getlist('select-place-of-beatings'),
                                                    place_of_beating.system_choices)

        cur_ep.place_of_beating.clear()

        for short_place in short_places:
            place_of_beating = PlaceOfBeating(place_of_beating=short_place)
            place_of_beating.save()
            cur_ep.place_of_beating.add(place_of_beating)


        cur_ep.symptoms = new_data['symptoms']
        cur_ep.more_info = new_data['more-info']

        cur_ep.save()