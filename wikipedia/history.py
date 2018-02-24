import os
import json

# Recreate history file from data files
#

def main():
    for f in os.listdir("data"):
        try:
            keys = json.load(open("data/" + f, "r")).keys()
            for key in keys:
                print (key)
        except:
            print ("skip " + f)


if __name__ == "__main__":
    main()
