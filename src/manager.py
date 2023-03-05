import os
import json

from models.label import label


def generateDefaultTemplates():
    pass


if __name__ == "__main__":
    labels = [label.default()] * 5
    print(json.dumps(labels, default=lambda o: o.__dict__, sort_keys=True, indent=4))
