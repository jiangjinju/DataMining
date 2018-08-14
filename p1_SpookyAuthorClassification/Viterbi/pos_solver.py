import random
import math
import copy

class Solver:

    # Calculate the log of the posterior probability of a given sentence
    #  with a given part-of-speech labeling
    def posterior(self, sentence, label):
        return 0
    #def posterior(self, sentence, label):
    #    print sentence
    #    print label
    #    return 0

    # Do the training!
    #
#    def train(self, data):
#        pass
    def train(self, data):
        self.first_pos_count = dict() #count of initial pos
        self.emission_count = dict() #count of word-pos associations
        self.transition_count = dict() #count of pos-pos transitions
        self.POSCount = dict() #count of each pos
        self.WordCount = dict() #counnt of each word
        for i in data:
            cur_word_set = i[0]
            cur_pos_set =  i[1]
            for j in range (0,len(cur_word_set)):
                if j != 0:
                    prev_word = cur_word
                    prev_pos = cur_pos
                    cur_word = cur_word_set[j]
                    cur_pos = cur_pos_set[j]                
                    transition_var = prev_pos + cur_pos
                    if self.transition_count.has_key(transition_var):
                        self.transition_count[transition_var]+=1.0
                    else:
                        self.transition_count.update({transition_var:1.0})                
                else:
                    cur_word = cur_word_set[j]
                    cur_pos = cur_pos_set[j]                
                    if self.first_pos_count.has_key(cur_pos):
                        self.first_pos_count[cur_pos_set[j]]+=1.0
                    else:
                        self.first_pos_count.update({cur_pos:1.0})
                emission_var = cur_word + cur_pos
                if self.emission_count.has_key(emission_var):
                    self.emission_count[emission_var]+=1.0
                else:
                    self.emission_count.update({emission_var:1.0})

                if self.POSCount.has_key(cur_pos):
                    self.POSCount[cur_pos]+=1.0
                else:
                    self.POSCount.update({cur_pos:1.0})                    
        #Calculating Emission Probability
        self.emission_probab = copy.deepcopy(self.emission_count)
        for pos in self.POSCount.keys():
            for wordPos in list(k for k,v in self.emission_probab.iteritems() if pos in k.lower()):
                self.emission_probab[wordPos] = self.emission_probab[wordPos] / self.POSCount[pos]
        #Calculating Transition Probability
        self.transition_probab = copy.deepcopy(self.transition_count)
        for pos in self.POSCount.keys():
            for wordPos in list(k for k,v in self.transition_probab.iteritems() if pos == k[-len(pos):].lower()):
                self.transition_probab[wordPos] = self.transition_probab[wordPos] / self.POSCount[pos]
        #Calculating First POS Probability
        self.first_pos_probab = copy.deepcopy(self.first_pos_count)
        self.first_pos_probab = {k: v / total for total in (sum(self.first_pos_probab.itervalues(), 0.0),) for k, v in self.first_pos_probab.iteritems()}
        #Calculating the POS probab
        self.PosProbab = copy.deepcopy(self.POSCount)
        self.PosProbab = {k: v / total for total in (sum(self.PosProbab.itervalues(), 0.0),) for k, v in self.PosProbab.iteritems()}
        minList = []
        minList.append(min(self.first_pos_probab.itervalues()))
        minList.append(min(self.transition_probab.itervalues()))
        minList.append(min(self.emission_probab.itervalues()))
        self.globalMin = min(minList) * 0.01 #determining a global minimum for calculations
        return False

    def iterateThruArray(self,PosArray,ProbabArray,Column,MaxRow,LastMaxPOS):
        curColumn = 0
        for i in range(Column):
            if PosArray[0][i] == LastMaxPOS:
                curColumn = i
        curMaxPos = PosArray[MaxRow][curColumn]
        if MaxRow == 1:
            ActualFirstPos = curMaxPos
            maxValFirstRow = math.log(self.globalMin)
            for i in range(0,Column):
                curVal =  ProbabArray[1][i]
                if curVal > maxValFirstRow:
                    maxValFirstRow = curVal
                    ActualFirstPos = PosArray[0][i]
            return [ActualFirstPos]
        else:
            MaxString = self.iterateThruArray(PosArray,ProbabArray,Column,MaxRow-1,curMaxPos)
        MaxString.append(LastMaxPOS)
        return MaxString

    def hmm_viterbi(self, sentence):
        posAll = list(self.POSCount.keys())
        ArrayForPOS = [["-" for i in range (len(posAll))]for j in range(len(sentence)+1)]
        for i in range(0,len(posAll)):
            ArrayForPOS[0][i] = posAll[i]
        ArrayForPOSProbabForMax = [[0.0 for i in range (len(posAll))]for j in range(len(sentence)+1)]
        smallestVal = math.log(self.globalMin)
        for i in range(0,len(sentence)):
            j = 0
            Word = sentence[i]
            for pos in posAll:
                WordPos = Word + pos
                priorProbab = math.log(self.PosProbab[pos])
                if self.emission_probab.has_key(WordPos):
                    probabWordPos = math.log(self.emission_probab[WordPos])
                else:
                    probabWordPos = smallestVal + math.log(0.1)
                if i == 0:
                    if self.first_pos_probab.has_key(pos):
                        probabOfFirstPos = math.log(self.first_pos_probab[pos])
                    else:
                        probabOfFirstPos = smallestVal + math.log(0.1)
                    ArrayForPOSProbabForMax[i+1][j] = probabWordPos + probabOfFirstPos
                else:
                    curPosVal = ArrayForPOS[0][j]
                    maxVal = smallestVal
                    prevPosActual = curPosVal
                    for cntr in range(0,len(posAll)):
                        prevPosVal = ArrayForPOS[0][cntr]
                        transitionPOS = prevPosVal + curPosVal
                        if self.transition_probab.has_key(transitionPOS):
                            transVal = math.log(self.transition_probab[transitionPOS])
                        else:
                            transVal = smallestVal - 10
                        prevPosValProbab = ArrayForPOSProbabForMax[i][cntr]
                        curVal = prevPosValProbab + transVal
                        if smallestVal > curVal:
                            smallestVal = curVal
                        if maxVal < curVal:
                            maxVal = curVal
                            prevPosActual = prevPosVal
                        ArrayForPOSProbabForMax[i+1][j] = probabWordPos + maxVal
                        ArrayForPOS[i+1][j] = prevPosActual
                j += 1
        maxString = []
        lastRowMaxCol = smallestVal + math.log(0.1)
        for i in range(0,len(posAll)):
            curVal =  ArrayForPOSProbabForMax[len(sentence)][i]
            if curVal > lastRowMaxCol:
                lastRowMaxCol = curVal
                lastRowMaxPOS = ArrayForPOS[len(sentence)][i]
                ActualLastPos = ArrayForPOS[0][i]
        if len(sentence) !=1:
            maxString = self.iterateThruArray(ArrayForPOS,ArrayForPOSProbabForMax,len(posAll),len(sentence)-1,lastRowMaxPOS)
        maxString.append(ActualLastPos)
        return maxString

    # This solve() method is called by label.py, so you should keep the interface the
    #  same, but you can change the code itself. 
    # It should return a list of part-of-speech labelings of the sentence, one
    #  part of speech per word.
    #
    def solve(self, algo, sentence):
        if algo == "HMM MAP":
            return self.hmm_viterbi(sentence)
        else:
            print "Unknown algo!"