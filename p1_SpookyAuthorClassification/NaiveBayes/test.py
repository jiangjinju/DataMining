import re
import math
import sys
import csv


#with open('train.csv', 'rb') as csvfile:
#    spamreader = csv.reader(csvfile, delimiter=' ', quotechar='')
#    for row in spamreader:
#        print ', '.join(row)

f = open('output.txt', "w")

def eliminateStopWords(word_list):
    noset = {'ourselves', 'hers', 'between', 'yourself', 'but', 'again', 'there', 'about', 'once', 'during', 'out',
             'very',
             'having', 'with', 'they', 'own', 'an', 'be', 'some', 'for', 'do', 'its', 'yours', 'such', 'into', 'of',
             'most',
             'itself', 'other', 'off', 'is', 's', 'am', 'or', 'who', 'as', 'from', 'him', 'each', 'the', 'themselves',
             'until',
             'below', 'are', 'we', 'these', 'your', 'his', 'through', 'don', 'nor', 'me', 'were', 'her', 'more',
             'himself',
             'this', 'down', 'should', 'our', 'their', 'while', 'above', 'both', 'up', 'to', 'ours', 'had', 'she',
             'all', 'no',
             'when', 'at', 'any', 'before', 'them', 'same', 'and', 'been', 'have', 'in', 'will', 'on', 'does',
             'yourselves',
             'then', 'that', 'because', 'what', 'over', 'why', 'so', 'can', 'did', 'not', 'now', 'under', 'he', 'you',
             'herself', 'has', 'just', 'where', 'too', 'only', 'myself', 'which', 'those', 'i', 'after', 'few', 'whom',
             't',
             'being', 'if', 'theirs', 'my', 'against', 'a', 'by', 'doing', 'it', 'how', 'further', 'was', 'here',
             'than'}

in_file = open('train.txt', 'r')  # open file lorem.txt for reading text data
contents = in_file.read()  # read the entire file into a string variable
#in_file.close()

newList = []

contents = contents.rstrip().strip()  ##space removal from each line
contArr = contents.splitlines()

j = 0

#print newList

author_list = []  ##stores all the location from training data
text_list = []  ## list containing each tweets  of every location from training data
i = 0
for x in contArr:
    #print x
        i += 1
        seperator_index = x.index("|")
        # #print seperator_index
        text_list.append(x[:(seperator_index)])
        author_list.append(x[(seperator_index + 1):])

#print text_list
unique_author_list = set(author_list)
all_text_list = []
unique_text_list = set()
#print unique_text_list, unique_author_list

text_array = []
punc = set(":+\"()[],./;'?-_!@#1234567890*\\")
for line in text_list:
    strp = ''.join(c for c in line if not c in punc)
    words = strp.lower().split()
    text_array.append(words)
    for current_word in words:
        unique_text_list.add(current_word)
        all_text_list.append(current_word)
#print len(all_text_list),len(unique_text_list)
#print 'hello', text_array
row = len(unique_text_list)
col = len(unique_author_list)

frequency_matrix = [[0 for x in range(col + 2)] for y in range(row + 2)]
probablity_matrix = [[0 for x in range(col + 1)] for y in range(row + 2)]


author_dict = dict()
count = 1
for item in unique_author_list:
    # e = next(iter(unique_loc_set))
    frequency_matrix[0][count] = item
    probablity_matrix[0][count] = item
    author_dict[item] = count
    count += 1
frequency_matrix[0][count] = "Total"
frequency_matrix[(len(unique_text_list) + 1)][0] = "Total"

author_count = dict()
for item in author_list:
    if (item in author_count):
        author_count[item] += 1
    else:
        author_count[item] = 1

count = 1
unique_text_dict = dict()
for item in unique_text_list:
    frequency_matrix[count][0] = item
    probablity_matrix[count][0] = item
    unique_text_dict[item] = count
    count += 1

##frequency_matrix contains the frequency of a word repeated under each location
   #print len(sentenceArray),sentenceArray
   #print  author_list[count]
count = 0
for sentenceArray in text_array:
        #print sentenceArray
        author = author_list[count]
        for word in sentenceArray:
            frequency_matrix[unique_text_dict[word]][author_dict[author]] += 1
            #print word,author,frequency_matrix[unique_text_dict[word]][author_dict[author]]
        count += 1
