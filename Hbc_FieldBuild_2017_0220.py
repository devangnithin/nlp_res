import os
import re
import math
import sys
import nltk
import pickle
import csv
#from Hc_Pickle_2017_0220 import RetrievePickleFile
#from Hc_Pickle_2017_0220 import SavePickleFile
#from Hc_Pickle_2017_0220 import Tree_Processor
#from Hc_Pickle_2017_0220 import Get_Avg_Per
#from Hc_Pickle_2017_0220 import Get_POS_Counts
from nltk.tree import Tree
from operator import itemgetter
from nltk import Tree

#nltk import experiments

###########################              Regular Expressions            ###########################

white_space = re.compile("^\s*$")

phrase_grep = re.compile("""
                        (^\s*\(\w+\s{1}(?!\w+))
                        """, re.X)

find_paren = re.compile("\)")
remove_space = re.compile("\s+", re.X)
remove_exterior = re.compile("""
                                ^\s+ |
                                \s+$ |
                                \( |
                                \) |
                                \" |
                            """, re.X)

word_grep = re.compile("""
                            (\(\w{2,4}\$*\ '?\w+\.*-*\w*\.*\w*\)) |
                            (\([.,?!]\ [.,?!]\))
                        """, re.X)

sentence_end = re.compile('''
                            \(\.\ \.\)        |
                            \(\?\ \?\)        |
                            \(!\ !\)
                          ''', re.X)

remove_misc = re.compile("""
                            (\.\ \.)        |
                            (\?\ \?)        |
                            (!\ !)          |
                            (,\ ,)

                          """, re.X)

pos_getter = re.compile("(?<=\()\w+\$?(?= )")
pos_word_getter = re.compile("(?<= )'*\w+\.*-*\w*\.*\w*(?=\))")

remove_basic_punct = re.compile("[,'\"]")

pos_getter = re.compile("(?<=\()\w+\$?(?= )")
pos_word_getter = re.compile("(?<= )'*\w+\.*-*\w*\.*\w*(?=\))")

#  Constant variables for Rounding level and Log base
ROUNDNUM = 2
LOGNUM = 2

###################################################################################################
###########################             RetrievePickleFile              ###########################
###################################################################################################
#    Function to retrieve a binary stored list or dictionary from a pickle saved file.

#Arguments:    File Path for dictionary or list pickle(minus ext), String of what it is for error, 
#               If is a dictionary or List
#Arg Type:     String (file Path), String(what it is getting), Bool
#Returns:      The retrieved object
#Ret Type:     Dictionary or List

def RetrievePickleFile(pick_path, what_isit="Object", isDict=True):
    #  If the file does not already exist, it will display this fact and give an empty
    #      list or dictionary(depending on what is requested)
    #if not os.path.exists(pick_path + ".mnw"):

    print ("<<<  No " + what_isit + " pickle file available, recreating   >>>")
    print ()
    problem_list = {} if isDict else []
        
    #  Since the file does exist, it will retrieve the dictionary/list from the file
    #else:
     #   obj_file = open(pick_path + ".mnw", 'rb')
      #  problem_list = pickle.load(obj_file)
       # if problem_list == None:
        #    print ("<<<  Couldn't read " + what_isit + " pickle file, <recreating   >>>")
         #   problem_list = {} if isDict else []
        #obj_file.close()
        
    return problem_list

###################################################################################################
###########################                SavePickleFile               ###########################
###################################################################################################
#    Function to Store in binary a list or dictionary.

#Arguments:    The Object to be saved, File Path for dictionary or list pickle(minus ext), 
#                   If it should also be stored as a text, If is a dict
#Arg Type:     List/Dict, String (file Path), Bool(text?), Bool(Dict?)
#Returns:      Nothing
#Ret Type:     N/A

