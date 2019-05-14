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


def myBNL(cat):

	optionFiles={0: allStats, 1: reboundStats, 2: assistStats, 3: stealStats, 4: blockStats, 5: pointStats}
	numOfChoices=len(cat)
	if numOfChoices<5:
		leftovers=5-numOfChoices
		for i in range(leftovers):
			cat.append(0)

	slHashMap={}
	firstTime=1

	with open(allStats, 'r',encoding='UTF-8') as df:

		row=df.readline()
		
		for row in df:		

			data=row.split(',') 
			data[-1] = data[-1].strip() #remove 
			iD=data[0]

			if numOfChoices==1:   #cat[0]

				if firstTime==1:
					slHashMap.update(iD: data[cat[0]])
					firstTime=0

		
			elif numOfChoices==2:  #cat[0] cat[1]

				if firstTime==1:
					slHashMap.update(iD: data[cat[0]], data[cat[1]])
					firstTime=0

			elif numOfChoices==3:  #cat[0] cat[1] cat[2]

				if firstTime==1:
					slHashMap.update(iD: data[cat[0]], data[cat[1]], data[cat[2]])
					firstTime=0

			elif numOfChoices==4:  #cat[0] cat[1] cat[2] cat[3]

				if firstTime==1:
					slHashMap.update(iD: data[cat[0]], data[cat[1]], data[cat[2]], data[cat[3]])
					firstTime=0

			elif numOfChoices==5:  #cat[0] cat[1] cat[2] cat[3] cat[4]

				if firstTime==1:
					slHashMap.update(iD: data[cat[0]], data[cat[1]], data[cat[2]], data[cat[3]], data[cat[4]])
					firstTime=0


		

		




if __name__ == '__main__':

	chosenCategories=getINput()
	skyline=myBNL(chosenCategories)
	print(chosenCategories)
	with open('skyline.csv', 'w', encoding='UTF-8') as rp2:

		csv_writer = csv.writer(rp2, delimiter=',')
		print('skyline: ', skyline)
		csv_writer.writerow(skyline)






