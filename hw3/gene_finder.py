# -*- coding: utf-8 -*-
"""
Created on Sun Feb  2 11:24:42 2014

@author: Austin Greene
"""


# you may find it useful to import these variables (although you are not required to use them)
from amino_acids import aa, codons
from load import load_seq
import random

def collapse(L):
    """ Converts a list of strings to a string by concatenating all elements of the list """
    output = ""
    for s in L:
        output = output + s
    return output

def codonGen(dna, start = 0):
    #Generator for creating the required codon for iterating through genes
    for i in xrange(start,len(dna),3):
        yield dna[i:i+3]

def coding_strand_to_AA(dna):
    """ Computes the Protein encoded by a sequence of DNA.  This function
    does not check for start and stop codons (it assumes that the input
    DNA sequence represents an protein coding region).
        
    dna: a DNA sequence represented as a strings        
    returns: a string containing the sequence of amino acids encoded by the
    the input DNA fragment"""

    i = 0
    c = 0
    aminoAcidSequence = ""
    currentCodons = codonGen(dna)
    for currentCodon in currentCodons:
        if len(currentCodon) < 3:
            break
        while currentCodon not in codons[c]:
            c = c+1

        aminoAcidSequence = aminoAcidSequence + aa[c]
        c = 0
        i+=3

    return aminoAcidSequence

def coding_strand_to_AA_unit_tests():
    """ Unit tests for the coding_strand_to_AA function """
        
    print coding_strand_to_AA("ATGGGGCCCTTT")
    'MGPF'
    print coding_strand_to_AA("ATGCCCGCTATAATTT")
    'MPAII'

def get_reverse_complement(dna):
    """ Computes the reverse complementary sequence of DNA for the specfied DNA
        sequence
    
        dna: a DNA sequence represented as a string
        returns: the reverse complementary DNA sequence represented as a string
    """
    i = 0
    complimentDna = ""
    for i in range(len(dna)):
        if(dna[i] == 'A'):
            complementaryBase = 'T'
        elif(dna[i] == 'T'):
            complementaryBase = 'A'
        elif(dna[i] == 'C'):
            complementaryBase = 'G'
        elif(dna[i] == 'G'):
            complementaryBase = 'C'

        complimentDna = complimentDna + complementaryBase 

    return complimentDna[::-1]
    
def get_reverse_complement_unit_tests():
    """ Unit tests for the get_complement function """
        
    print get_reverse_complement("ATGCCCGCTTTAAA")
    'TTTAAAGCGGGCAT'    

def rest_of_ORF(dna):
    """ Takes a DNA sequence that is assumed to begin with a start codon and returns
        the sequence up to but not including the first in frame stop codon.  If there
        is no in frame stop codon, returns the whole string.
        
        dna: a DNA sequence
        returns: the open reading frame represented as a string
    """
    i = 0
    stopCodons = ['TAG','TAA','TGA']
    codons = codonGen(dna)
    finalCode = ''
    for currentCodon in codons:
        if currentCodon not in stopCodons:
            finalCode+=currentCodon 
        else:
           break
    return finalCode


def rest_of_ORF_unit_tests():
    """ Unit tests for the rest_of_ORF function """
    print rest_of_ORF("ATGTTTCCCTGAA")
    'ATGTTTCCC'
        
def find_all_ORFs_oneframe(dna, start = 0):
    """ Finds all non-nested open reading frames in the given DNA sequence and returns
        them as a list.  This function should only find ORFs that are in the default
        frame of the sequence (i.e. they start on indices that are multiples of 3).
        By non-nested we mean that if an ORF occurs entirely within
        another ORF, it should not be included in the returned list of ORFs.
        
        dna: a DNA sequence
        returns: a list of non-nested ORFs
    """
    i = 0
    startCodons = ['ATG']
    stopCodons = ['TAG','TAA','TGA']
    currentGene = ""
    codons = codonGen(dna,start)
    genesInORF = []
    inGene = False

    for currentCodon in codons:
        if(currentCodon in startCodons):
            inGene = True
        elif(currentCodon in stopCodons):
            inGene = False
            if(currentGene != ""):
                genesInORF.append(currentGene)
            currentGene = ""
        if(inGene):
            currentGene+=currentCodon

    if(currentGene != ""):
        genesInORF.append(currentGene)
    return genesInORF