def SavePickleFile(obj_to_save, pick_path, textYN=False, isDict=True):
    #  The first thing it does is opens the file that is to be saved
    pickle_file = open(pick_path + ".mnw", 'wb')

    #  Saves the data into the file in binary form and closes the file.
    pickle.dump(obj_to_save, pickle_file)
    pickle_file.close()
    
    #  If a text version is to be created, it does so by creating a new txt file 
    #  under the same name(with a .txt extension, and adds the data into the file
    if textYN == True:
        #  Opening a new text file for storing in unsorted
        text_file = open(pick_path + ".txt", 'w')
        
        #  Opening a new text file for storing sorted by the key (or for list)
        text_file_key = open(pick_path + "-Key_Sort.txt", 'w')
        
        if isDict:
            #  Opening a new text file for storing by value
            text_file_val = open(pick_path + "-Val_Sort.txt", 'w')
            
            #  Writing the dictionary object to a text file unsorted.
            [text_file.write(str(a).rjust(20) + " :: " + str(b).ljust(20) + "\n") for a,b in obj_to_save.items()]
            
            #  Writing the dictionary object to a text file sorted by values
            [text_file_val.write(str(this_key).rjust(20) + " :: " + str(this_value).ljust(20) + "\n") for this_key,
              this_value in sorted(obj_to_save.items(), key=itemgetter(1))]
                
            #  Closing the value set file
            text_file_val.close()
            
            #  Writing the dictionary object to a text file sorted by keys
            [text_file_key.write(str(this_key).rjust(20) + " :: " + 
              str(obj_to_save[this_key]).ljust(20) + "\n") for this_key
              in sorted(obj_to_save.keys())]
            
            
        else:
            #  Writing the List to the file in unsorted form
            [text_file.write(str(a) + "\n") for a in obj_to_save ]
            
            #  Sorting the list then writing the list to the sorted file
            obj_to_save.sort()
            [text_file_key.write(str(b) + "\n") for b in obj_to_save ]
            
        #  Closing rest of the files
        text_file.close()
        text_file_key.close()
    return

def Tree_Processor(input_filename):
    #open, read, accum, call compute complexities, close
    
    tree_height_list = []
    
    first_child_flag = True
    
    #  Dictionaries for each type of data needed
    sentence_dict, nested_dict = {}, {}  #  Sentence Level types (SBARs, etc) and Nested Versions
    word_dict, pos_dict = {}, {}      #  Dictionary for each word and each Part of Speech
    sentence_dict["QUEST"] = 0
    #  Lists for "stacks" keeping track of the sentence tree and POS
    sentence_stack, pos_word__list = [], []
    
    #  List of sentence lengths
    sent_totals = []
    sentWord = 0
    
    opened_file = open(input_filename, 'r')
    
    entire_tree = ""
    #  Going through each line to get the sentence structure and words
    for each_line in opened_file:
        #print('[', each_line, ']')
        if re.search(white_space, each_line):
            if not entire_tree == "":
                #  Getting the tree height and appending the count
                each_tree = nltk.Tree.fromstring(entire_tree)
                tree_height_list.append(each_tree.height())
                #print('tree height:', each_tree.height())
                if each_tree.height() == 1:
                    print ("Only one tree in:  '" + str(file_path) + "'")
                Compute_Complexities([sentence_dict, nested_dict, pos_word__list, word_dict, pos_dict, tree_height_list])
                entire_tree = ""
            continue
        
        #  Adding the tree line to the text
        entire_tree += each_line
        
        #  Searching for all pertinent information
        search_line = re.search(phrase_grep, each_line)     #  Phrases/Sentences (SBAR, (NP, etc.
        word_get = re.findall(word_grep, each_line)         #  Getting all the actual words
        paren_count = re.findall(find_paren, each_line)     #  Parentheses to keep track of tree form
        sent_end = re.search(sentence_end, each_line)       #  End of a sentence
        
        #  If the sentence is ended, append word count to the list and reset word count.
        if sent_end:
            sent_totals.append(sentWord)
            sentWord = 0
        
        #  If there was a new phrase/sentence level processes it.
        if search_line:
            #  Getting the structure itself and removing excess space.
            sent_struct = re.sub(remove_space, "", search_line.group())            
            
            #  If there is no stack or the parent is the same as the child, do not count
            if len(sentence_stack) == 0 or not sent_struct == sentence_stack[-1]:
                
                #  Dictionary count of any structure that is nested (has a version of itself in the stack alread)
                nested_dict[sent_struct] = nested_dict[sent_struct] + 1 if sent_struct in nested_dict and sent_struct in sentence_stack else 1
                
                #  Dictionary count of all structures
                sentence_dict[sent_struct] = (sentence_dict[sent_struct] + 1) if sent_struct in sentence_dict else 1                

            #  Adding the structure to the stack
            sentence_stack.append(sent_struct)
                
        #  If the current line has a pos/word pair
        if word_get:
            
            #  Iterating through each pair of pos/word
            for each_pair in word_get:
                for each_set in each_pair:
                    #  Ignoring the pair if it is nothing or a sentence/punct
                    if each_set == '' or re.search(remove_misc, each_set):
                        continue
                    
                    #  Getting the POS and the word
                    each_pos = re.search(pos_getter, each_set)
                    each_word = re.search(pos_word_getter, each_set)
                    
                    if each_pos and each_word:
                        c_pos = each_pos.group()
                        c_word = each_word.group().lower()
                        c_word = re.sub(remove_basic_punct, "", c_word)
                        
                        #  Adding the POS / Word pair to the POS Stack and incrementing the word Count
                        pos_word__list.append((c_pos, c_word))
                        sentWord += 1 
                        
                        #  Adding the Word to the dictionary or incrementing its count
                        word_dict[c_word] = word_dict[c_word] + 1 if c_word in word_dict else 1

                        #  Adding the POS to the dictionary or incrementing its count
                        pos_dict[c_pos] = pos_dict[c_pos] + 1 if c_pos in pos_dict else 1
                        
        #  This pops through the correct amount of ")" to get through the tree,  popping out as many structures as there are ")"
        closeParen = len(paren_count) - len(word_get)
        while closeParen > 0 and len(sentence_stack) > 0:
            sentence_stack.pop() 
            closeParen -= 1

    if not entire_tree == "":
        #  Getting the tree height and appending the count
        if not entire_tree[0] == "(":
          print("entire tree:", entire_tree)
          print()
          print("we are hosed")
          print()
        else:
          each_tree = nltk.Tree.fromstring(entire_tree)
          tree_height_list.append(each_tree.height())
          if each_tree.height() == 1:
             print ("Only one tree in:  '" + str(file_path) + "'")
          Compute_Complexities([sentence_dict, nested_dict, pos_word__list, word_dict, pos_dict, tree_height_list])
          entire_tree = ""
     
    opened_file.close()
    
    sent_totals.sort()
    
    #  Returning 
    #    the Sentence Dictionary of all sentences
    #    The Nested Dictionary of nested levels
    #    The POS/Word list
    #    The Individual Word Dictionary
    #    The individual POS Dictionary
    return sentence_dict, nested_dict, pos_word__list, word_dict, pos_dict, tree_height_list

