import pandas as pd
import matplotlib.pyplot as plt

# Create All Terms Option
termsW = [str(i)+"W" for i in range(11,21)]
termsS = [str(i)+"S" for i in range(11,20)]
termsX = [str(i)+"X" for i in range(11,20)]
termsF = [str(i)+"F" for i in range(11,20)]
allTerms = termsW + termsS + termsX + termsF

# Create Recent Terms Option (since the first term that current seniors participated in)
recentTerms = ["16F", "17W", "17S", "17X", "17F", "18W", "18S", "18X", "18F", "19W", "19S", "19X", "19F", "20W"]

def findCourses(data, courses, terms = allTerms):
    frames = []
    for course in courses:
        tokens = course.split("-")
        courseDept = tokens[0]
        courseNumber = float(tokens[1])
        frames.append(data[(data['Department'] == courseDept) & (data['Course Number'] == courseNumber) & (data['Term'].isin(terms))])
    return(pd.concat(frames))

def plotEnrollment(courseData, courses):
    currCourse = courseData.iloc[0, 1] + str(courseData.iloc[0,2]) # sets current course to first course
    currTerm =  courseData.iloc[0, 0] # helps look for terms with multiple sections
    currEnrollments = [] # holds enrollments of different sections in same term
    terms = [courseData.iloc[0,0]] # holds all terms (non-repeating)
    enrollments = [] # holds enrollments per term (combining sections)

    for rowNum in range(courseData.shape[0]):
        if ((courseData.iloc[rowNum, 1] + str(courseData.iloc[rowNum,2])) != currCourse):
            print(courseData.iloc[rowNum, 1] + str(courseData.iloc[rowNum,2]))
            print(currCourse)
            plt.plot(terms, enrollments)
            currTerm = courseData.iloc[rowNum, 0]
            currEnrollments = []
            terms = [courseData.iloc[rowNum, 0]]
            enrollments = []

        if (courseData.iloc[rowNum, 0] != currTerm):
            enrollments.append(sum(currEnrollments))
            currEnrollments = []
            terms.append(courseData.iloc[rowNum, 0])
            currTerm = courseData.iloc[rowNum, 0]

        currEnrollments.append(courseData.iloc[rowNum,4])

        if(rowNum == courseData.shape[0]-1):
            enrollments.append(sum(currEnrollments))

    plt.ylabel('Terms')
    plt.xlabel('Enrollments by Term')
    plt.legend([course for course in courses], loc='upper left')
    plt.show()

def plotGrades(courseData):

    currTerm = courseData.iloc[0, 0]  # helps look for terms with multiple sections
    terms = [courseData.iloc[0, 0]]  # holds all terms (non-repeating)
    points = []  # holds enrollments per term (combining sections)
    currPoints = []  # holds enrollments of different sections in same term

    for rowNum in range(courseData.shape[0]):

        if (courseData.iloc[rowNum, 0] != currTerm):
            points.append(sum(currPoints)/len(currPoints))
            currPoints = []
            terms.append(courseData.iloc[rowNum, 0])
            currTerm = courseData.iloc[rowNum, 0]

        currPoints.append(courseData.iloc[rowNum, 6])

        if (rowNum == courseData.shape[0] - 1):
            points.append(sum(currPoints)/len(currPoints))

    plt.plot(terms, points)
    plt.ylabel('Terms')
    plt.xlabel('Median Quality Points')
    plt.show()


termsOfInterest = ["15F", "18F", "19F", "15S", "18W"]
coursesOfInterest = ["MATH-40", "ENGS-50"]

dataTable = pd.read_csv("data/processedData.csv")
queryResult = findCourses(dataTable, coursesOfInterest, allTerms)
print(queryResult)
# plotEnrollment(queryResult, coursesOfInterest)
queryResult.to_csv("data/courseTrial.csv", index = False)