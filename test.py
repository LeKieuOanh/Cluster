import os

formatted_data = ['1 Si 0.000000 0.000000 1.057081', '2 Si 0.000000 0.000000 -1.057081']
data = []
for item in formatted_data:
    data.append(" ".join(item.split()))
for i in data:
    print(f"{i}")

