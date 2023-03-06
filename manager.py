import os
import sys
import json

from models.label import label
import models.template as template


def generateDefaultTemplates():
    labels = template.labelsTemplate.default()
    with open("templates/labels.json", "w") as file:
        file.write(labels.toJson())


def applyTemplate(index):
    templateFile = ''
    target = ''
    owner = ''
    repo = ''

    for i in range(index, len(sys.argv)):
        if sys.argv[i].lower() == "--target":
            target = sys.argv[i + 1]
            break
        else:
            templateFile = sys.argv[i]

    if target.__contains__("/"):
        parts = target.split("/")
        owner = parts[0]
        repo = parts[1]
    else:
        owner = target

    if templateFile != '':
        path = 'templates/' + templateFile
        instance = template.labelsTemplate.build(path)

        if instance == '':
            return

        if repo != '':
            instance.apply(owner, repo)
        else:
            instance.applyToRepos(owner)


if __name__ == "__main__":
    generateDefaultTemplates()
