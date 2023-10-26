import re


def splitName(fullName):
    names = re.findall(r"[\w']+", fullName)

    last=''
    first=''

    if ',' in fullName:
        last,first = fullName.split(',', 1)
        # first = ' '.join(names)
    elif any(map(str.isupper, names)):
        for name in names:
            if name.isupper():
                last = name
            else:
                first+=name
                first += ' '
    else:
        last = names[-1]
        first = ' '.join(names[:-1])



    # last = ''
    # first = ''
    # for name in names:
    #     if name.isupper():
    #         last = name

    last = last.upper().strip()
    first = first.strip()
    return (last, first)