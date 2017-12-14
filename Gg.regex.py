import sys
import re
import os


input_file = "./wilde2.txt"
output_filename = "./wilde3";

if sys.argv.__len__() > 1:
    input_file = input_file
if sys.argv.__len__() > 2:
    output_filename = sys.argv[2]


f = open(input_file) #wilde.6.txt
#output_filename = output_file #wilde.7.txt
output_file = open(output_filename+ ".txt", 'w')
linecount =0
filecount =0

#regex for non-terminal punctuation at the end of a line with an optional space
punct1 = ',' + ' ?' + '\n'
punct2 = ';' + ' ?' + '\n'
punct3 = '!' + ' ?' + '\n'
punct4 = '\?' + ' ?' + '\n'
punct5 = ':' + ' ?' + '\n'
punct6 = '\.' + ' ?' + '\n'

#sub ,'s, ;'s, and :'s with .'s, if ., ?, or !, write same line
for line in f:
    #if line.__len__() > 242 :
    #    continue;
    linecount =linecount +1
    #if linecount % 500 == 0:
        #filecount = filecount +1
        #output_file.close();
        #output_file = open(output_filename+"_"+str(filecount)+ ".txt", 'w')
    if re.search (punct1, line):
        new_punct = re.sub(punct1, '.\n', line)
        output_file.write(new_punct)
    if re.search (punct2, line):
        new_punct = re.sub(punct2, '.\n', line)
        output_file.write(new_punct)
    if re.search (punct5, line):
        new_punct = re.sub(punct5, '.\n', line)
        output_file.write(new_punct)
    else:
        if re.search (punct6, line):
            output_file.write(line)
        if re.search (punct4, line):
            output_file.write(line)
        if re.search (punct3, line):
            output_file.write(line)

f.close()
output_file.close()
#os.remove(input_file)
####################################################################################################