def Get_Avg_Per(numNum, numDiv, mult=1, caller=""):
    retval = round((float(numNum) / numDiv * mult), ROUNDNUM) if numDiv > 0 else 0
#    if caller == "perOfTree":
#      print (numNum, numDiv, mult, retval)
    return retval

# Function to reduce the types of parts-of-speech.  All NN (NN,NNS etc) become nouns, all VB become verbs etc 

def Get_POS_Counts(pos_dict):
    
    numFor = 0
    numWs = 0
    numDet = 0
    numNouns = 0
    numVerbs = 0
    numAdjs = 0
    numAdvs = 0
    numPreps = 0
    numPron = 0
    numInters = 0
    numCards = 0
    numModal = 0
    numCC = 0
    numTO = 0
    numPart = 0
    numEx = 0
    numPOSs = 0
    numLists = 0
    numSym = 0
    
    numTotal = 0
    
    for each_k in pos_dict.keys():
        pos_count = pos_dict[each_k]
        numTotal += pos_count   
        if 'DT' in each_k:
            numDet += pos_count
        elif 'NN' in each_k:
            numNouns += pos_count
        elif 'VB' in each_k:
            numVerbs += pos_count
        elif 'JJ' in each_k:
            numAdjs += pos_count
        elif 'RB' in each_k:
            numAdvs += pos_count
        elif 'IN' in each_k:
            numPreps += pos_count
        elif 'UH' in each_k:
            numInters += pos_count
        elif 'CD' in each_k:
            numCards += pos_count
        elif 'MD' in each_k:
            numModal += pos_count
        elif 'CC' in each_k:
            numCC += pos_count
        elif 'TO' in each_k:
            numTO += pos_count
        elif 'RP' in each_k:
            numPart += pos_count
        elif 'EX' in each_k:
            numEx += pos_count
        elif 'FW' in each_k:
            numFor += pos_count
        elif 'POS' in each_k:
            numPOSs += pos_count
        elif 'P' in each_k:
            numPron += pos_count
        elif 'LS' in each_k:
            numLists += pos_count
        elif 'SYM' in each_k:
            numSym += pos_count
        #  Getting total of all 'WH' words
        if 'W' in each_k:
            numWs += pos_count
            
    
    pos_count_dict = {'FW':numFor, 'W':numWs, 'DT':numDet, 'NN':numNouns, 'VB':numVerbs, 'JJ':numAdjs, 'RB':numAdvs, 'IN':numPreps, 'PR':numPron,
                      'UH':numInters, 'CD':numCards, 'MD':numModal, 'CC':numCC, 'TO':numTO, 'RP':numPart, 'EX':numEx, 'POS':numPOSs, 'LS':numLists,
                      'SYM':numSym, 'Totals':numTotal}
    
    
    return pos_count_dict
