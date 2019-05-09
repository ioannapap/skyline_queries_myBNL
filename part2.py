import csv

allStats='2017_ALL.csv'
assistStats='2017_AST.csv'
pointStats='2017_PTS.csv'
stealStats='2017_STL.csv'
blockStats='2017_BLK.csv'
reboundStats='2017_TRB.csv'



def getINput():

	chosenCategories=[]
	args=[]
	checked=0

	print('------------------------------NBA STATS 2017------------------------------')
	print('-----------------------------SKYLINE PLAYERS------------------------------\n')
	print('Choose which of the following statCategories you are interested in: ')
	print('1. Rebounds 	  2. Assists 	 3. Steals  	4. Blocks 	  5. Points')

	while checked==0:
		args=input('\nGive the numbers with comma in [ ]:\n')
		checked=checkArgs(args, chosenCategories)

	return chosenCategories



def checkArgs(args, cat):

	#checking chosenCategories

	for i in args:

		if i.isdigit(): 
				
			if int(i)>=1 and int(i)<=5:
				cat.insert(len(cat), int(i))
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


def makeHashMaps(cat):

	optionFiles={0: allStats, 1: reboundStats, 2: assistStats, 3: stealStats, 4: blockStats, 5: pointStats}
	numOfChoices=len(cat)
	if numOfChoices<5:
		leftovers=5-numOfChoices
		for i in range(leftovers):
			cat.append(0)

		print(cat)
	
	with open(optionFiles[cat[0]], 'r',encoding='UTF-8') as df1, open(optionFiles[cat[1]], 'r',encoding='UTF-8') as df2, open(optionFiles[cat[2]], 'r',encoding='UTF-8') as df3, open(optionFiles[cat[3]], 'r',encoding='UTF-8') as df4, open(optionFiles[cat[4]], 'r',encoding='UTF-8') as df5:
		print('y')




if __name__ == "__main__":

	chosenCategories=getINput()