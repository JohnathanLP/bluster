import json
import os
import requests

stats={}
uuids = [x.split(".")[0] for x in os.listdir("world/stats")]

PULL_USERNAMES = True          # Set false to disable loading usernames from Mojang API - this prevents spamming Mojang servers, and also allows for faster debugging

for uuid in uuids:
    stats[uuid] = json.load(open("world/stats/" + uuid + ".json"))
    try:
        if PULL_USERNAMES:
            data = requests.get("https://sessionserver.mojang.com/session/minecraft/profile/" + uuid.replace("-","")).json()
            stats[uuid]["username"] = data["name"]
        else:
            stats[uuid]["username"] = "NOT_LOADED"
        print("Loaded stats for {}:{}".format(uuid,stats[uuid]["username"]))
    except Exception as error:
        stats[uuid]["username"] = "unknown"
        print("Encountered error loading stats for {}".format(uuid))


categories = []
for uuid in stats:
    for group in stats[uuid]["stats"]:
        for category in stats[uuid]["stats"][group]:
            if category not in categories:
                categories.append((group,category))

print(categories)

f = open("output.csv", "w")

f.write(",,")
for uuid in stats:
    f.write(stats[uuid]["username"] + ",")
f.write("\n")

f.write(",,")
for uuid in stats:
    f.write(uuid + ",")
f.write("\n")

for c in categories:
    f.write("{},{},".format(*c))

    for uuid in stats:
        if c[0] in stats[uuid]["stats"]:
            if c[1] in stats[uuid]["stats"][c[0]]:
                f.write(str(stats[uuid]["stats"][c[0]][c[1]]))
        f.write(",")

    f.write("\n")

f.close()
