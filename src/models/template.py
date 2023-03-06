import json
from models.label import *


class labelsTemplate:
    labels = []

    def default():
        return labelsTemplate([
            label("bug", "Something isn't working", "#D73A4A"),
            label("documentation",
                  "Improvements or additions to documentation", "#0075CA"),
            label("duplicate", "This issue or pull request already exists", "#CFD3D7"),
            label("enhancement", "New feature or request", "#A2EEEF"),
            label("fixed", "This problem has been fixed", "#74D971"),
            label("help wanted", "Extra attention is needed", "#008672"),
            label("invalid", "This doesn't seem right", "#E4E669"),
            label("lab", "Experimental features", "#D93F0B"),
            label("merged", "Pull Request had been merged", "#0922A5"),
            label("question", "Further information is requested", "#D876E3"),
            label("tracking", "This issue is tracking by another issue", "#FEF2C0"),
            label("wontfix", "This will not be worked on", "#FFFFFF"),
            label("working on", "We are working on this issue", "#D4B4D3"),
        ])

    def __init__(self, labels):
        self.labels = labels

    def add(self, label):
        if not self.labels.__contains__(label):
            self.labels.append(label)

    def remove(self, name):
        for x in self.labels:
            if x.name == name:
                self.labels.remove(x)

    def update(self, name, label):
        for x in self.labels:
            if x.name == name:
                x = label

    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    def applyToRepos(self, owner):
        cmd = 'gh repo list'
        json = '--json name'
        jq = '--jq \".[].name\"'

        process = os.popen('{} {} {} {}'.format(cmd, owner, json, jq))
        repos = process.read().splitlines()
        process.close()

        print('Applying to repos: ')
        print(repos)

        for repo in repos:
            self.apply(owner, repo)

    def apply(self, owner, repo):
        currentLabels = getLabels(owner, repo)
        currentLabelsNames = [x.name for x in currentLabels]
        templateLabelsNames = [x.name for x in self.labels]

        actions = []

        for x in currentLabelsNames:
            if not templateLabelsNames.__contains__(x):
                actions.append(action('delete', x, label.default()))
            else:
                i = currentLabelsNames.index(x)
                j = templateLabelsNames.index(x)

                ndiff = currentLabels[i].name != self.labels[j].name
                ddiff = currentLabels[i].description != self.labels[j].description
                cdiff = currentLabels[i].color.lower(
                ) != self.labels[j].color.lower().replace("#", "")
                if ndiff or ddiff or cdiff:
                    # print('x -> {} diffed in {} {} {}'.format(x, ndiff, ddiff, cdiff))
                    actions.append(action('edit', x, self.labels[j]))

        for x in templateLabelsNames:
            if not currentLabelsNames.__contains__(x):
                actions.append(
                    action('create', x, self.labels[templateLabelsNames.index(x)]))

        print(json.dumps(actions, default=lambda o: o.__dict__,
              sort_keys=True, indent=4))

        for x in actions:
            x.execute(owner, repo)
