#import HMM
from HMM import states,start_probability,transition_probability,emission_probability,observations_process
from viterbi import viterbi


'''Read data'''
'''Read data'''
print "read test data"

DIR = ''
fname = 'test.words'
fpath = DIR+fname
#read file
rows = []
f=open(fpath, 'rb')
lines = f.readlines()
f.close()
#remove '\n'
for line in lines:
    line = line.rstrip('\n')
    rows.append(line)
#print rows[:10]

test_data = []
temp = []
for elem in rows:
    if elem != '':
        temp.append(elem)
    else:
        test_data.append(temp)
        temp = []
print 'test data: ',len(test_data),test_data[:5]

#print viterbi(observations_process(test_data[0]),states,start_probability,transition_probability,emission_probability)[1]

#print test_data[91:93]

Output = []
Counter = 0
for sample in test_data:
    Counter += 1

    print "This is the "+str(Counter)+" sample"
    POS_result = viterbi(observations_process(sample),states,start_probability,transition_probability,emission_probability)[1]
    temp_result = []
    for i in range(len(sample)):
        temp_result.append(sample[i]+' '+POS_result[i])
    Output.append(temp_result)

'''Write the result in a file'''
#When you run the code, remember change the output file name

f = open('Output_result2','w')
for i in Output:
    for j in i:
        f.write(j+'\n')
    f.write('\n')
f.close()
