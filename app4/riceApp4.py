'''
Algorithmic Thinking Application 4:
Applications to genomics and beyond
'''

DESKTOP = True

import math
import random
import urllib2

if DESKTOP:
    import matplotlib.pyplot as plt
    import alg_project4_solution as student
else:
    import simpleplot
    import userXX_XXXXXXX as student
    

# URLs for data files
PAM50_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_PAM50.txt"
HUMAN_EYELESS_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_HumanEyelessProtein.txt"
FRUITFLY_EYELESS_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_FruitflyEyelessProtein.txt"
CONSENSUS_PAX_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_ConsensusPAXDomain.txt"
WORD_LIST_URL = "http://storage.googleapis.com/codeskulptor-assets/assets_scrabble_words3.txt"



###############################################
# provided code

def read_scoring_matrix(filename):
    """
    Read a scoring matrix from the file named filename.  

    Argument:
    filename -- name of file containing a scoring matrix

    Returns:
    A dictionary of dictionaries mapping X and Y characters to scores
    """
    scoring_dict = {}
    scoring_file = urllib2.urlopen(filename)
    ykeys = scoring_file.readline()
    ykeychars = ykeys.split()
    for line in scoring_file.readlines():
        vals = line.split()
        xkey = vals.pop(0)
        scoring_dict[xkey] = {}
        for ykey, val in zip(ykeychars, vals):
            scoring_dict[xkey][ykey] = int(val)
    return scoring_dict



def read_protein(filename):
    """
    Read a protein sequence from the file named filename.

    Arguments:
    filename -- name of file containing a protein sequence

    Returns:
    A string representing the protein
    """
    protein_file = urllib2.urlopen(filename)
    protein_seq = protein_file.read()
    protein_seq = protein_seq.rstrip()
    return protein_seq


def read_words(filename):
    """
    Load word list from the file named filename.

    Returns a list of strings.
    """
    # load assets
    word_file = urllib2.urlopen(filename)
    
    # read in files as string
    words = word_file.read()
    
    # template lines and solution lines list of line string
    word_list = words.split('\n')
    print "Loaded a dictionary with", len(word_list), "words"
    return word_list


def string_match_percent(seq_x, seq_y):
    """
    input: seq_x and seq_y must have the same length
    output: the percentage of characters that agree
    """
    
    length = len(seq_x)
    agree = 0
    for i in range(0, length):
        if seq_x[i] == seq_y[i]:
            agree += 1
    
    return float(agree)/length


def generate_null_distribution(seq_x, seq_y, scoring_matrix, num_trials):
    """
    input:
        two sequences, scoring matrix, number of trials.
        A trial is defined as:
        1. Generate a random permutation rand_y of the sequence seq_y using random.shuffle().
        2. Compute the maximum value score for the local alignment of seq_x and rand_y using the score matrix scoring_matrix.
        3. Increment the entry score in the dictionary scoring_distribution by one.
    output:
        a dictionary scoring_distribution that represents an un-normalized distribution
    """
    
    scoring_distribution = {}
    for i in range(num_trials):
        rand_y = random.sample(seq_y, len(seq_y))
        local_S = student.compute_alignment_matrix(seq_x, rand_y, scoring_matrix, False)
        local_alignment = student.compute_local_alignment(seq_x, rand_y, scoring_matrix, local_S)
        if local_alignment[0] in scoring_distribution:
            scoring_distribution[local_alignment[0]] += 1
        else:
            scoring_distribution[local_alignment[0]] = 1
    
    return scoring_distribution

def normalize(distribution):
    """
    normalize a distribution (a dict)
    """
    
    values = distribution.values()
    total = sum(values)
    new_values = [float(x)/total for x in values]
    new_dist = dict(zip(distribution.keys(), new_values))
    return new_dist

def check_spelling(checked_word, dist, word_list):
    """
    input:
        iterates through word_list and returns the set of all words
        that are within edit distance dist of the string checked_word
    output:
        the set of all words that are within edit distance dist of
        the string checked_word
    """
    
    result_set = set([])
    diag_score = 2
    off_diag_score = 1
    dash_score = 0
    alphabet = set('abcdefghijklmnopqrstuvwxyz')
    matrix_M = student.build_scoring_matrix(alphabet, diag_score, off_diag_score, dash_score)
    for word in word_list:
        matrix_S = student.compute_alignment_matrix(checked_word, word, matrix_M, True)
        global_align_word = student.compute_global_alignment(checked_word, word, matrix_M, matrix_S)
        if len(checked_word) + len(word) - global_align_word[0] <= dist:
            result_set.add(word)
    
    return result_set



#PAM50 = read_scoring_matrix(PAM50_URL)
#HUMAN_EYELESS = read_protein(HUMAN_EYELESS_URL)
#FRUITFLY_EYELESS = read_protein(FRUITFLY_EYELESS_URL)
#CONSENSUS_PAX = read_protein(CONSENSUS_PAX_URL)
WORD_LIST = read_words(WORD_LIST_URL)

#word_set_humble = check_spelling('humble', 1, WORD_LIST)
#print "word_set_humble: ", word_set_humble

word_set_firefly = check_spelling('firefly', 2, WORD_LIST)
print "word_set_firefly: ", word_set_firefly