####################################################################################################################################################
####################################################################################################################################################

tree_get = re.compile('tree-(.*)$')

#  Constant variable for writing to file (word widths) 
SENTENCE_WIDTH = 45
NUMBER_WIDTH = 20
NUMBER_WIDTH2 = 23
NUMBER_PREC = "%8.2f"

#  Constant variables for Rounding level and Log base
ROUNDNUM = 2
LOGNUM = 2

## Function to deal with the parsed files and process through them.
## It requires the path where the parsers saved the new parsed files.
## For each file in the directory it will send the file to the
## Process_Parsed_File() function to process each file.

def Main_Process_Files(input_filename, output_filename):

    #  Default paths, file and variable for Isaiah data
    data_list_path = ''

#  Path of the Total vs Unique Word list
    total_unique_file = "./temp/TotalvsUnique.txt"
       
    #  Iterating through each file in the pre-parsed tree to process through
    #  Sending each 'file' to the Process_Parsed_Files method to process all data
       
    #  Processing the Tree File
    word_totals = Process_Parsed_File(input_filename, output_filename)
    #print('!!!!!!!!!!!!!!!!!!')
        
    totalCount = word_totals[0]
    print('total:', totalCount)
    uniqueCount = word_totals[1]
    print('unique:', uniqueCount)
        
    #if os.path.exists(total_unique_file):
     #   total_unique = open(total_unique_file, 'a')
    #else:
     
    total_unique = open(total_unique_file, 'w')
    total_unique.write("Total".rjust(10) + "Unique".rjust(10) + "Percentage".rjust(16) + "\n")
        
    uniquePercent = float(uniqueCount) / totalCount * 100 if totalCount > 0 else 0
    total_unique.write(str(totalCount).ljust(10) + str(uniqueCount).rjust(10) + "%8.4f".rjust(12) %uniquePercent + "%\n")
    total_unique.close()
        
    return
 
def Process_Parsed_File(input_filename, output_filename):
    
    unique_cnts_pick_file = "./temp/Unique-Dict-Cnts"
    unique_pick_file = "./temp/Unique-Dict"
    
    unique_word_dict = RetrievePickleFile(unique_cnts_pick_file, "Unique Dict")
    
    complexity_lists = Tree_Processor(input_filename)

    print('***********')
    word_dict = complexity_lists[3]
    wordTotals = unique_word_dict["@@TOTALS@@"] if "@@TOTALS@@" in unique_word_dict else 0
    
    for each_word in word_dict.keys():
        if not each_word == "@@TOTALS@@" and not each_word == "@@UNIQUE@@":
            unique_word_dict[each_word] = unique_word_dict[each_word] + word_dict[each_word] if each_word in unique_word_dict else word_dict[each_word]
            wordTotals += word_dict[each_word]
    
    word_counts = Get_Word_Counts(word_dict)
    
    totalWords = word_counts[0]
    uniqueWords = word_counts[1]
    
    print_string = ("Files Total Words: " + str(totalWords)
                  + "\tFiles Unique: " + str(uniqueWords)
                  + "\tRunning Total: " + str(wordTotals) 
                  + "\tTotal Unique: " + str(len(unique_word_dict)) + "\n")

    print_file = open("./temp/running-count.txt", 'w')
    print_file.write(print_string)
    print_file.close()
        
    unique_word_dict["@@TOTALS@@"] = wordTotals
    unique_word_dict["@@UNIQUE@@"] = len(unique_word_dict)
        
    #Compute_Complexities(complexity_lists)
    
    SavePickleFile(unique_word_dict, unique_cnts_pick_file, True)  
    
    unique_file = open(unique_pick_file + ".txt", 'w')
    
    for key in sorted(unique_word_dict.keys()):
        unique_file.write(key + "\n")
    
    unique_file.close()
    
    return totalWords, uniqueWords

