import rhinoscriptsyntax as rs

import sys
my_path = 'C:/Users/ukeer/timber_grammar'
sys.path.append(my_path)

import beam
b = beam.Beam()
print (b.length)
#rs.MessageBox (b.a)
