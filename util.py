import re


def splitName(fullName):
    names = re.findall(r"[\w']+", fullName)

    last = ""
    first = ""

    if len(names) == 1:  # BugsBUNNY
        names = re.findall(r"([A-Z][^A-Z]+|[A-Z]+)", fullName)
        return splitName(" ".join(names[1:] + names[0:1]))  # Now "BUNNY Bugs"

    if "," in fullName:
        last, first = fullName.split(",", 1)
        # first = ' '.join(names)
    elif any(map(str.isupper, names)):
        for name in names:
            if name.isupper():
                last += name
                last += " "
            else:
                first += name
                first += " "
    else:
        last = names[-1]
        first = " ".join(names[:-1])

    last = last.upper().strip()
    first = first.strip()
    return (last, first)


# e.g. c:\folder\folder\{stem}.pdf
def incrementStem(stem: str):
    match = re.match(r"(.*)\((\d+)\)$", stem)
    if match:
        i = int(match.group(2)) + 1
        incremented = f"{match.group(1)}({i})"
    else:
        incremented = stem + "(1)"
    return incremented


if __name__ == "__main__":
    print(incrementStem("foobar"))
    print(incrementStem("foobar(1)"))

    print(splitName("BugsBUNNY"))
    print(splitName("bunny, bugs"))
    print(splitName("Bunny,Bugs"))
    print(splitName("BUNNY Bugs"))
    print(splitName("The Martian, Marvin"))
    print(splitName("THE MARTIAN, Marvin"))
    print(splitName("THE MARTIAN Marvin"))
