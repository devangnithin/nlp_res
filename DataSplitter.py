#5494

import sys
import re
import os

input_file = "./temp/Complexity_Data.csv"
train_filename = "Complexity_Data_train.csv"
test_filename = "Complexity_Data_test.csv"

f = open(input_file) #wilde.6.txt
#output_filename = output_file #wilde.7.txt
train_output_file = open(train_filename, 'w')
test_output_file = open(test_filename, 'w')
linecount =0



