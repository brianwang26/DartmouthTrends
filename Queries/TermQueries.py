import pandas as pd
import matplotlib.pyplot as plt

dataTable = pd.read_csv("processedData.csv")

# Create All Terms Option
termsW = [str(i)+"W" for i in range(11,21)]
termsS = [str(i)+"S" for i in range(11,20)]
termsX = [str(i)+"X" for i in range(11,20)]
termsF = [str(i)+"F" for i in range(11,20)]
allTerms = termsW + termsS + termsX + termsF

# Create Recent Terms Option (since the first term that current seniors participated in)
recentTerms = ["16F", "17W", "17S", "17X", "17F", "18W", "18S", "18X", "18F", "19W", "19S", "19X", "19F", "20W"]

# input: list of courses and list of terms; booleans of whether to plot grades and plot enrollments; file name to write result into
# output: write table of data queried to specified CSV file

def findCoursesTerms(courses, terms, outputFile, plotGrades = False, plotEnrollments = False):
    frames = [] # initialize resulting frames
    for course in courses: # split courses by department and number
        tokens = course.split("-")
        courseDept = tokens[0]
        courseNumber = float(tokens[1])
        frames.append(dataTable[(dataTable['Department'] == courseDept) & (dataTable['Course Number'] == courseNumber) & (dataTable['Term'].isin(terms))])

    result = pd.concat(frames)
    result.to_csv(outputFile + ".csv", index=False)

    if(plotGrades):
        currCourse = result.iloc[0][2] + str(result.iloc[0][3]) # retrieves 1st course from result table
        currTerms = [result.iloc[0][1]] # instantiates list of terms with first course (terms held in 1st column)
        currGrades = [result.iloc[0][6]] # will hold the grades of the course (grades held in 6th column)

        for rowNum in range(result.shape[0]):
            if ((result.iloc[rowNum][2] + str(result.iloc[rowNum][3]) != currCourse)): # we have arrived at different course
                # plot previous course
                plt.plot(currTerms, currGrades)
                plt.xlabel('Terms')
                plt.ylabel('Grades by Term')
                plt.legend([currCourse])
                plt.show()

                currTerms = [result.iloc[rowNum][1]] # start new terms list
                currGrades = [result.iloc[rowNum][6]] # start new grades list
                currCourse = result.iloc[rowNum][2] + str(result.iloc[rowNum][3])

            else:
                currTerms.append(result.iloc[rowNum][1])
                currGrades.append(result.iloc[rowNum][6])

        plt.plot(currTerms, currGrades, label = currCourse) # plots for final course in the query
        plt.xlabel('Terms')
        plt.ylabel('Grades by Term')
        plt.legend([currCourse])
        plt.show()

    if (plotEnrollments):
        currCourse = result.iloc[0][2] + str(result.iloc[0][3]) # retrieves 1st course from result table
        currTerms = [result.iloc[0][1]] # instantiates list of terms with first course (terms held in 1st column)
        currEnrollments = [result.iloc[0][5]] # will hold the grades of the course (grades held in 6th column)

        for rowNum in range(result.shape[0]):
            if ((result.iloc[rowNum][2] + str(result.iloc[rowNum][3]) != currCourse)): # we have arrived at different course
                # plot previous course
                plt.plot(currTerms, currEnrollments)
                plt.xlabel('Terms')
                plt.ylabel('Enrollments by Term')
                plt.legend([currCourse])
                plt.show()

                currTerms = [result.iloc[rowNum][1]] # start new terms list
                currEnrollments = [result.iloc[rowNum][5]] # start new grades list
                currCourse = result.iloc[rowNum][2] + str(result.iloc[rowNum][3])

            else:
                currTerms.append(result.iloc[rowNum][1])
                currEnrollments.append(result.iloc[rowNum][5])

        # plots for final course in the query
        plt.plot(currTerms, currEnrollments)
        plt.xlabel('Terms')
        plt.ylabel('Enrollments by Term')
        plt.legend([currCourse])
        plt.show()


termsOfInterest = ["15F", "18F", "19F", "15S", "18W"]
coursesOfInterest = ["MATH-20", "ECON-22"]

findCoursesTerms(coursesOfInterest, recentTerms, "courseTrial", True, True)