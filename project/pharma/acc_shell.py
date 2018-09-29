
import acc

SCALE_FILE = 'hellberg.zsc'

hellberg = acc.Hellberg(open(SCALE_FILE).read().strip())

#Examples from the book: Introduction to pharmaceutical bioinformatics, Wikberg
sequence = 'VFWLFIY'
print(sequence, hellberg.ac(sequence), sep = ' : ' )

sequence = 'ACDEFGI'
print(sequence, hellberg.ac(sequence), sep = ' : ' )

#Assignment Pharmaceutical bioinformatics, Fall 2018
sequence = 'ACDEFHI'
print(sequence, hellberg.ac(sequence), sep = ' : ' )

sequence = 'VFWLYFI'
print(sequence, hellberg.ac(sequence), sep = ' : ' )