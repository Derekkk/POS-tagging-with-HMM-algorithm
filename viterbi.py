import math

# Use the wikipedia page for Viterbi algorithm as reference
# Wikipedia page: https://en.wikipedia.org/wiki/Viterbi_algorithm


###############################################
# viterbi fuction for viterbi algorithm, use Wikipedia page as reference
#Input: observations: tuple of tokens, eg: ('What','if','Google','Morphed','Into','GoogleOS','?')
#       states: tuple of all tags
#       start_p: dictionary of start probability, eg: {'ADV': 0.07948656621222992, 'NOUN': 0.06641154428765048, 'ADP': 0.04273299848521087, ...}
#       trans_p: transition probability, with format of dictionary
#       emit_p: emission probability, with format of dictionary
#Output: (probability, state), eg:(0, ['X', 'X', 'X', 'X', 'X', 'X', 'X'])
################################################

def viterbi(obs, states, start_p, trans_p, emit_p):
    V = [{}]
    path = {}

    # Initialize base cases (t == 0)
    for y in states:
        if  emit_p[y].has_key(obs[0]):
            V[0][y] = start_p[y] * emit_p[y][obs[0]]
        else:
            V[0][y] = 0
        path[y] = [y]


    # Run Viterbi for t > 0
    for t in range(1, len(obs)):
        V.append({})
        newpath = {}

        for y in states:

            temp = []
            for y0 in states:
                if V[t - 1][y0] >= 0:
                    if trans_p[y0].has_key(y) and emit_p[y].has_key(obs[t]):
                        temp.append((V[t - 1][y0] * trans_p[y0][y] * emit_p[y][obs[t]], y0))
                    else:
                        temp.append((0,y0))

            (prob, state) = max(temp)

            V[t][y] = prob
            newpath[y] = path[state] + [y]

        path = newpath

    #t = len(obs) - 1
    (prob, state) = max((V[len(obs) - 1][y], y) for y in states)
    return (prob, path[state])


