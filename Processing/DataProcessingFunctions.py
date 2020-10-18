from pandas import DataFrame
import pandas as pd
from itertools import islice

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
    currCourseNumber = (data.loc[0]["Course Number"])
    enrollments = [data.loc[0]["Enrollment"]]
    points = [data.loc[0]["Points"]]

    for rowNum in range(1, data.shape[0]):
        thisTerm = data.loc[rowNum]["Term"]
        thisDepartment = data.loc[rowNum]["Department"]
        thisCourseNumber = (data.loc[rowNum]["Course Number"])

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

# input: processed data
# output: data organized by course and terms
def organize_courses_and_terms(processed_data):
    result = processed_data # make copy of input
    course_names = []
    for row in range(processed_data.shape[0]):
        current_course = processed_data.iloc[row].loc['Department'] + "-" + str(processed_data.iloc[row].loc['Course Number'])
        course_names.append(current_course)
    result.insert(2, "Course Name", course_names)
    result.drop(['Year', 'Department', 'Course Number'], axis=1, inplace=True) # drop unnecessary columns
    return result


# input: processed data
# output: data organized by courses and years
def organize_courses_and_years(processed_data):
    result = processed_data # make copy of input
    total_enrollments = []  # holds column of enrollments
    total_sections = []  # holds column of number of sections of each course
    course_names = [] # holds column for courses
    mean_points = []  # holds mean of the quality points of each course
    rows_to_drop = []  # holds which rows to drop

    current_year = processed_data.iloc[0].loc['Year']
    current_course = processed_data.iloc[0].loc['Department'] + "-" + str(processed_data.iloc[0].loc['Course Number'])
    course_names.append(current_course)
    current_sections = [processed_data.iloc[0].loc['Number of Sections']]
    current_enrollments = [processed_data.iloc[0].loc['Enrollments']]
    current_points = [processed_data.iloc[0].loc['Mean Points']]

    for row in range(1, processed_data.shape[0]):
        this_year = processed_data.loc[row]['Year']
        this_course = processed_data.iloc[row].loc['Department'] + "-" + str(processed_data.iloc[row].loc['Course Number'])

        if (this_year == current_year and this_course == current_course):
            current_sections.append(processed_data.loc[row]['Number of Sections'])
            current_enrollments.append(processed_data.loc[row]['Enrollments'])
            current_points.append(processed_data.loc[row]['Mean Points'])
            rows_to_drop.append(row)  # will drop this row because its a same course and same term of previous section

        else:
            total_sections.append(sum(current_sections))  # number of sections for this course
            total_enrollments.append(sum(current_enrollments))  # total enrollment for this course across sections
            mean_points.append(sum(current_points) / len(current_points))  # average median for this course across sections

            current_year = this_year
            current_course = this_course
            current_sections = [processed_data.loc[row]['Number of Sections']]
            current_enrollments = [processed_data.loc[row]['Enrollments']]
            current_points = [processed_data.loc[row]['Mean Points']]
            course_names.append(current_course)

    # for last row
    total_sections.append(sum(current_sections))
    total_enrollments.append(sum(current_enrollments))
    mean_points.append(sum(current_points) / len(current_points))

    result = result.drop(processed_data.index[rows_to_drop])  # drops the rows of repeat courses
    result.drop(['Term', 'Department', 'Course Number', 'Number of Sections', 'Enrollments', 'Mean Points'], axis=1, inplace=True) # drop unnecessary columns
    result.insert(1, "Course Name", course_names)
    result.insert(2, "Number of Sections", total_sections)
    result.insert(3, "Enrollments", total_enrollments)
    result.insert(4, "Mean Points", mean_points)
    return result


