from pandas import DataFrame
import pandas as pd

# output: data table where all courses are split into department, course number, and section number
def ReadCourses(data):
    shape = data.shape
    depts = [] # hold column of all depts
    courseNumbers = [] # holds column of all courseNumbers
    sectionNumbers = [] # holds column of all sectionNumbers

    for rowNum in range(shape[0]): # courses are in the format: Dept-CourseNumber-SectionNumber
        course = data.loc[rowNum]["Course"]
        tokens = course.split('-')
        depts.append(tokens[0])
        courseNumbers.append(tokens[1])
        sectionNumbers.append(tokens[2])

    data.insert(2, "Department", depts)
    data.insert(3, "Course Number", courseNumbers)
    data.insert(4, "Section Number", sectionNumbers)


# output: data table where all courses receive a "quality points" designation for their median
def AssigningPoints(data):

    shape = data.shape
    points = []

    for rowNum in range(shape[0]):
        grade = data.loc[rowNum]["Median"]

        # assigning quality points for the median of each course
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

# output: data table where each term has a corresponding year listed
def AddYears(data):
    shape = data.shape
    years = []

    for rowNum in range(shape[0]):
        term = data.loc[rowNum]['Term']
        year = term[:2]
        years.append("20" + year)

    data.insert(0, "Year", years)

# output: average the medians and sum the enrollments of courses with multiple sections; keeps only one section of a course from a term
def CombineSections(data):

    totalEnrollments = [] # holds column of enrollments
    numOfSections = [] # holds column of number of sections of each course
    meanPoints = [] # holds mean of the quality points of each course
    rowsToDrop = [] # holds which rows to drop

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
            rowsToDrop.append(rowNum) # will drop this row because its a same course and same term of previous section

        else:
            totalEnrollments.append(sum(enrollments)) # total enrollment for this course across sections
            meanPoints.append(sum(points)/len(points)) # average median for this course across sections
            numOfSections.append(len(enrollments)) # number of sections for this course

            currTerm = thisTerm
            currDepartment = thisDepartment
            currCourseNumber = thisCourseNumber
            enrollments = [data.loc[rowNum]["Enrollment"]]
            points = [data.loc[rowNum]["Points"]]

    # for last row
    totalEnrollments.append(sum(enrollments))
    numOfSections.append(len(enrollments))
    meanPoints.append(sum(points)/len(points))

    data = data.drop(data.index[rowsToDrop]) # drops the rows of repeat courses
    data.insert(8, "Number of Sections", numOfSections)
    data.insert(9, "Enrollments", totalEnrollments)
    data.insert(10, "Mean Points", meanPoints)
    return(data)







