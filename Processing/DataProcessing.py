import pandas as pd
from Processing import DataProcessingFunctions

# RAW DATA ---> AUGMENTED DATA
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


# AUGMENTED DATA ---> PROCESSED DATA

dataTable2 = pd.read_csv("/Users/brianwang/Desktop/DartmouthTrends/data/augmentedData.csv")

dataTable2 = DataProcessingFunctions.CombineSections(dataTable2) # combine sections

dataTable2.drop(['Course', 'Section Number', 'Enrollment', 'Points', 'Median'], axis=1, inplace=True) # drop repetitive columns

dataTable2.sort_values(by=["Department", "Course Number"], inplace = True) # Re-sort by Dept, Courses, Term

dataTable2.to_csv("/Users/brianwang/Desktop/DartmouthTrends/data/processedData.csv", index=False) # write final processed data to csv


# PROCESSED DATA ---> BY COURSE/TERM, BY COURSE/YEAR, ..... DATA

processed_data = pd.read_csv("/Users/brianwang/Desktop/DartmouthTrends/data/processedData.csv")

courses_and_terms = DataProcessingFunctions.organize_courses_and_terms(processed_data)
courses_and_terms.to_csv("/Users/brianwang/Desktop/DartmouthTrends/data/data_by_course_and_term.csv", index=False)

courses_and_years = DataProcessingFunctions.organize_courses_and_years(processed_data)
courses_and_years.to_csv("/Users/brianwang/Desktop/DartmouthTrends/data/data_by_course_and_year.csv", index=False)

departments_and_terms = DataProcessingFunctions.organize_departments_and_terms(processed_data)
departments_and_terms.to_csv("/Users/brianwang/Desktop/DartmouthTrends/data/data_by_department_and_term.csv", index=False)

departments_and_terms = DataProcessingFunctions.organize_departments_and_years(processed_data)
departments_and_terms.to_csv("/Users/brianwang/Desktop/DartmouthTrends/data/data_by_department_and_year.csv", index=False)