def organize_departments_and_terms(processed_data):
    result = processed_data

    termOrder = []
    for i in range(11,20):
        termOrder.append(str(i)+"W")
        termOrder.append(str(i) + "S")
        termOrder.append(str(i) + "X")
        termOrder.append(str(i) + "F")
    termOrder.append(str(20)+"W")

    result['Term'] = pd.Categorical(result['Term'], termOrder) # Organize Term column by chronological order
    result.sort_values(by=["Department", "Term"], inplace = True) # Resort by Dept, Courses, Term

    all_terms = []
    total_enrollments = []  # holds column of enrollments
    total_sections = []  # holds column of number of sections of each course
    mean_points = []  # holds mean of the quality points of each course
    rows_to_drop = []  # holds which rows to drop

    current_term = result.iloc[0].loc['Term']
    all_terms = [current_term]
    current_dept = result.iloc[0].loc['Department']
    current_sections = [result.iloc[0].loc['Number of Sections']]
    current_enrollments = [result.iloc[0].loc['Enrollments']]
    current_points = [result.iloc[0].loc['Mean Points']]

    for index, row in islice(result.iterrows(), 1, None):
        this_term = row['Term']
        this_dept = row['Department']

        if (this_term == current_term and this_dept == current_dept):
            current_sections.append(row['Number of Sections'])
            current_enrollments.append(row['Enrollments'])
            current_points.append(row['Mean Points'])
            rows_to_drop.append(index)  # will drop this row because its a same department and same term of previous section

        else:
            total_sections.append(sum(current_sections))  # number of sections for this department
            total_enrollments.append(sum(current_enrollments))  # total enrollment for this course across sections
            mean_points.append(sum(current_points) / len(current_points))  # average median for this department

            current_term = this_term
            all_terms.append(current_term)
            current_dept = this_dept
            current_sections = [row['Number of Sections']]
            current_enrollments = [row['Enrollments']]
            current_points = [row['Mean Points']]

    # for last row
    total_sections.append(sum(current_sections))
    total_enrollments.append(sum(current_enrollments))
    mean_points.append(sum(current_points) / len(current_points))

    print(len(total_sections))
    result = result.drop(result.index[rows_to_drop])  # drops the rows of repeat courses
    result.drop(['Year', 'Term', 'Course Number', 'Number of Sections', 'Enrollments', 'Mean Points'], axis=1, inplace=True) # drop unnecessary columns
    result.insert(0, "Term", all_terms)
    result.insert(2, "Number of Sections", total_sections)
    result.insert(3, "Enrollments", total_enrollments)
    result.insert(4, "Mean Points", mean_points)
    print(result.shape[0])
    return result


def organize_departments_and_years(processed_data):
    result = processed_data
    result.sort_values(by=["Department", "Year"], inplace = True) # Resort by Dept, Courses, Term

    all_years = []
    total_enrollments = []  # holds column of enrollments
    total_sections = []  # holds column of number of sections of each course
    mean_points = []  # holds mean of the quality points of each course
    rows_to_drop = []  # holds which rows to drop

    current_year = result.iloc[0].loc['Year']
    all_years= [current_year]
    current_dept = result.iloc[0].loc['Department']
    current_sections = [result.iloc[0].loc['Number of Sections']]
    current_enrollments = [result.iloc[0].loc['Enrollments']]
    current_points = [result.iloc[0].loc['Mean Points']]

    for index, row in islice(result.iterrows(), 1, None):
        this_year = row['Year']
        this_dept = row['Department']

        if (this_year == current_year and this_dept == current_dept):
            current_sections.append(row['Number of Sections'])
            current_enrollments.append(row['Enrollments'])
            current_points.append(row['Mean Points'])
            rows_to_drop.append(index)  # will drop this row because its a same department and same term of previous section

        else:
            total_sections.append(sum(current_sections))  # number of sections for this department
            total_enrollments.append(sum(current_enrollments))  # total enrollment for this course across sections
            mean_points.append(sum(current_points) / len(current_points))  # average median for this department

            current_year = this_year
            all_years.append(current_year)
            current_dept = this_dept
            current_sections = [row['Number of Sections']]
            current_enrollments = [row['Enrollments']]
            current_points = [row['Mean Points']]

    # for last row
    total_sections.append(sum(current_sections))
    total_enrollments.append(sum(current_enrollments))
    mean_points.append(sum(current_points) / len(current_points))

    print(len(total_sections))
    result = result.drop(result.index[rows_to_drop])  # drops the rows of repeat courses
    result.drop(['Year', 'Term', 'Course Number', 'Number of Sections', 'Enrollments', 'Mean Points'], axis=1, inplace=True) # drop unnecessary columns
    result.insert(0, "Year", all_years)
    result.insert(2, "Number of Sections", total_sections)
    result.insert(3, "Enrollments", total_enrollments)
    result.insert(4, "Mean Points", mean_points)
    print(result.shape[0])
    return result