#print frequency_matrix

xLastIndex = len(frequency_matrix) - 1
yLastIndex = len(frequency_matrix[0]) - 1

totalRowSum = 0
totalColSum = 0


# Calculates total of row
for x in range(1, len(frequency_matrix)):
    totalRowSum = 0
    for y in range(1, len(frequency_matrix[0])):
        totalRowSum += frequency_matrix[x][y]
        # #print "frequency_matrix["+str(x)+"]["+str(y)+"] =" + str(frequency_matrix[x][y])
    frequency_matrix[x][len(frequency_matrix[0]) - 1] = totalRowSum


# Calculate total of column i.e.total number of word in each location
for y in range(1, len(frequency_matrix[0])):
    totalColSum = 0
    for x in range(1, len(frequency_matrix) - 1):
        totalColSum += frequency_matrix[x][y]
    # #print 'totalColSum for '+str(y)+" = "+str(totalColSum)
    frequency_matrix[len(frequency_matrix) - 1][y] = totalColSum

for i in range(1, len(frequency_matrix)):
    for j in range(1, len(unique_author_list) + 1):
        # #print  frequency_matrix[i+1][j],frequency_matrix[len(frequency_matrix)-1][j]
        a = frequency_matrix[i][j]  ##no. of times a word has repeat in a location
        b = frequency_matrix[len(frequency_matrix) - 1][j]  ##total of word in that sepcific location
        c = len(unique_text_list)  ##all the unique words
        probablity_matrix[i][j] = -(math.log(((a + 1) / float(b + c))))  # * (d / float(e))))

#print probablity_matrix
#reading test file
in_file = open('test.txt', "rt")  # open file lorem.txt for reading text data
test_data = in_file.read()  # read the entire file into a string variable
in_file.close()

test_data = test_data.rstrip().strip()
tempArr = test_data.splitlines()
wordTest_list=[]
#array = []
#with open("test.txt", "r") as ins:
#    lines = [line.lower().split() for line in ins]
#print lines

unique_text_set_test=set()
all_text_list_test=[]

lines=[]
punc = set(":+\"()[],./;'?-_!@#1234567890*\\")
for line in tempArr:
    #print line
    strp = ''.join(c for c in line if not c in punc)
    words = strp.lower().split()
    lines.append(words)
    for current_word in words:
        unique_text_set_test.add(current_word)
        all_text_list_test.append(current_word)
#print len(unique_text_set_test), len(all_text_list_test)
#print lines

for i in range(len(lines)):
    temp_test_prod_dict = dict()
    #print all_text_list_test[i]
    for k in range(1, len(unique_author_list) + 1):
        prod_prob_per_tweet = 1
        for j in range(len(lines[i])):
            word = lines[i][j]
            #print word
            #word = all_text_list_test[i]
            try:
                index_probablity_of_text = unique_text_dict[word]
                
            except:
                KeyError
                index_probablity_of_text = -1

        #print index_probablity_of_text,word
            if index_probablity_of_text != -1:
                total = probablity_matrix[index_probablity_of_text][k]
                prod_prob_per_tweet *= total
            else:
                a = 0
                b = frequency_matrix[len(frequency_matrix) - 1][k]  ##total of word in that sepcific location
                c = len(unique_text_list)  ##all the unique words
                d = author_count[frequency_matrix[0][k]]  ##no. of times a location has repeated
                e = len(author_list)  ##all the location
                total = -(math.log(((a + 1) / float(b + c)) * (d / float(e))))
                # #print " ELSE CASE Total of '"+ word+ "' in region "+frequency_matrix[0][k] +" ="+str(total)
                prod_prob_per_tweet *= total
        temp_test_prod_dict[frequency_matrix[0][k]] = prod_prob_per_tweet
    max_value = min(temp_test_prod_dict.values())
    result = [key for key, value in temp_test_prod_dict.iteritems() if value == max_value]
    # #print "suggested elem ="+str(result)
    line = ""
    for word in lines[i]:
        line += " " + word
    # print "---------------------------"
    # print "****" + line + "*****"
    #print result[0]
    #print result[0],(lines[i]) 
    f.write(result[0] + ',  ' + str(lines[i]) + '\n')