#LOCAL_S = student.compute_alignment_matrix(HUMAN_EYELESS, FRUITFLY_EYELESS, PAM50, False)
#LOCAL_ALIGN = student.compute_local_alignment(HUMAN_EYELESS, FRUITFLY_EYELESS, PAM50, LOCAL_S)
#print "Human-eyeless vs. Fruitfly-eyeless local alignment score: "
#print LOCAL_ALIGN[0]
#print "Human-eyeless local alignment: "
#print LOCAL_ALIGN[1]
#print "Fruitfly-eyeless local alignment: "
#print LOCAL_ALIGN[2]



## variables that need to be saved
#HUMAN_LOCAL = 'HSGVNQLGGVFVNGRPLPDSTRQKIVELAHSGARPCDISRILQVSNGCVSKILGRYYETGSIRPRAIGGSKPRVATPEVVSKIAQYKRECPSIFAWEIRDRLLSEGVCTNDNIPSVSSINRVLRNLASEKQQ'
#FRUITFLY_LOCAL = 'HSGVNQLGGVFVGGRPLPDSTRQKIVELAHSGARPCDISRILQVSNGCVSKILGRYYETGSIRPRAIGGSKPRVATAEVVSKISQYKRECPSIFAWEIRDRLLQENVCTNDNIPSVSSINRVLRNLAAQKEQQ'

#GLOBAL_HC_S = student.compute_alignment_matrix(HUMAN_LOCAL, CONSENSUS_PAX, PAM50, True)
#GLOBAL_HC_ALIGN = student.compute_global_alignment(HUMAN_LOCAL, CONSENSUS_PAX, PAM50, GLOBAL_HC_S)
#print "Human-local vs. Consensus global alignment score: "
#print GLOBAL_HC_ALIGN[0]
#print "Human-local global alignment: "
#print GLOBAL_HC_ALIGN[1]
#print "Consensus global alignment: "
#print GLOBAL_HC_ALIGN[2]
#print "Percentage agreed: "
#print string_match_percent(GLOBAL_HC_ALIGN[1], GLOBAL_HC_ALIGN[2]) * 100, "%"

#GLOBAL_FC_S = student.compute_alignment_matrix(FRUITFLY_LOCAL, CONSENSUS_PAX, PAM50, True)
#GLOBAL_FC_ALIGN = student.compute_global_alignment(FRUITFLY_LOCAL, CONSENSUS_PAX, PAM50, GLOBAL_FC_S)
#print "Fruitfly-local vs. Consensus global alignment score: "
#print GLOBAL_FC_ALIGN[0]
#print "Fruitfly-local global alignment: "
#print GLOBAL_FC_ALIGN[1]
#print "Consensus global alignment: "
#print GLOBAL_FC_ALIGN[2]
#print "length: ", len(GLOBAL_FC_ALIGN[2])
#print "Percentage agreed: "
#print string_match_percent(GLOBAL_FC_ALIGN[1], GLOBAL_FC_ALIGN[2]) * 100, "%"

#NULL_DISTRIBUTION = generate_null_distribution(HUMAN_EYELESS, FRUITFLY_EYELESS, PAM50, 1000)
#NORMALIZED_NULL = normalize(NULL_DISTRIBUTION)
#print "Normalized NULL_DISTRIBUTION:", NORMALIZED_NULL

#SAVED_NULL_DISTRIBUTION = {38: 0.003, 39: 0.003, 40: 0.003, 41: 0.013, 42: 0.024, 43: 0.018, 44: 0.034, 45: 0.049, 46: 0.062, 47: 0.066, 48: 0.067, 49: 0.073, 50: 0.075, 51: 0.06, 52: 0.058, 53: 0.054, 54: 0.042, 55: 0.039, 56: 0.041, 57: 0.031, 58: 0.022, 59: 0.031, 60: 0.012, 61: 0.021, 62: 0.023, 63: 0.018, 64: 0.01, 65: 0.009, 66: 0.003, 67: 0.005, 68: 0.007, 69: 0.001, 70: 0.002, 71: 0.003, 72: 0.002, 73: 0.002, 74: 0.001, 75: 0.001, 76: 0.001, 77: 0.002, 78: 0.002, 79: 0.001, 80: 0.002, 81: 0.001, 82: 0.002, 86: 0.001}

#plt.bar(range(len(SAVED_NULL_DISTRIBUTION)), SAVED_NULL_DISTRIBUTION.values(), align='center')
#plt.xticks(range(len(SAVED_NULL_DISTRIBUTION)), SAVED_NULL_DISTRIBUTION.keys())
#plt.xlabel('local alignment score')
#plt.ylabel('probability')
#plt.title('NULL DISTRIBUTION GENERATED WITH 1000 TRIALS')
#
#plt.show()

#n = len(SAVED_NULL_DISTRIBUTION)
#mean_dist = float(sum(SAVED_NULL_DISTRIBUTION.keys()))/n
#sd_dist = math.sqrt(float(sum([(s - mean_dist)**2 for s in SAVED_NULL_DISTRIBUTION.keys()]))/n)
#
#print "mean =", mean_dist
#print "sd =", sd_dist
#
#z_score = (875 - mean_dist)/sd_dist
#print "z_score =", z_score



