import numpy as np
import random as rd
#Tree Class Def
class Node(object):
    def __init__(self, data):
        self.data = data
        self.children = []

    def add_child(self, obj):
        self.children.append(obj)
#funcition
def itsct_slash_update(itsct_temp,row,col):
	'Update itsct in slash and back slash way'
	row_temp = row
	col_temp = col
	while (col_temp!=dim-1 and row_temp!=dim-1):
		col_temp += 1
		row_temp += 1
		itsct_temp[row_temp,col_temp] = 1
	row_temp = row
	col_temp = col
	while (col_temp!=dim-1 and row_temp!=0):
		col_temp += 1
		row_temp -= 1
		itsct_temp[row_temp,col_temp] = 1
	return itsct_temp;

def itsct_update(itsct,row,col):
	'Update itsct'
	itsct_temp = np.array(itsct)
	itsct_temp[:,col] = 1
	itsct_temp[row,:] = 1
	itsct_temp = itsct_slash_update(itsct_temp,row,col)
	return itsct_temp;

def Candidate_Add(choices,itsct,col_index,dim,answer_found):
	#If it's deep enough, then the datas in the tree are a set of available resolution, turning answer_foun to True to stop searching.
	if col_index+1 == dim:
		answer_found = True
		print("Done")
	#Otherwise, keep searching to the deeper node.
	if col_index+1 < dim and not answer_found:
		itsct_temp = itsct_update(itsct,choices.data,col_index)    #Intersection table update
		row_cnddt = np.where(itsct_temp[:,col_index+1]==0)[0]    #Find available candidate choices
		if np.size(row_cnddt) != 0:    #If it's not a deadlock, try those candidates.
			#Calculate the number of blocking for choosing each candidate.
			row_cnddt_itsct = np.array([])
			for e in row_cnddt:
				itsct_cnddt_temp = itsct_update(itsct_temp,e,col_index+1)
				row_cnddt_itsct = np.append(row_cnddt_itsct,np.sum(itsct_cnddt_temp))
			row_cnddt_itsct = np.intc(row_cnddt_itsct)
			#Choose the candidate node in the increasing order of the number of blocking
			for e in row_cnddt[np.argsort(row_cnddt_itsct)]:
				#If the answer has been found, it will stop adding other children by breaking the for loop.
				if answer_found:
					break
				#Otherwise, it will keep trying another candidate node, after removing the previous fail node if exists.
				elif len(choices.children)!=0:
					choices.children.pop()
				choices.children.append(Node(e))
				answer_found = Candidate_Add(choices.children[-1],itsct_temp,col_index+1,dim,answer_found)
	return answer_found;

def PrintNode(Node,col):
	print("[",Node.data,",",col,"]")
	for e in Node.children:
		PrintNode(e,col+1)

#parameter setting & initialization
dim = 40
first_col_candidate = list(range(dim))
answer_found = False

#main
#If the answer is not found, it will randomly choose another block in the first column.
while not answer_found and len(first_col_candidate)!=0 :
	itsct = np.zeros((dim,dim))    #Initialization of intersection table
	choices = Node(rd.choice(first_col_candidate))  #Randomly choose a block in the first column
	col_index = 0
	#itsct_update(itsct,choices.data,col_index)
	answer_found = Candidate_Add(choices,itsct,col_index,dim,answer_found)
	if not answer_found:
		first_col_candidate.remove(choices.data)

PrintNode(choices,0)











