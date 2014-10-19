'''
Algorithmic Thinking Project 4:
DP Sequence Alignment
'''

#import math
#import matplotlib.pyplot as plt
#import random
#import urllib2

def is_dash(letter):
    """
    check if the input letter is dash or not
    """
    
    if letter == '-':
        return True
    else:
        return False


def build_scoring_matrix(alphabet, diag_score, off_diag_score, dash_score):
    """
    input:
        a set of characters alphabet and three scores diag_score, off_diag_score,
        and dash_score.
    output:
        a dictionary of dictionaries whose entries are indexed by
        pairs of characters in alphabet plus '-'. The score for any entry indexed
        by one or more dashes is dash_score. The score for the remaining diagonal
        entries is diag_score. Finally, the score for the remaining off-diagonal
        entries is off_diag_score
        
    DONE
    """
    
    ## build the matrix M from alphabet, a set of chars
    my_alphabet = set(alphabet)
    my_alphabet.add('-')
    #print type(my_alphabet)
    scoring_matrix = {}
    for letter_x in my_alphabet:
        scoring_matrix[letter_x] = {}
        for letter_y in my_alphabet:
            if letter_x == letter_y and not is_dash(letter_x):
                scoring_matrix[letter_x][letter_y] = diag_score
            elif letter_x != letter_y and letter_x != '-' and letter_y != '-':
                scoring_matrix[letter_x][letter_y] = off_diag_score
            elif is_dash(letter_x) != is_dash(letter_y):
                scoring_matrix[letter_x][letter_y] = dash_score
            else:
                scoring_matrix[letter_x][letter_y] = dash_score
    
    return scoring_matrix
    

def compute_alignment_matrix(seq_x, seq_y, scoring_matrix, global_flag):
    """
    input:
        two sequences seq_x and seq_y whose elements share a common alphabet with
        the scoring matrix scoring_matrix. The function computes
    output
        the alignment matrix for seq_x and seq_y as described in the Homework.
        If global_flag is True, each entry of the alignment matrix is computed using
        the method described in Question 8 of the Homework. If global_flag is False,
        each entry is computed using the method described in Question 12 of the Homework.
        
    DONE
    """
    
    ## check if input sequences share common alphabet with the scoring matrix
    alphabet = set(scoring_matrix.keys())
    #print "alphbet type:", type(alphabet)
    for letter in seq_x:
        if letter not in alphabet:
            return "Error: input sequences do not share common alphabet with the scoring matrix"
    for letter in seq_y:
        if letter not in alphabet:
            return "Error: input sequences do not share common alphabet with the scoring matrix"
    

    
    ## initialize the alignment matrix as a 2D list
    align_matrix = [ [0 for dummy_col in range(len(seq_y)+1)] for dummy_row in range(len(seq_x)+1)]
    ## compute the 0th row and col
    for idx_i in range(1, len(seq_x)+1):
        letter_x = seq_x[idx_i - 1]
        align_matrix[idx_i][0] = align_matrix[idx_i - 1][0] + scoring_matrix[letter_x]['-']
        ## if local
        if global_flag == False:
            if align_matrix[idx_i][0] < 0:
                align_matrix[idx_i][0] = 0
    
    for idx_j in range(1, len(seq_y)+1):
        letter_y = seq_y[idx_j - 1]
        align_matrix[0][idx_j] = align_matrix[0][idx_j - 1] + scoring_matrix['-'][letter_y]
        ## if local
        if global_flag == False:
            if align_matrix[0][idx_j] < 0:
                align_matrix[0][idx_j] = 0
    
    ## compute other entries
    for idx_i in range(1, len(seq_x)+1):
        for idx_j in range(1, len(seq_y)+1):
            letter_x = seq_x[idx_i - 1]
            letter_y = seq_y[idx_j - 1]
            
            align_matrix[idx_i][idx_j] = max([align_matrix[idx_i - 1][idx_j - 1] + scoring_matrix[letter_x][letter_y],
                                              align_matrix[idx_i - 1][idx_j] + scoring_matrix[letter_x]['-'],
                                              align_matrix[idx_i][idx_j - 1] + scoring_matrix['-'][letter_y]])
            if global_flag == False:
                if align_matrix[idx_i][idx_j] < 0:
                    align_matrix[idx_i][idx_j] = 0
    
    return align_matrix
    