def find_all_ORFs_oneframe_unit_tests():
    """ Unit tests for the find_all_ORFs_oneframe function """

    print find_all_ORFs_oneframe("ATGCATGAATGTCCCAGATAGCCCATGCCCTGCCC")
    ['ATGCATGAATGTCCCAGA', 'ATGCCCTGCCC']

def find_all_ORFs(dna):
    """ Finds all non-nested open reading frames in the given DNA sequence in all 3
        possible frames and returns them as a list.  By non-nested we mean that if an
        ORF occurs entirely within another ORF and they are both in the same frame,
        it should not be included in the returned list of ORFs.
        
        dna: a DNA sequence
        returns: a list of non-nested ORFs
    """
     
    inORF1 = find_all_ORFs_oneframe(dna)
    inORF2 = find_all_ORFs_oneframe(dna,1)
    inORF3 = find_all_ORFs_oneframe(dna,2)

    allGenes = inORF1 + inORF2 + inORF3

    return allGenes
def find_all_ORFs_unit_tests():
    """ Unit tests for the find_all_ORFs function """
        
    print find_all_ORFs("ATGCCCCATGCCCAATGCCCTAG")
    ['ATGCCCCATGAATGTAG', 'ATGCCCAATGTAG', 'ATGCCC']
def find_all_ORFs_both_strands(dna):
    """ Finds all non-nested open reading frames in the given DNA sequence on both
        strands.
        
        dna: a DNA sequence
        returns: a list of non-nested ORFs
    """
     
    complementaryDna = get_reverse_complement(dna)

    frealAllGenes = find_all_ORFs(dna) + find_all_ORFs(complementaryDna)

    return frealAllGenes

def find_all_ORFs_both_strands_unit_tests():
    """ Unit tests for the find_all_ORFs_both_strands function """

    print find_all_ORFs_both_strands("ATGCCCCGAATGCCCTAGCATCAAA")
    ['ATGCCCCGAATG', 'ATGCCCCTACATTCGCAT']

def longest_ORF(dna):
    """ Finds the longest ORF on both strands of the specified DNA and returns it
        as a string"""

    longestORF = ""
    ORFs = find_all_ORFs_both_strands(dna)
    for currentORF in ORFs:
        if len(currentORF) > len(longestORF):
            longestORF = currentORF

    return longestORF

def longest_ORF_unit_tests():
    """ Unit tests for the longest_ORF function """

    print longest_ORF("ATGCCCCGAATGTAGCATCAAA")
    'ATGCCCCTACATTCGCAT'

def longest_ORF_noncoding(dna, num_trials):
    """ Computes the maximum length of the longest ORF over num_trials shuffles
        of the specfied DNA sequence
        
        dna: a DNA sequence
        num_trials: the number of random shuffles
        returns: the maximum length longest ORF """

    trials = 0
    maximumRandomORF = 0
    while(trials < num_trials):
        dnaList = list(dna)
        random.shuffle(dnaList)
        shuffledDna = collapse(dnaList)
        currentLongestORF = longest_ORF(shuffledDna)
        if  len(currentLongestORF) > maximumRandomORF:
            maximumRandomORF = len (currentLongestORF)
        trials+=1

    print  maximumRandomORF
    return maximumRandomORF
def gene_finder(dna, threshold):
    """ Returns the amino acid sequences coded by all genes that have an ORF
        larger than the specified threshold.
        
        dna: a DNA sequence
        threshold: the minimum length of the ORF for it to be considered a valid
                   gene.
        returns: a list of all amino acid sequences whose ORFs meet the minimum
                 length specified.
    """
    AminoAcidSequences = []
    ORFs = find_all_ORFs_both_strands(dna)
    for currentORF in ORFs:
        if len(currentORF)>threshold:
            aminoAcidSequence = coding_strand_to_AA(currentORF)
            AminoAcidSequences.append(aminoAcidSequence)
    return AminoAcidSequences


# coding_strand_to_AA_unit_tests()
# get_reverse_complement_unit_tests()
# rest_of_ORF_unit_tests()
# find_all_ORFs_oneframe_unit_tests()
# find_all_ORFs_unit_tests()
# find_all_ORFs_both_strands_unit_tests()
# longest_ORF_unit_tests()
# dna = load_seq("./data/X73525.fa")
# #longest_ORF_noncoding(dna, 10)
# print gene_finder(dna, 450)