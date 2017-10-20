import csv
import pandas as pd
from viterbi import viterbi

'''Read data'''
print "Step 1: read data"

DIR = ''
fname = 'train.counts'
fpath = DIR+fname
#read file
rows = []
f=open(fpath, 'rb')
lines = f.readlines()
f.close()
#remove '\n'
for line in lines:
    line = line.rstrip('\n')
    rows.append([line])

Emission_count = [row[0].split() for row in rows[:22189]] # Read the text and remove all the unnecessary symbols
Bigram_count = [row[0].split() for row in rows if row[0].strip().split()[1] == "2-GRAM"]

#print 'Emission_count: ',Emission_count[:10]
#print 'Bigram_count: ',Bigram_count[:5]

#coumpute the tags and their counts, eg:[['ADV', 10551], ['NOUN', 35315], ['ADP', 17640]]
tag = []    #all the appeared tags
word = []
for w in Emission_count:
    tag.append(w[2])
    word.append(w[3])
tag_no_rep = list(set(tag)) #remove the reprtition
tag_count = [[i,0] for i in tag_no_rep]
word_no_rep = list(set(word))
word_count = [[i,0] for i in word_no_rep]
for element in Emission_count:
    tag_count[tag_no_rep.index(element[2])][1] += eval(element[0])
    word_count[word_no_rep.index(element[3])][1] += eval(element[0])

#print tag_count
#tag_count is: [['ADV', 10551], ['NOUN', 35315], ['ADP', 17640], ['PRON', 17183], ['SCONJ', 3842], ['PROPN', 12945], ['DET', 17148], ['SYM', 598], ['INTJ', 688], ['PART', 5564], ['PUNCT', 23680], ['NUM', 3999], ['AUX', 7895], ['X', 848], ['CONJ', 6707], ['ADJ', 12475], ['VERB', 27508]]
#tag_no_rep is: ['ADV', 'NOUN', 'ADP', 'PRON', 'SCONJ', 'PROPN', 'DET', 'SYM', 'INTJ', 'PART', 'PUNCT', 'NUM', 'AUX', 'X', 'CONJ', 'ADJ', 'VERB']
#word_count is: [['Unemployent', 1], ['Andreas', 1], ['CONFIRMIT', 1], ['Roofing', 1], ['affirms', 1], ['worshiped', 1],...]

''''--------------------------<UNK>------------------------'''
'''UNK'''
print "Step to: UNK handling"

Emission_count_UNK = []
UNK_element = []
UNK_word = []
for i in word_count:
    if i[1] < 2:
        UNK_word.append(i[0])


for i in Emission_count:
    if i[3] in UNK_word:
        UNK_element.append([i[0],i[1],i[2],'UNK'])
    else:
        Emission_count_UNK.append(i)

temp = []
for tag in tag_no_rep:
    count_tag = 0
    for ele in UNK_element:
        if ele[2] == tag:
            count_tag += eval(ele[0])
    temp.append([str(count_tag), 'WORDTAG', tag, 'UNK'])
#print 'temp: ',temp
#print 'emission_count_unk: ',len(Emission_count_UNK)
#print 'UNK_ele: ',len(UNK_element)
Emission_count_UNK += temp
#print 'emission_count_unk: ',Emission_count_UNK[:10]

'''Question 4.1, emission probabilities'''
print "Step 3: Compute emission_prob"
####################################################################
###Question 4, part 1
###Emission_Prob function: Compute emission probabilities
###input: dataset of a list, with the form of [['<count>', 'WORDTAG', '<tag>', '<word>'],...]
###output: emission prob result, list with the form of [['<word>', '<tag>', prob value],...]
###################################################################
def Emission_Prob(Emission_count):
    word = []   #all the appeared words
    tag = []    #all the appeared tags
    word_count = []     #word_count list

    for w in Emission_count:
        word.append(w[3])
        tag.append(w[2])
        word_count.append([w[3],w[2],eval(w[0])])

    word_no_rep = list(set(word)) #remove the repetition
    tag_no_rep = list(set(tag)) #remove the reprtition
    tag_sum = [[i,0] for i in tag_no_rep]

    for element in Emission_count:
        tag_sum[tag_no_rep.index(element[2])][1] += eval(element[0])

    #compute the emission prob

    for element in word_count:
        j = tag_no_rep.index(element[1])
        #print "j: ",j
        temp = element[2]*1.0
        #print temp,tag_sum[j][1]
        element[2] = temp/(tag_sum[j][1])

    return word_count

