from django.db import models


class TransmissionWays(models.Model):
    transmission_way_choices = (
        ('Ал' , 'Алиментарный'),
        ('Вод' , 'Водный'),
        ('Кб' , 'Контактно-бытовой'),
        ('Ук' , 'Укус'),
        ('Пар' , 'Парентеральный'),
        ('По' , 'Половой'),
        ('Вк' , 'Воздушно-капельный'),
        ('Вп' , 'Воздушно-пылевой'),
        ('Ран' , 'Раневой'),
        ('Кп' , 'Контактно-половой'),
    )
    transmission_way = models.CharField(max_length=3, choices=transmission_way_choices)