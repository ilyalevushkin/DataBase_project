from django.db import models


class EpidemicManager(models.Manager):

    class StrEpidemic:
        def __init__(self, source_country_of_infection):
            self.source_country_of_infection = source_country_of_infection

    def current_epidemic(self, pk):
        return self.get(pk=pk)

    def get_all_epidemics(self):
        return self.order_by('source_country_of_infection')

    def get_epidemics_by_epidemiology_pk(self, epidemiology_pk):
        query = self.filter(epidemiology__pk=epidemiology_pk)
        for raw in query:
            raw.printable_data = self.get_printable_data(raw.id)
        return query

    def get_printable_data(self, epidemic_pk):
        cur_ep = self.current_epidemic(epidemic_pk)
        source_country_of_infection = cur_ep.source_country_of_infection.name
        str_epidemic = self.StrEpidemic(source_country_of_infection)
        return str_epidemic

    def post_changes_in_epidemic(self, pk, request):
        cur_ep = self.current_epidemic(pk)
        cur_ep.source_country_of_infection = request.POST['select-country']
        cur_ep.more_info = request.POST['more-info']
        try:
            cur_ep.photo = request.FILES['photo']
        except:
            pass
        cur_ep.save()
