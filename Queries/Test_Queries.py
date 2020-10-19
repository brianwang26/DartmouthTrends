from Queries.Query_Processor import get_query_result

# List courses/departments you are interested in
coursesOfInterest = ["WRIT-5", "COSC-10", "MATH-20"]
departmentsOfInterest = ["COSC", "MATH", "WRIT"]

# List of times you are interested in
# Term Options: Query_Processor.allTerms, Query_Processor.recentTerms
# Term Options: Query_Process.allYears, Query_Process.recentYears
termsOfInterest = ["15S", "15F", "18W", "18F", "19W", "19F", "20W"]
yearsOfInterest = [2010, 2012, 2014, 2016, 2017, 2018, 2019]


# # Specify whether or not you want to plot grades/enrollments
plotGrades = True
plotEnrollments = True

get_query_result(is_courses=True, is_terms=True, academic_items=coursesOfInterest, time_items=termsOfInterest,
                 plotting_grades=plotGrades, plotting_enrollments = plotEnrollments, outputFile="test_course_term")





