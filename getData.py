import json
import requests


url = 'https://canvas.vt.edu/api/v1/courses'
header = {"Authorization": "Bearer 4511~hNgxEqiPIYBBsV6jwwogaa1Jit4cBsPhFKOzPFjRpzws7qhhZd2PP5MUlt2uPhLI"}
           
r = requests.get(url, headers=header)

for item in r.json():
    print (item["name"])
    print (item["points_possible"])
