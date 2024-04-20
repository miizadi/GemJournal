import time
import json
import os

def saveNote(title, creationTime, group, body):
    data = {
        "title": title,
        "creationTime": creationTime,
        "group": group,
        "body": body
    }

    fileName = "./saves/" + str(creationTime).replace(".", "") + ".json"

    with open(fileName, "w") as file:
        json.dump(data, file)

def readNotes():
    noteFiles = [f for f in os.listdir("./saves")]

    totalData = []

    for path in noteFiles:
        with open("./saves/" + path, "r") as file:
            data = json.load(file)
            totalData.append(data)

    return totalData

print(readNotes())