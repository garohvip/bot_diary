import json

with open("bd.json", "r") as f:
    data = json.load(f)
for i in range(len(data)):
    if data[i].get('login') == 5881762568:
        for j in data[i]['plan']:
            if "r" in j:
                count = len(data[i]['plan'][j])
                print(count)
                break
                # data[i]['plan'][j][]