def Get_Word_Counts(word_dict):
    wordTotal = 0
    
    for each_k in word_dict.keys():
        wordTotal += word_dict[each_k]
        
    uniqueTotal = len(word_dict)
    
    return wordTotal, uniqueTotal

#Compute_Complexities

def Compute_Complexities(complexity_lists):
    print('compute complexities bug')
    struct_flag = True
    num_flag = True
       
    data_name = ""
    if struct_flag and num_flag:
        data_name = data_name + "All"
    elif struct_flag and not num_flag:
        data_name = data_name + "MostNoNum"
    elif not struct_flag and num_flag:
        data_name = data_name + "MostNum"
    elif not struct_flag and not num_flag:
        data_name = data_name + "Basic"
        
    data_list_main = RetrievePickleFile(data_name, "Data-List" + data_name, False)
    
    sentence_dict = complexity_lists[0]             #  Dictionary for total Sentences
    word_dict = complexity_lists[3]                 #  Dictionary for all the words
    pos_dict = complexity_lists[4]
    tree_height_list = complexity_lists[5]
    
    pos_count_dict = Get_POS_Counts(pos_dict)

    #  Entire complexity list for each student/speaker
    main_complexity_list = []

    #  File to save all the complexity information into csv format.
    csv_path = "./temp/Complexity_Data" + ".csv"
    
    numSentences = sentence_dict["(ROOT"] if "(ROOT" in sentence_dict else 0
    
    if numSentences == 0:
        print("NO sentences in '" + str(file_name) + "'")
        return
    
    totalWords = pos_count_dict["Totals"] if "Totals" in pos_count_dict else 0
    averageWords = round(float(totalWords) / numSentences, ROUNDNUM) if numSentences > 0 else 0

    #  Getting tree heights
    totalHeights = 0
    for each_height in tree_height_list:
        totalHeights += each_height
    numOfHeights = each_height            
    
    averageHeights = round((float(totalHeights) / numOfHeights), ROUNDNUM) if numOfHeights > 0 else 0
    
    #  Tree Heights compared to words and sentences
    perOfTree = Get_Avg_Per(numOfHeights, totalWords, 100, "perOfTree")
    avgOfTree = Get_Avg_Per(numOfHeights, numSentences)

    numOfUnique = len(word_dict)
    perOfUnique = Get_Avg_Per(numOfUnique, totalWords, 100)
    avgOfUnique = Get_Avg_Per(numOfUnique, numSentences)
    
    sent_struct_list = [("(S", sentence_dict, True, "S"),                           ("(SBAR", sentence_dict, True, "SBAR"), 
                        ("(SBARQ", sentence_dict, True, "SBARQ"),                   ("(NP", sentence_dict, True, "Noun Phrase"),
                        ("(VP", sentence_dict, True, "Verb Phrase"),                ("(ADJP", sentence_dict, True, "Adjective Phrase"),
                        ("(ADVP", sentence_dict, True, "Adverb Phrase"),            ("(CONJP", sentence_dict, True, "Conjunction Phrase"),
                        ("(FRAG", sentence_dict, True, "Fragment"),                 ("(PP", sentence_dict, True, "Prepositional Phrase"),
                        ("(SQ", sentence_dict, True, "Question"),
                        ("(WHNP", sentence_dict, False, "WH Noun Phrase"),          ("(WHVP", sentence_dict, False, "WH Verb Phrase"),
                        ("(WHADJP", sentence_dict, False, "WH Adjective Phrase"),   ("(WHADVP", sentence_dict, False, "WH Adverb Phrase"),
                        ("(WHPP", sentence_dict, False, "WH Prepositional Phrase"), ("(INTJ", sentence_dict, False, "Interjection Phrase"),
                        ("(PRN", sentence_dict, False, "PRN"),                      ("(PRT", sentence_dict, False, "PRT"),
                        ("(SINV", sentence_dict, False, "SINV"),                    ("(QP", sentence_dict, False, "Question Phrase"),
                        ("(X", sentence_dict, False, "Symbol Phrase"),              ("(UCP", sentence_dict, False, "UCP"),
                        ("(RRC", sentence_dict, False, "RRC"),                      ("(LST", sentence_dict, False, "List Phrase"),
                        
                        ("NN", pos_count_dict, True, "Noun"),                      ("VB", pos_count_dict, True, "Verb"), 
                        ("JJ", pos_count_dict, True, "Adjective"),                 ("RB", pos_count_dict, True, "Adverb"),
                        ("IN", pos_count_dict, True, "Preposition"),               ("DT", pos_count_dict, True, "Determiner"),
                        ("PR", pos_count_dict, True, "Pronoun"),                   ("UH", pos_count_dict, True, "Interjection"),
                        ("RP", pos_count_dict, True, "Particle"),                  ("CD", pos_count_dict, False, "Cardinal Number"),
                        ("CC", pos_count_dict, False, "Coordinating Conjunction"), ("MD", pos_count_dict, False, "Modal"),
                        ("TO", pos_count_dict, False, "To"),                       ("EX", pos_count_dict, False, "Existential there"),
                        ("POS", pos_count_dict, False, "Possessive Ending"),       ("LS", pos_count_dict, False, "List Item Marker"),
                        ("SYM", pos_count_dict, False, "Symbol"),                  ("FW", pos_count_dict, False, "Foreign Word"),
                        ("W", pos_count_dict, False, "WH Word")
                        ]
      
    master_struct_list = {}

    conja = 'and'
    conjb = 'but'
    conjo = 'or'
    conjf = 'for'
    
    row = f.readline()

    main_complexity_list.append(("Q_N", row[0:2], "numeric", "Q_N"))
    main_complexity_list.append(("Sentence_Number", numSentences, "numeric", "Sentence_Number"))

    #main_complexity_list.append(("Num_of_Sentences", numSentences, "numeric", "NumSent"))
    main_complexity_list.append(("Num_of_Words", row.count(' '), "numeric", "totalWords"))
    #main_complexity_list.append(("Avg_Words_Per_Sentence", averageWords, "numeric", "AvgWord"))
    main_complexity_list.append(("Tree_Height", numOfHeights, "numeric", "AvgTH"))

    main_complexity_list.append(("AND", row.count(conja), "numeric"))
    main_complexity_list.append(("BUT", row.count(conjb), "numeric"))
    main_complexity_list.append(("OR", row.count(conjo), "numeric"))
    main_complexity_list.append(("FOR", row.count(conjf), "numeric"))

    main_complexity_list.append(("Num_Unique_Word", numOfUnique, "numeric", "NumUnique"))
    main_complexity_list.append(("N100_Unique_Word", perOfUnique, "numeric", "N100Unique"))
    main_complexity_list.append(("Avg_Unique_Word", avgOfUnique, "numeric", "AvgUnique"))

    data_file_name = "./temp/data"
        
    write_file = open(data_file_name, 'a')
    
    write_file.write("Data: ".ljust(SENTENCE_WIDTH) + "\n\n")

    write_file.write("Q_N:".ljust(SENTENCE_WIDTH) + str(999).rjust(NUMBER_WIDTH2) + "\n") 
    
    write_file.write("Sentence_Number:".ljust(SENTENCE_WIDTH) + str(000).rjust(NUMBER_WIDTH2) + "\n\n")
        
    write_file.write("Number of Words:".ljust(SENTENCE_WIDTH) + NUMBER_PREC.rjust(NUMBER_WIDTH) %totalWords + "\n")
    write_file.write("Number of Sentences:".ljust(SENTENCE_WIDTH) + NUMBER_PREC.rjust(NUMBER_WIDTH) %numSentences + "\n")
    write_file.write("Total Tree Height:".ljust(SENTENCE_WIDTH) + NUMBER_PREC.rjust(NUMBER_WIDTH) %totalHeights+ "\n\n")
    
    write_file.write("Average Words Per Sentence:".ljust(SENTENCE_WIDTH) + NUMBER_PREC.rjust(NUMBER_WIDTH) %averageWords + "\n")
    write_file.write("Average Tree Height:".ljust(SENTENCE_WIDTH) + NUMBER_PREC.rjust(NUMBER_WIDTH) %averageHeights + "\n\n")

    write_file.write("Number of Unique Words:".ljust(SENTENCE_WIDTH) + NUMBER_PREC.rjust(NUMBER_WIDTH) %numOfUnique + "\n")
    write_file.write("N100W of Unique Words:".ljust(SENTENCE_WIDTH) + NUMBER_PREC.rjust(NUMBER_WIDTH) %perOfUnique + "\n")
    write_file.write("Average of Unique Words:".ljust(SENTENCE_WIDTH) + NUMBER_PREC.rjust(NUMBER_WIDTH) %avgOfUnique + "\n")

    write_file.write("\n")   
    
    for each_set in sent_struct_list:
        each_pos = each_set[0]
        each_dict = each_set[1]
        each_flag = each_set[2]
        each_desc = each_set[3]
        
        cur_pos = re.sub("\(", "", each_pos)
        cur_num = each_dict[each_pos] if each_pos in each_dict else 0
        cur_per = Get_Avg_Per(cur_num, totalWords, 100)
        cur_avg = Get_Avg_Per(cur_num, numSentences)
        cur_log = 1
        
        master_struct_list[each_pos] = (cur_pos, cur_num, cur_per, cur_avg, cur_log, each_flag, each_desc)
        if struct_flag or each_flag:
            if num_flag:
                main_complexity_list.append(("N" + cur_pos, cur_num, "numeric", "N" + cur_pos))
            main_complexity_list.append(("W" + cur_pos, cur_per, "numeric", "W" + cur_pos))
            main_complexity_list.append(("A" + cur_pos, cur_avg, "numeric", "A" + cur_pos))
            
        write_file.write(str("Number of " + each_desc + "s:").ljust(SENTENCE_WIDTH) + NUMBER_PREC.rjust(NUMBER_WIDTH) %cur_num + "\n")
        write_file.write(str("N100W of " + each_desc + "s:").ljust(SENTENCE_WIDTH) + NUMBER_PREC.rjust(NUMBER_WIDTH) %cur_per + "\n")
        write_file.write(str("Average of " + each_desc + "s:").ljust(SENTENCE_WIDTH) + NUMBER_PREC.rjust(NUMBER_WIDTH) %cur_avg + "\n")
        write_file.write("\n")
    
    write_file.close()
    
        #  Adding current students data into the grand total lists
    data_list_main.append(main_complexity_list)
                   
    if not os.path.exists(csv_path):
        csv_file = open(csv_path, 'a')
        print('length:', len(main_complexity_list))
        for e_element in main_complexity_list:
            csv_file.write(str(e_element[0]) + ",")
        print(("Number of Words:".ljust(SENTENCE_WIDTH) + NUMBER_PREC.rjust(NUMBER_WIDTH) %totalWords + "\n"))
        csv_file.write("\n")
        
    else:
        csv_file = open(csv_path, 'a')
        print(("Word Count:".ljust(SENTENCE_WIDTH) + NUMBER_PREC.rjust(NUMBER_WIDTH) %totalWords + "\n"))
    
    for e_element in main_complexity_list:
        e_data = e_element[1]
        csv_file.write(str(e_data) + ",") if not isinstance(e_data, float) else csv_file.write("%.2f" %e_data + ",")
    csv_file.write("\n")
    
    csv_file.close()
    #close other files here
    
    SavePickleFile(data_list_main, data_name, False, False)
        
    return

#--

input_filename = "./ttt"
output_filename = "./temp/wilde8.txt";

if sys.argv.__len__() > 1:
    input_filename = sys.argv[1]
if sys.argv.__len__() > 2:
    output_filename = sys.argv[2]


#input_filename = input_file
#output_filename = output_file
f = open("./wilde2.txtmarkup", 'r')
Main_Process_Files(input_filename, output_filename)
#Tree_Processor(input_filename)
