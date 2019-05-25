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
			data[-1] = data[-1].strip()
			iD=data[0] 
			delList=[]
			needToInsert=0
			pl=0

			if numOfChoices==1:   

				if firstTime==1:
					slHashMap.update({iD : [data[1], int(data[cat[0]+2])]}) #+2 due to name and tm column
					firstTime=0

				for idd in slHashMap:
					val1=slHashMap.get(idd)
					val1=val1[1] 

					if int(data[cat[0]+2])>val1:	
						delList.insert(len(delList), idd)
						needToInsert=1
						
				for idss in delList:
					del slHashMap[idss]
					
				if needToInsert==1:
					slHashMap.update({iD : [data[1], int(data[cat[0]+2])]})
					needToInsert=0



			elif numOfChoices==2:  

				if firstTime==1:
					slHashMap.update({iD : [data[1], int(data[cat[0]+2]), int(data[cat[1]+2])]}) 
					firstTime=0

				for idd in slHashMap:
					val1=slHashMap.get(idd)
					val2=slHashMap.get(idd)
					val1=val1[1] 
					val2=val2[2]

					if (int(data[cat[0]+2])>val1 and int(data[cat[1]+2])>=val2) or (int(data[cat[1]+2])>val2 and int(data[cat[0]+2])>=val1):
						delList.insert(len(delList), idd)
						needToInsert=1
					elif int(data[cat[0]+2])>val1 or int(data[cat[1]+2])>val2 :
						pl+=1
				
					
				for idss in delList:
					del slHashMap[idss]

				if len(slHashMap)==pl:
					needToInsert=1
					
				if needToInsert==1:
					slHashMap.update({iD : [data[1], int(data[cat[0]+2]), int(data[cat[1]+2])]})
					needToInsert=0



			elif numOfChoices==3: 

				if firstTime==1:
					slHashMap.update({iD : [data[1], int(data[cat[0]+2]), int(data[cat[1]+2]), int(data[cat[2]+2])]}) 
					firstTime=0

				for idd in slHashMap:
					val1=slHashMap.get(idd)
					val2=slHashMap.get(idd)
					val3=slHashMap.get(idd)
					val1=val1[1] 
					val2=val2[2]
					val3=val3[3]

					if (int(data[cat[0]+2])>val1 and int(data[cat[1]+2])>=val2 and int(data[cat[2]+2])>=val3) or (int(data[cat[1]+2])>val2 and int(data[cat[0]+2])>=val1 and int(data[cat[2]+2])>=val3) or (int(data[cat[2]+2])>val3 and int(data[cat[0]+2])>=val1 and int(data[cat[1]+2])>=val2):
						delList.insert(len(delList), idd)
						needToInsert=1
					elif int(data[cat[0]+2])>val1 or int(data[cat[1]+2])>val2 or int(data[cat[2]+2])>val3:
						pl+=1
				
				
				for idss in delList:
					del slHashMap[idss]
				
				if len(slHashMap)==pl:
					needToInsert=1

				if needToInsert==1:
					slHashMap.update({iD : [data[1], int(data[cat[0]+2]), int(data[cat[1]+2]), int(data[cat[2]+2])]})
					needToInsert=0
				


		
			elif numOfChoices==4: 

				if firstTime==1:
					slHashMap.update({iD : [data[1], int(data[cat[0]+2]), int(data[cat[1]+2]), int(data[cat[2]+2]), int(data[cat[3]+2])]}) 
					firstTime=0

				for idd in slHashMap:
					val1=slHashMap.get(idd)
					val2=slHashMap.get(idd)
					val3=slHashMap.get(idd)
					val4=slHashMap.get(idd)
					val1=val1[1] 
					val2=val2[2]
					val3=val3[3]
					val4=val4[4]

					if (int(data[cat[0]+2])>val1 and int(data[cat[1]+2])>=val2 and int(data[cat[2]+2])>=val3 and int(data[cat[3]+2])>=val4) or (int(data[cat[1]+2])>val2 and int(data[cat[0]+2])>=val1 and int(data[cat[2]+2])>=val3 and int(data[cat[3]+2])>=val4) or (int(data[cat[2]+2])>val3 and int(data[cat[0]+2])>=val1 and int(data[cat[1]+2])>=val2 and int(data[cat[3]+2])>=val4) or (int(data[cat[3]+2])>val4 and int(data[cat[0]+2])>=val1 and int(data[cat[1]+2])>=val2 and int(data[cat[2]+2])>=val3):
						delList.insert(len(delList), idd)
						needToInsert=1
					elif int(data[cat[0]+2])>val1 or int(data[cat[1]+2])>val2 or int(data[cat[2]+2])>val3 or int(data[cat[3]+2])>val4:
						pl+=1
				
				
				
				for idss in delList:
					del slHashMap[idss]

				if len(slHashMap)==pl:
					needToInsert=1

				if needToInsert==1:
					slHashMap.update({iD : [data[1], int(data[cat[0]+2]), int(data[cat[1]+2]), int(data[cat[2]+2]), int(data[cat[3]+2])]})
					needToInsert=0
		

	

			elif numOfChoices==5: 

				if firstTime==1:
					slHashMap.update({iD : [data[1], int(data[cat[0]+2]), int(data[cat[1]+2]), int(data[cat[2]+2]), int(data[cat[3]+2]), int(data[cat[4]+2])]}) 
					firstTime=0

				for idd in slHashMap:
					val1=slHashMap.get(idd)
					val2=slHashMap.get(idd)
					val3=slHashMap.get(idd)
					val4=slHashMap.get(idd)
					val5=slHashMap.get(idd)
					val1=val1[1] 
					val2=val2[2]
					val3=val3[3]
					val4=val4[4]
					val5=val5[5]

					if (int(data[cat[0]+2])>val1 and int(data[cat[1]+2])>=val2 and int(data[cat[2]+2])>=val3 and int(data[cat[3]+2])>=val4 and int(data[cat[4]+2])>=val5) or (int(data[cat[1]+2])>val2 and int(data[cat[0]+2])>=val1 and int(data[cat[2]+2])>=val3 and int(data[cat[3]+2])>=val4 and int(data[cat[4]+2])>=val5) or (int(data[cat[2]+2])>val3 and int(data[cat[0]+2])>=val1 and int(data[cat[1]+2])>=val2 and int(data[cat[3]+2])>=val4 and int(data[cat[4]+2])>=val5) or (int(data[cat[3]+2])>val4 and int(data[cat[0]+2])>=val1 and int(data[cat[1]+2])>=val2 and int(data[cat[2]+2])>=val3 and int(data[cat[4]+2])>=val5) or (int(data[cat[4]+2])>val5 and int(data[cat[0]+2])>=val1 and int(data[cat[1]+2])>=val2 and int(data[cat[2]+2])>=val3 and int(data[cat[3]+2])>=val4):
						delList.insert(len(delList), idd)
						needToInsert=1
					elif int(data[cat[0]+2])>val1 or int(data[cat[1]+2])>val2 or int(data[cat[2]+2])>val3 or int(data[cat[3]+2])>val4 or int(data[cat[4]+2])>val5:
						pl+=1
				

				for idss in delList:
					del slHashMap[idss]
			
				if len(slHashMap)==pl:
					needToInsert=1		
								
				if needToInsert==1:
					slHashMap.update({iD : [data[1], int(data[cat[0]+2]), int(data[cat[1]+2]), int(data[cat[2]+2]), int(data[cat[3]+2]), int(data[cat[4]+2])]})
					needToInsert=0
					

		sk=list(slHashMap.values())
		return sk


if __name__ == '__main__':

	chosenCategories=getINput()
	skyline=myBNL(chosenCategories)

	with open('skyline.csv', 'w', encoding='UTF-8') as rp2:	
		csv_writer = csv.writer(rp2, delimiter=',')
		for s in skyline:
			csv_writer.writerow(s)