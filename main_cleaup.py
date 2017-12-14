import sys
import re
import os

input_file = "./wilde.clean.txt"
output_filename = "wilde1.txt";

startIndex = 0
endIndex = 0


def witeLine(line):
    pattern = r'\[(\.\.\.)?\d+\]'

    if not line.startswith('CHAPTER'):
        line = re.sub(pattern, '', line)
        line = removeAbbrevation(line);
        output_file.write(line)  # write the file when you get to the meat, ignore back matter


def countQuotes(input):
    return input.count('\"') % 2 == 0;


def removeQuotation():
    input_file = "./wilde1.txt"
    output_filename = "./wilde2.txt";

    if sys.argv.__len__() > 1:
        input_file = input_file
    if sys.argv.__len__() > 2:
        output_filename = sys.argv[2]

    f = open(input_file)  # wilde.5.txt
    # output_filename = output_file #wilde.6.txt
    output_file = open(output_filename, 'w')
    markup_filename = output_filename + 'markup'  # wilde.6.txtmarkup
    markup_file = open(markup_filename, 'w')

    # pattern = re.compile(r'''
    #                \s*                                     #spaces we don't want
    #                (.*?)                                   #stuff before terminator, ? makes this non-greedy
    #                (\!"|\?"|\."|\;"|\,"|\!|\?|\.|\,[ ]")   #terminator and terminator with quote mark
    #                \s*                                     #spaces
    #                (.*)''', re.VERBOSE)  # c
    pattern = re.compile(r'''
                        \s*                                     #spaces we don't want
                        (.*?)                                   #stuff before terminator, ? makes this non-greedy
                        (\!"|\?"|\."|\;"|\!|\?|\.|\,[ ]")   #terminator and terminator with quote mark
                        \s*                                     #spaces
                        (.*)''', re.VERBOSE)  # c
    # pattern = re.compile(r'''
    #                     \s*                                     #spaces we don't want
    #                     (.*?)                                   #stuff before terminator, ? makes this non-greedy
    #                      (\!"|\?"|\."|\;"|\!|\?|\.[ ]")$    #terminator and terminator with quote mark
    #                     \s*                                     #spaces
    #                     (.*)''', re.VERBOSE)
    # haracters, allow comments in string

    line_count = 0
    sentence_count = 0
    markup_count = 0

    sent_type = 'N: '
    quote_flag = False
    sentend = f.readline()  # primer
    # sentend = sentend[0:-1]
    # line_count +=1
    #
    # Strip quotation marks at the front and back of sentend
    # If quote flag is on, type Q
    # If quote flag is off, type N
    # If a end quote is encountered and flag is off, there is an error
    # Then, print sentence where error occured, exit program
    #
    while True:
        m = pattern.match(sentend)
        if m and countQuotes(sentend):
            if re.search('^\s*".*?', sentend) and not quote_flag:
                quote_flag = True
                sent_type = 'Q: '
                sentfront = m.group(1)[1:]
            else:
                sentfront = m.group(1)
            sent_term = m.group(2)
            sentend = m.group(3)
            if sent_term == ', "':
                sentend = '"' + sentend
                sent_term = ','
            elif sent_term[-1] == '"':
                sent_term = sent_term[0:-1]
                quote_flag = False
            else:
                sent_term = m.group(2)
            if len(sentfront.split("\"")) > 3:
                print((sentfront + sent_term + '\n'))
                print("---------------")
            output_file.write((sentfront + sent_term + '\n'))
            sentence_count += 1
            stringTemp = (sent_type + sentfront + sent_term + '\n')
            stringTemp = stringTemp.replace("\"", "")
            markup_file.write(stringTemp)
            markup_count += 1
            if quote_flag == False:
                sent_type = 'N: '
        else:
            newline = f.readline()
            if len(newline) == 0:
                break
            if newline[-1] == '\n':
                newline = newline[0:-1]
            sentend += ' ' + newline
            # line_count +=1

    # print('Line count:', line_count)
    print('Sentence count:', sentence_count)
    print('Markup count:', markup_count)

    f.close()
    output_file.close()
    markup_file.close()  # close files
    # os.remove(input_file);


def removeAbbrevation(line):
    abbreviations = {'Dr\.': ['Dr', 0], 'Mrs\.': ['Mrs', 0], 'Mr\.': ['Mr', 0], ' VIII\.': [' VIII', 0],
                     ' XII\.': [' XII', 0], ' II\.': [' II', 0], ' VI\.': [' VI', 0], ' XIV\.': [' XIV', 0],
                     'James I\.': ['James I', 0], }
    for key in abbreviations:
        if re.search(key, line):
            abbreviations[key][1] += 1
            line = re.sub(key, abbreviations[key][0], line)
            while re.search(key, line):
                abbreviations[key][1] += 1
                line = re.sub(key, abbreviations[key][0], line)
    return line


if sys.argv.__len__() > 1:
    input_file = sys.argv[1]
if sys.argv.__len__() > 2:
    output_filename = sys.argv[2]

f = open(input_file)  # wilde.clean.txt
output_file = open(output_filename, 'w')

for line in f:
    if 'CHAPTER I' in line:
        break;
    startIndex += 1;

for line in f:
    if 'End of Project Gutenberg\'s The Picture of Dorian Gray, by Oscar Wilde' in line:
        break  # break out of for loop when you get to back matter
    else:
        witeLine(line)
removeQuotation()
print('File written:')

# output_file.close()
# f.close()
