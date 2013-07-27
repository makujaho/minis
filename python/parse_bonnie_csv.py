#!/usr/bin/env python
'''
This is a quick parser that takes all lines in 'bonnie.csv' and adds the values together

Useful when testing file systems in cluster environments with multiple nodes
'''

import csv

seq_output_blk  = 0
seq_output_rwrt = 0
seq_input_blk   = 0
ran_seeks       = 0
seq_create_r    = 0
seq_create_w    = 0
seq_create_d    = 0
ran_create_r    = 0
ran_create_w    = 0
ran_create_d    = 0

with open('bonnie.csv', 'rb') as csvfile:
    r = csv.reader(csvfile)
    for row in r:
        seq_output_blk  += float(row[9])
        seq_output_rwrt += float(row[11])
        seq_input_blk   += float(row[15])
        ran_seeks       += float(row[17])
        seq_create_r    += float(row[24])
        seq_create_w    += float(row[26])
        seq_create_d    += float(row[28])
        ran_create_r    += float(row[30])
        ran_create_w    += float(row[32])
        ran_create_d    += float(row[34])

print "Sequential - in 1000 elements per second"
print "seq output block:   " +  str(seq_output_blk)
print "seq output rewrite: " +  str(seq_output_rwrt)
print "seq input block:    " +  str(seq_input_blk)

print ""
print "Random seeks per second"
print "ran_seeks:          " +  str(ran_seeks)

print ""
print "Sequential create in elements per second"
print "seq create read:    " +  str(seq_create_r)
print "seq create write:   " +  str(seq_create_w)
print "seq create delete:  " +  str(seq_create_d)

print ""
print "Random create in elements per second"
print "ran create read:    " +  str(ran_create_r)
print "ran create write:   " +  str(ran_create_w)
print "ran create delete:  " +  str(ran_create_d)
