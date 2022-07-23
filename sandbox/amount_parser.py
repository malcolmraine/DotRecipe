

test = "1 8/4 tbsp"

print(test)
parts = test.split(" ")
print(parts)
whole = 0
decimal = 0
unit = ""

for idx, part in enumerate(parts):
    print(part)
    if "." in part:
        whole, decimal = part.split(".")
        whole = int(whole)
        decimal = (float("1." + decimal) - 1)
    elif part.isnumeric():
        whole = int(part)
    elif "/" in part:
        decimal = int(part.split("/")[0]) / int(part.split("/")[1])
    elif idx == len(parts) - 1 and "/" not in part and "." not in part and not part.isnumeric():
        unit = part

print(whole + decimal, unit)