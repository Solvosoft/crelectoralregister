#read the file line in line
#delete whitespaces
import re

def readFile():
    """with open("PADRON_PEQ.txt") as fichero:
        for line in fichero:
            lines = re.sub(' +', ' ', line)
            print(lines)

    with open("PADRON_TEMP.txt", "w") as fichero:
        fichero.write(lines)
        print("****")
        print(lines)"""

    archivo = open("PADRON_PEQ.txt", "r")
    for lines in archivo.readlines():
        line = re.sub(' +', ' ', lines)
        #lines.split(",")
        print(line)
        #archivoTemp = open("PADRON_TEMP.txt", "w")
        #archivoTemp.writelines(line)
        #print ("+++", line)
    archivo.close()




readFile()