#########################################################################################
def compute_global_alignment(seq_x, seq_y, scoring_matrix, alignment_matrix):
    """
    input:
        two sequences seq_x and seq_y whose elements share a common alphabet with
        the scoring matrix scoring_matrix. This function computes a global alignment of
        seq_x and seq_y using the global alignment matrix alignment_matrix.
    output:
        a tuple of the form (score, align_x, align_y) where score is the score of the
        global alignment align_x and align_y. Note that align_x and align_y should have
        the same length and may include the padding character '-'
        
    DONE
    """
    
    ## check if input sequences share common alphabet with the scoring matrix
    alphabet = set(scoring_matrix.keys())
    #print "alphbet type:", type(alphabet)
    for letter in seq_x:
        if letter not in alphabet:
            return "Error: input sequences do not share common alphabet with the scoring matrix"
    for letter in seq_y:
        if letter not in alphabet:
            return "Error: input sequences do not share common alphabet with the scoring matrix"
    
    idx_i = len(seq_x)
    idx_j = len(seq_y)
    align_x = ""
    align_y = ""
    score = alignment_matrix[idx_i][idx_j]
    
    while idx_i != 0 and idx_j != 0:
        letter_x = seq_x[idx_i - 1]
        letter_y = seq_y[idx_j - 1]
        if alignment_matrix[idx_i][idx_j] == alignment_matrix[idx_i - 1][idx_j - 1] + scoring_matrix[letter_x][letter_y]:
            align_x = letter_x + align_x
            align_y = letter_y + align_y
            idx_i -= 1
            idx_j -= 1
        else:
            if alignment_matrix[idx_i][idx_j] == alignment_matrix[idx_i - 1][idx_j] + scoring_matrix[letter_x]['-']:
                align_x = letter_x + align_x
                align_y = '-' + align_y
                idx_i -= 1
            else:
                align_x = '-' + align_x
                align_y = letter_y + align_y
                idx_j -= 1
    
    while idx_i != 0:
        letter_x = seq_x[idx_i - 1]
        align_x = letter_x + align_x
        align_y = '-' + align_y
        idx_i -= 1

    while idx_j != 0:
        letter_y = seq_y[idx_j - 1]
        align_x = '-' + align_x
        align_y = letter_y + align_y
        idx_j -= 1
        
    return (score, align_x, align_y)


def compute_local_alignment(seq_x, seq_y, scoring_matrix, alignment_matrix):
    """
    input:
        two sequences seq_x and seq_y whose elements share a common alphabet with
        the scoring matrix scoring_matrix. This function computes a local alignment of
        seq_x and seq_y using the local alignment matrix alignment_matrix.
    output:
        a tuple of the form (score, align_x, align_y) where score is the score of the
        optimal local alignment align_x and align_y. Note that align_x and align_y
        should have the same length and may include the padding character '-'
    """
    
    ## check if input sequences share common alphabet with the scoring matrix
    alphabet = set(scoring_matrix.keys())
    #print "alphbet type:", type(alphabet)
    for letter in seq_x:
        if letter not in alphabet:
            return "Error: input sequences do not share common alphabet with the scoring matrix"
    for letter in seq_y:
        if letter not in alphabet:
            return "Error: input sequences do not share common alphabet with the scoring matrix"
    
    align_x = ""
    align_y = ""
    
    ## finding the maximum score in the LOCAL alignment matrix
    max_score = -1
    for index_i in range(0, len(seq_x) + 1):
        for index_j in range(0, len(seq_y) + 1):
            if alignment_matrix[index_i][index_j] > max_score:
                max_score = alignment_matrix[index_i][index_j]
                idx_i = index_i
                idx_j = index_j
    
    while idx_i != 0 and idx_j != 0 and alignment_matrix[idx_i][idx_j] != 0:
        letter_x = seq_x[idx_i - 1]
        letter_y = seq_y[idx_j - 1]
        if alignment_matrix[idx_i][idx_j] == alignment_matrix[idx_i - 1][idx_j - 1] + scoring_matrix[letter_x][letter_y]:
            align_x = letter_x + align_x
            align_y = letter_y + align_y
            idx_i -= 1
            idx_j -= 1
        else:
            if alignment_matrix[idx_i][idx_j] == alignment_matrix[idx_i - 1][idx_j] + scoring_matrix[letter_x]['-']:
                align_x = letter_x + align_x
                align_y = '-' + align_y
                idx_i -= 1
            else:
                align_x = '-' + align_x
                align_y = letter_y + align_y
                idx_j -= 1

    return (max_score, align_x, align_y)
    

#########################################################################################
## testing
#alphabet = set(['A', 'T', 'C', 'G'])
#
#test_M = build_scoring_matrix(alphabet, 10, 2, -4)
#print "scoring_matrix: ", test_M
#
#sequence_x = 'ACC'
#sequence_y = 'TTTACACGG'
#
#test_global_S = compute_alignment_matrix(sequence_x, sequence_y, test_M, True)
#test_local_S = compute_alignment_matrix(sequence_x, sequence_y, test_M, False)
#
#print "global_S: ", test_global_S
#print "local_S: ", test_local_S
#
#test_global_align = compute_global_alignment(sequence_x, sequence_y, test_M, test_global_S)
#print "test_global_alignment: ", test_global_align
#
#test_local_align = compute_local_alignment(sequence_x, sequence_y, test_M, test_local_S)
#print "test_local_alignment: ", test_local_align