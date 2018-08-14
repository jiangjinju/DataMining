from pos_solver import *
import sys

# Read in training or test data file
#
def read_data(fname):
    exemplars = []
    file = open(fname, 'r');
    for line in file:
        data = tuple([w.lower() for w in line.split("|")])
        line = tuple([w.lower() for w in data[0].split()])
        author =  data[1].rstrip()
        lengthLine = len(list(line))
        exemplars += [(line,tuple([author]*lengthLine)),]        
    return exemplars



####################
# Main program
#



for count in range(1,11):
    train_file = "train_part"+str(count)+".txt"
    test_file = "test_part"+str(count)+".txt"
    #(train_file, test_file) = ("train_part2.txt","test_part2.txt")

    #print "Learning model..."
    solver = Solver()
    train_data = read_data(train_file)
    solver.train(train_data)

    #print "Loading test data..."
    test_data = read_data(test_file)

    #print "Testing classifiers..."
    Algorithms = ("HMM MAP",)
    Algorithm_labels = ['1. HMM MAP']

    error_count = 0
    sent_no = 1
    #print "sentence,mws,eap,hpl,P_LABEL,C_LABEL"

    for (s, gt) in test_data:
        outputs = list()
        # run all algorithms on the sentence
        for (algo, label) in zip(Algorithms, Algorithm_labels):
            outputs = copy.deepcopy(solver.solve( algo, s))
            authors = [0]*3
            gt_list = list(gt)
            total_words = len(gt_list)
            #print outputs
            for i in range(0,total_words):
                if outputs[i] == "mws":
                    authors[0] += 1.0
                if outputs[i] == "eap":
                    authors[1] += 1.0
                if outputs[i] == "hpl":
                    authors[2] += 1.0
            author_id = authors.index(max(authors))        
            if author_id == 0:
                author_name = "MWS"
            if author_id == 1:
                author_name = "EAP"
            if author_id == 2:
                author_name = "HPL"                        
            #print str(sent_no)+","+str(round(float(authors[0]/total_words),3))+","+str(round(float(authors[1]/total_words),3))+","+str(round(float(authors[2]/total_words),3))+","+author_name+","+gt_list[0].upper()+","+str(author_name.lower() == gt_list[0])
            sent_no += 1
            if author_name.lower() != gt_list[0]:
                error_count += 1.0
    print str(count)+" Accuracy:"+str(float(1 - error_count/sent_no)*100)+"%"
#    print "----"
