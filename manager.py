import os
import json

from models.label import label
import models.template as template


def generateDefaultTemplates():
    labels = template.labelsTemplate.default()
    with open("templates/labels.json", "w") as file:
        file.write(labels.toJson())


if __name__ == "__main__":
    generateDefaultTemplates()
