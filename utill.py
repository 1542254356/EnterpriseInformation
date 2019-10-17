

def saveList(fileName, list):
    with open(fileName, "w+",encoding = "utf-8") as f:
        for e in list:
            f.write(str(e) + "\n")

