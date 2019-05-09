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



def makeHashMaps(cat, k):

	hashMap={} #ids and names only
	hashMap1={}
	hashMap2={}
	hashMap3={}
	hashMap4={}
	hashMap5={}


	with open(allStats, 'r', encoding='UTF-8') as df:
		
		row=df.readline() #to skip labels

		for row in df:						
			data=row.split(',') 
			data[-1] = data[-1].strip() #remove \n
			hashMap.update({int(data[0]): [data[1], data[2], data[3], data[4], data[5], data[6], data[7]]})

	optionFiles={0: allStats, 1: reboundStats, 2: assistStats, 3: stealStats, 4: blockStats, 5: pointStats}
	numOfChoices=len(cat)

	if numOfChoices<5:
		leftovers=5-numOfChoices
		for i in range(leftovers):
			cat.append(0)

	
	with open(optionFiles[cat[0]], 'r', encoding='UTF-8') as df1, open(optionFiles[cat[1]], 'r', encoding='UTF-8') as df2, open(optionFiles[cat[2]], 'r',encoding='UTF-8') as df3, open(optionFiles[cat[3]], 'r', encoding='UTF-8') as df4, open(optionFiles[cat[4]], 'r', encoding='UTF-8') as df5:
		
		if numOfChoices==1: #cat[0] 

			firstRow=1
			for row in df1:
				data1=row.split(',')
				#the top ks are the first k 
				topKPlayer=hashMap.get(int(data1[0]))
				yield [str(topKPlayer[0]), int(topKPlayer[cat[0]+1])]


		elif numOfChoices==2: #cat[0] cat[1]

			firstRow=1
			for row in zip(df1,df2):
				data1=row.split(',')
				data2=row.split(',')
				if firstRow==1:
					maxv1=data1[1]
					maxv2=data2[1]
					firstRow=0
				performance1=normalization(int(data1[1]), maxv1)
				performance2=normalization(int(data2[1]), maxv2) 
				hashMap1.update({int(data1[0]): performance1})
				hashMap2.update({int(data2[0]): performance2})	

		
		elif numOfChoices==3: #cat[0] cat[1] cat[2]

			firstRow=1
			for row in zip(df1,df2,df3):
				data1=row.split(',')
				data2=row.split(',')
				data3=row.split(',') 
				if firstRow==1:
					maxv1=data1[1]
					maxv2=data2[1]
					maxv3=data3[1]
					firstRow=0
				performance1=normalization(int(data1[1]), maxv1)
				performance2=normalization(int(data2[1]), maxv2) 
				performance3=normalization(int(data3[1]), maxv3)
				hashMap1.update({int(data1[0]): performance1})
				hashMap2.update({int(data2[0]): performance2})
				hashMap3.update({int(data3[0]): performance3})


		elif numOfChoices==4: #cat[0] cat[1] cat[2] cat[3]

			firstRow=1
			for row in zip(df1,df2,df3,df4):
				data1=row.split(',')
				data2=row.split(',')
				data3=row.split(',') 
				data4=row.split(',')
				if firstRow==1:
					maxv1=data1[1]
					maxv2=data2[1]
					maxv3=data3[1]
					maxv4=data4[1]
					firstRow=0
				performance1=normalization(int(data1[1]), maxv1)
				performance2=normalization(int(data2[1]), maxv2) 
				performance3=normalization(int(data3[1]), maxv3)	
				performance4=normalization(int(data4[1]), maxv4)
				hashMap1.update({int(data1[0]): performance1})
				hashMap2.update({int(data2[0]): performance2})
				hashMap3.update({int(data3[0]): performance3})				
				hashMap4.update({int(data4[0]): performance4})


		elif numOfChoices==5: #cat[0] cat[1] cat[2] cat[3] cat[4]

			firstRow=1
			for row in zip(df1,df2,df3,df4,df5):
				data1=row.split(',')
				data2=row.split(',')
				data3=row.split(',') 
				data4=row.split(',')
				data5=row.split(',')
				if firstRow==1:
					maxv1=data1[1]
					maxv2=data2[1]
					maxv3=data3[1]
					maxv4=data4[1]
					maxv5=data5[1]
					firstRow=0
				performance1=normalization(int(data1[1]), maxv1)
				performance2=normalization(int(data2[1]), maxv2) 
				performance3=normalization(int(data3[1]), maxv3)	
				performance4=normalization(int(data4[1]), maxv4)
				performance5=normalization(int(data5[1]), maxv5)
				hashMap1.update({int(data1[0]): performance1})
				hashMap2.update({int(data2[0]): performance2})
				hashMap3.update({int(data3[0]): performance3})				
				hashMap4.update({int(data4[0]): performance4})
				hashMap5.update({int(data5[0]): performance5})
	
		'''
		with open(results, 'w', encoding='UTF-8') as record:

		csv_writer = csv.writer(record, delimiter=',')	
		csv_writer.writerow(['titleId', 'primaryTitle','title','regions'])
		
		'''

def normalization(rowValue, maxv):
	return rowValue/maxv


if __name__ == "__main__":
	
	inputs=getINput()
	chosenCategories=inputs[0]
	k=inputs[1]
	print('k', k)
	counter=0
	with open('topks.csv', 'w', encoding='UTF-8') as rp1: 
		csv_writer = csv.writer(rp1, delimiter=',')
		for topks in makeHashMaps(chosenCategories, k):
			if counter<k:
				csv_writer.writerow(topks)
				print(topks)
				counter+=1
			else:
				break
	 
