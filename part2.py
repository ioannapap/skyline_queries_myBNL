import csv

allStats='2017_ALL.csv'
assistStats='2017_AST.csv'
pointStats='2017_PTS.csv'
stealStats='2017.STL.csv'
blockStats='2017_BLK.csv'
reboundStats='2017_TRB.csv'

def getINput():

	args=[]
	checked=0

	print('--------------------------NBA STATS 2017--------------------------')
	print('-------------------------SKYLINE PLAYERS--------------------------')
	print('------------------------------------------------------------------')
	print('Choose which of the following statCategories you are interested in: ')
	print('1. Rebounds 	  2. Assists 	 3. Steals  	4. Blocks 	  5. Points')

	while checked==0:
		args=input('Give the numbers with comma in [ ]:\n')
		checked=checkArgs(args)

	return args

def checkArgs(args):

	chosenCategories=[]
	#checking chosenCategories
	for i in args:
	
		if i.isdigit(): 
				
			if int(i)>=1 and int(i)<=5:
				chosenCategories.insert(len(chosenCategories), int(i))
			else:
				print('insert number from 1-5.\n')
				return 0 

		elif i=='[' or i==']' or i==',':
			pass
		elif i=='-':
			print('Insert number from 1-5.\n')
			return 0 

		else:
			print('Insert number from 1-5.\n')
			return 0 

	return 1








if __name__ == "__main__":

	chosenCategories=[]
	getINput()