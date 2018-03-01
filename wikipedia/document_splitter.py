import codecs
import os
import json

# Split large documents in parts
#

def main():
    try:
        os.mkdir("chunks")
    except:
        pass
    chunck_size = 10000
    for file_name in os.listdir("data"):
        try:
            base_name = file_name.split('.')[0]
            if os.stat("data/" + file_name).st_size > 50000:
                with open("data/" + file_name, "r") as f:
                    s = f.read()
                end_of_chunk = 0
                i = 0
                start_of_chunk = 1
                counter = 0
                while end_of_chunk<len(s):
                    if s[end_of_chunk] == ']' and counter > chunck_size:
                        chunk = s[start_of_chunk:end_of_chunk]
                        output_file_name = "chunks/" + base_name + str(i) + ".json"
                        with codecs.open(output_file_name, "w", encoding='utf-8') as out:
                            if chunk[0] != "{":
                                out.write("{")
                            out.write(chunk + "]}")
                        start_of_chunk = end_of_chunk + 2
                        end_of_chunk = start_of_chunk
                        i = i + 1
                        counter = 0
                    else:
                        counter = counter + 1
                        end_of_chunk = end_of_chunk + 1

        except Exception as e:
            print (e)
            print ("skip " + file_name)


if __name__ == "__main__":
    main()
