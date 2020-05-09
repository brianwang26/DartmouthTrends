from pandas import DataFrame
import pandas as pd

def AssigningPoints(data):

    shape = data.shape
    points = []

    for rowNum in range(shape[0]):
        grade = data.loc[rowNum]["Median"]
        # print(grade)
        if (grade == "A"):
            points.append(12)
        elif (grade == "A/A-"):
            points.append(11.5)
        elif (grade == "A-"):
            points.append(11)
        elif(grade == "A-/B+"):
            points.append(10.5)
        elif(grade == "B+"):
            points.append(10)
        elif(grade == "B+/B"):
            points.append(9.5)
        elif (grade == "B"):
            points.append(9)
        elif (grade == "B/B-"):
            points.append(8.5)
        elif (grade == "B-"):
            points.append(8)
        elif(grade == "B-/C+"):
            points.append(7.5)
        elif(grade == "C+"):
            points.append(7)
        elif(grade == "C+/C"):
            points.append(6.5)
        elif (grade == "C"):
            points.append(6)
        elif (grade == "C/C-"):
            points.append(5.5)
        elif (grade == "C-"):
            points.append(5)

    data.insert(7, "Points", points)

def ReadCourses(data):
    shape = data.shape
    depts = []
    courseNumbers = []
    sectionNumbers = []

    for rowNum in range(shape[0]):
        course = data.loc[rowNum]["Course"]
        tokens = course.split('-')
        depts.append(tokens[0])
        courseNumbers.append(tokens[1])
        sectionNumbers.append(tokens[2])

    data.insert(2, "Department", depts)
    data.insert(3, "Course Number", courseNumbers)
    data.insert(4, "Section Number", sectionNumbers)

def AddYears(data):
    shape = data.shape
    years = []

    for rowNum in range(shape[0]):
        term = data.loc[rowNum]['Term']
        year = term[:2]
        years.append("20" + year)

    data.insert(0, "Year", years)

def CombineSections(data):

    totalEnrollments = []
    numOfSections = []
    meanPoints = []
    rowsToDrop = []

    currTerm = data.loc[0]["Term"]
    currDepartment = data.loc[0]["Department"]
    currCourseNumber = data.loc[0]["Course Number"]
    enrollments = [data.loc[0]["Enrollment"]]
    points = [data.loc[0]["Points"]]

    for rowNum in range(1, data.shape[0]):
        thisTerm = data.loc[rowNum]["Term"]
        thisDepartment = data.loc[rowNum]["Department"]
        thisCourseNumber = data.loc[rowNum]["Course Number"]

        if(thisTerm == currTerm and thisDepartment == currDepartment and thisCourseNumber == currCourseNumber):
            points.append(data.loc[rowNum]["Points"])
            enrollments.append(data.loc[rowNum]["Enrollment"])
            rowsToDrop.append(rowNum)

        else:
            totalEnrollments.append(sum(enrollments))
            meanPoints.append(sum(points)/len(points))
            numOfSections.append(len(enrollments))
            currTerm = thisTerm
            currDepartment = thisDepartment
            currCourseNumber = thisCourseNumber
            enrollments = [data.loc[rowNum]["Enrollment"]]
            points = [data.loc[rowNum]["Points"]]

    totalEnrollments.append(sum(enrollments))
    numOfSections.append(len(enrollments))
    meanPoints.append(sum(points)/len(points))

    data = data.drop(data.index[rowsToDrop])
    data.drop(['Course', 'Section Number', 'Enrollment', 'Points'], axis=1, inplace=True)
    data.insert(4, "Number of Sections", numOfSections)
    data.insert(5, "Enrollments", totalEnrollments)
    data.insert(7, "Mean Points", meanPoints)
    return(data)







