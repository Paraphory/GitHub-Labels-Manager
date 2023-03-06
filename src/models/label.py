import os
import json


class label:
    name = "Label Name"
    description = "Label Description"
    color = "#ffffff"

    def default():
        return label("Label Name", "Label Description", "#ffffff")

    def __init__(self, name, description, color):
        self.name = name
        self.description = description
        self.color = color

    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    def fromJson(text):
        tmp = json.loads(text, object_hook=lambda d: label(
            d['name'], d['description'], d['color']))
        return label(tmp.name, tmp.description, tmp.color)


class action:
    option = str()  # create, edit, delete
    name = str()
    label = label.default()

    def __init__(self, option, name, label):
        self.option = option
        self.name = name
        self.label = label

    def execute(self, owner, repo):
        cmd = 'gh label {}'.format(self.option)
        repo = '-R {}/{}'.format(owner, repo)

        append = str()

        if self.option == 'create':
            label = '\"{}\" --description \"{}\" --color {}'.format(
                self.name, self.label.description, self.label.color.replace("#", ""))
            append = '-f {}'.format(label)
        elif self.option == 'edit':
            nameChanged = self.name != self.label.name
            append = '\"{}\" --description \"{}\" --color {}'.format(
                self.name, self.label.description, self.label.color.replace("#", ""))
            if nameChanged:
                append += ' --name \"{}\"'.format(self.label.name)
        elif self.option == 'delete':
            append = '\"{}\" --yes'.format(self.name)

        fullCommand = '{} {} {}'.format(cmd, repo, append)

        print(os.system(fullCommand))


def getLabels(owner, repo):
    # example cmd: gh label list -R Crequency/KitX --json name,description,color --jq ".[]"

    cmd = 'gh label list'
    repo = '-R {}/{}'.format(owner, repo)
    condition = '--json name,description,color'
    jq = '--jq \".[]\"'

    fullCommand = '{} {} {} {}'.format(cmd, repo, condition, jq)

    process = os.popen(fullCommand)
    output = process.read().splitlines()
    process.close()

    labels = [label.fromJson(x) for x in output if x != '']

    return labels


if __name__ == "__main__":
    print([x.toJson() for x in getLabels('Crequency', 'KitX')])
