import pandas as pd
from Processing import DataProcessingFunctions

dataTable = pd.read_csv("/Users/brianwang/Desktop/DartmouthTrends/data/rawData.csv") # read in raw data file

dataTable.rename(columns={'TERM':'Term','ENRL':'Enrollment','MEDIAN':'Median', 'COURSE':'Course'}, inplace=True) # rename columns

DataProcessingFunctions.ReadCourses(dataTable) # Splitting Courses into Dept, Course #, Section #

DataProcessingFunctions.AssigningPoints(dataTable) # Assigning Quality Points of Median

DataProcessingFunctions.AddYears(dataTable) # add corresponding calendar year for each term

# Creating Term Order to sort term column
termOrder = []
for i in range(11,20):
    termOrder.append(str(i)+"W")
    termOrder.append(str(i) + "S")
    termOrder.append(str(i) + "X")
    termOrder.append(str(i) + "F")
termOrder.append(str(20)+"W")

dataTable['Term'] = pd.Categorical(dataTable['Term'], termOrder) # Organize Term column by chronological order

dataTable.sort_values(by=["Department", "Course Number", 'Term'], inplace = True) # Sort by Dept, Courses, Term

dataTable.to_csv("/Users/brianwang/Desktop/DartmouthTrends/data/augmentedData.csv", index=False) # store this version before combining sections

dataTable2 = pd.read_csv("/Users/brianwang/Desktop/DartmouthTrends/data/augmentedData.csv") # read in augmented data file

dataTable2 = DataProcessingFunctions.CombineSections(dataTable2) # combine sections

dataTable2.drop(['Course', 'Section Number', 'Enrollment', 'Points', 'Median'], axis=1, inplace=True) # drop unnecessary columns

dataTable.sort_values(by=["Department", "Course Number"], inplace = True) # Resort by Dept, Courses, Term

dataTable2.to_csv("/Users/brianwang/Desktop/DartmouthTrends/data/processedData.csv", index=False) # write final processed data to csv