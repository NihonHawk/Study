import os
from pathlib import Path


def finder():
    names = os.listdir(os.getcwd())
    for name in names:
        fullname = os.path.join(os.getcwd(), name)
        if os.path.isfile(fullname):
            # print(fullname)
            if Path(fullname).suffix == '.ps1':
                with open(fullname, "r") as file:
                    text = file.read()
                with open("apps.ps1", "a") as file2:
                    file2.write(text + '\n')


if __name__ == '__main__':
    finder()