emission_prob = Emission_Prob(Emission_count_UNK)
#print 'emission_prob: ', len(emission_prob),emission_prob[:10]


'''Question 4.2 Transition probabilities'''
print "Step 4: Compute Transition_prob"
####################################################################
###Question 4, part2
###Transition_Prob function: Compute transition probabilities
###input: a list of 2-gram counts, with the form of [['433', '2-GRAM', 'PART', 'NOUN'], ['625', '2-GRAM', 'PUNCT', 'ADP'], ['445', '2-GRAM', 'VERB', 'VERB']]
###output: transition prob result, list with the form of [[prob(tag1,tag2), '<tag1>', '<tag2>'],...]
###################################################################
def Transition_Prob(Bigram_count):
    start_symbol = [x for x in Bigram_count if x[2] == '*' and x[3]!='*']
    count_StartTag = 0  # the number of tag * (start tag)
    for elem in start_symbol:
        count_StartTag += eval(elem[0])

    Bigram_tag = [[t[0],t[2],t[3]] for t in Bigram_count] #eg: [['433', 'PART', 'NOUN'], ['625', 'PUNCT', 'ADP'], ['445', 'VERB', 'VERB'],...]
    tran_prob = []

    start_probability = {}#test
    for elem in Bigram_tag:
        if elem[1]!='*':
            prob = (eval(elem[0]) * 1.0) / tag_count[tag_no_rep.index(elem[1])][1]
            tran_prob.append([prob,elem[1],elem[2]])
        if elem[1]=='*' and elem[2]!='*':
            prob = (eval(elem[0]) * 1.0)/count_StartTag
            #tran_prob.append([prob, elem[1], elem[2]])
            start_probability[elem[2]] = prob #test
    return tran_prob,start_probability



tran_prob,start_probability = Transition_Prob(Bigram_count)


"""Convert list to Dic as the input for Viterbi Algorithm"""

states = tuple(tag_no_rep)
transition_probability = {}
for elem in tran_prob:
    if transition_probability.has_key(elem[1]):
        transition_probability[elem[1]][elem[2]] = elem[0]
    else:
        transition_probability[elem[1]] = {}
        transition_probability[elem[1]][elem[2]] = elem[0]

emission_probability = {}
for elem in emission_prob:
    if emission_probability.has_key(elem[1]):
        emission_probability[elem[1]][elem[0]] = elem[2]
    else:
        emission_probability[elem[1]] = {}
        emission_probability[elem[1]][elem[0]] = elem[2]



#print emission_probability
#print transition_probability
#print start_probability
#print observations
#print states

'''UNK processing for observations: transfer the unknown words to UNK '''
observations = ('What','if','Google','Morphed','Into','GoogleOS','?')
#observations = ('The','President','has','also','said','he','would','like','to','see','Israel','said','off','the','map','which','he','could','nt','even','begin','to','try','without','nuclear','weapons','.')
#observations = ('I','drafted','the','into','TVA','Option','as','a','series','of','calls','tied','to','the','MOPA','delivery','term','and','quantity','-','not','sure','if','this','anything','close','to','what','you','all','had','in','mind','.')
def observations_process(observations):
    observations_process = []
    Dict = []
    for word in word_no_rep:
        if word not in UNK_word:
            Dict.append(word)

    for elem in observations:
        if elem not in Dict:
            elem = 'UNK'
            observations_process.append(elem)
        else:
            observations_process.append(elem)
    observations = tuple(observations_process)
    #print "observations with UNK: ",observations
    return observations

print 'the first 10 elements of emission_prob: ', emission_prob[:10]
print 'teh first 10 elemnets of transition_prob: ',tran_prob[:10]
#print viterbi(observations_process(observations),states,start_probability,transition_probability,emission_probability)


