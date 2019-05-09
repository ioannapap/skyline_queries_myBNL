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
	print('------------------------------TOK K PLAYERS ------------------------------\n')
	print('Choose which of the following statCategories you are interested in: ')
	print('1. Rebounds 	  2. Assists 	 3. Steals  	4. Blocks 	  5. Points')

	while checked==0 or len(args)!=2:
		args=input('\nGive the numbers with comma in [ ] and then, the number of the Top-k players you are looking for:\n').split(' ')
		checked=checkArgs(args, chosenCategories)

	k=int(args[1])
	return [chosenCategories, k]



def checkArgs(args, cat):

	#checking chosenCategories

	if args[0][0]!='[' or args[0][len(args[0])-1]!=']':
		print('\nInsert the chosen categories in [ ]\n')
		return 0

	for i in args[0]:

		if i.isdigit(): 
				
			if int(i)>=1 and int(i)<=5:
				cat.insert(len(cat), int(i))
			else:
				print('\nInsert number from 1-5.\n')
				return 0 

		elif i=='[' or i==']' or i==',':
			pass
		elif i=='-':
			print('\nInsert number from 1-5.\n')
			return 0 

		else:
			print('\nInsert number from 1-5.\n')
			return 0 

	#checking k
	try:
		k=int(args[1])

	except ValueError:
		print('\nInsert integer for k.\n')
		return 0

	except IndexError:
		print('Insert integer for k.\n')
		return 0

	if k<=0 or k>595:
		print( '\nAll players are 595.\n')
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
		'''
		for row in df1:
			data1=row.split(',')
			hashMap1.append({ })

		if numOfChoices>=2:
			for row in df2:
				data2=row.split(',') 
				hashMap2.append({ })	


		if numOfChoices>=3:
			for row in df3:
				data3=row.split(',') 
				hashMap3.append({ })



		if numOfChoices>=4:
			for row in df4:
				data4=row.split(',') 
				hashMap4.append({ })

		if numOfChoices==5:
			for row in df5:
				data5=row.split(',') 
				hashMap5.append({ })
	
	
		with open(results, 'w', encoding='UTF-8') as record:

		tsv_writer = csv.writer(record, delimiter='\t')	
		tsv_writer.writerow(['titleId', 'primaryTitle','title','regions'])
		
		'''






if __name__ == "__main__":
	
	inputs=getINput()
	chosenCategories=inputs[0]
	k=inputs[1]
	makeHashMaps(chosenCategories)
	print(k)
