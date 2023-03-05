import json


class label:
    name = "Label Name"
    descr = "Label Description"
    color = "#ffffff"

    def default():
        return label("Label Name", "Label Description", "#ffffff")

    def __init__(self, name, descr, color):
        self.name = name
        self.descr = descr
        self.color = color

    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    def fromJson(self, json):
        tmp = json.loads(json)
        self.name = tmp.name
        self.descr = tmp.descr
        self.color = tmp.color
