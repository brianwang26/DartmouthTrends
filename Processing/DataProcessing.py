import pandas as pd
from Processing import DataProcessingFunctions

# Checking if commits work


# dataTable = pd.read_csv("data/rawData.csv")
# dataTable.rename(columns={'TERM':'Term','ENRL':'Enrollment','MEDIAN':'Median', 'COURSE':'Course'}, inplace=True)
# DataProcessingFunctions.ReadCourses(dataTable) # Splitting Courses into Dept, Course #, Section #
# DataProcessingFunctions.AssigningPoints(dataTable) # Assigning Quality Points of Median
# DataProcessingFunctions.AddYears(dataTable)
#
# # Creating Term Order to sort term column
# termOrder = []
# for i in range(11,20):
#     termOrder.append(str(i)+"W")
#     termOrder.append(str(i) + "S")
#     termOrder.append(str(i) + "X")
#     termOrder.append(str(i) + "F")
# termOrder.append(str(20)+"W")
#
# dataTable['Term'] = pd.Categorical(dataTable['Term'], termOrder) # Organize Term column by chronological order
# dataTable.sort_values(by=["Department", "Course Number", 'Term'], inplace = True) # Sort by Dept, Courses, Term
# dataTable.to_csv("data/processedData.csv", index=False)

dataTable = pd.read_csv("data/processedData.csv")

print(dataTable.shape[0])

dataTable = DataProcessingFunctions.CombineSections(dataTable)

print(dataTable.shape[0])

dataTable.to_csv("data/combined.csv", index=False)
