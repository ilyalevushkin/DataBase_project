import json

class JsonConverter:


    def get_json_data(self, split_line, model_str="virus"):
        if (model_str == "virus"):
            return {
                "model": "virus_app.virus",
                "pk": int(split_line[0]),
                "fields": {
                    "name": split_line[1],
                    "epidemiology": int(split_line[2]),
                    "photo": "img/viruses/" + split_line[3]
                }
            }
        elif (model_str == "epidemiology"):
            return {
                "model": "virus_app.epidemiology",
                "pk": int(split_line[0]),
                "fields": {
                    "structure": split_line[1],
                    "source_of_infection": split_line[2],
                    "transmission_mechanism": split_line[3],
                    "symptoms": split_line[4],
                    "more_info": split_line[5],
                    "transmission_way": json.loads(split_line[6]),
                    "place_of_beating": json.loads(split_line[7])
                }
            }
        elif (model_str == "epidemic"):
            return {
                "model": "virus_app.epidemic",
                "pk": int(split_line[0]),
                "fields": {
                    "source_country_of_infection": split_line[1],
                    "epidemiology": int(split_line[2])
                }
            }
        elif (model_str == "period"):
            return {
                "model": "virus_app.period",
                "pk": int(split_line[0]),
                "fields": {
                    "date_from": split_line[1],
                    "date_to": split_line[2]
                }
            }
        elif (model_str == "place"):
            return {
                "model": "virus_app.place",
                "pk": int(split_line[0]),
                "fields": {
                    "country": split_line[1],
                    "town": split_line[2],
                    "region": split_line[3],
                    "population": int(split_line[4])
                }
            }
        elif (model_str == "placedemography"):
            return {
                "model": "virus_app.placedemography",
                "pk": int(split_line[0]),
                "fields": {
                    "infected": int(split_line[1]),
                    "recovered": int(split_line[2]),
                    "dead": int(split_line[3]),
                    "epidemic": int(split_line[4]),
                    "period": int(split_line[5]),
                    "place": int(split_line[6]),
                }
            }

    def get_json_data_mas(self, file_lines, model_str):
        json_data_mas = []
        for line in file_lines:
            split_line = line.split("\,")
            json_data_mas.append(self.get_json_data(split_line, model_str))
        return json_data_mas