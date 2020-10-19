from Queries.Query_Processor import get_query_result

# List courses you are interested in

coursesOfInterest = ["WRIT-5", "COSC-10", "MATH-20"]
departmentsOfInterest = ["COSC", "MATH", "WRIT"]

# List terms you are interested in
# Term Options: TermQueries.allTerms, TermQueries.recentTerms
termsOfInterest = ["15F", "18F", "19F", "15S", "18W"]
yearsOfInterest = [2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019]

# # Specify whether or not you want to plot grades/enrollments
# plotGrades = True
# plotEnrollments = False
#
# TermQueries.find_courses_by_terms(coursesOfInterest, termsOfInterest, "sample", plotGrades, plotEnrollments)
#
# course_or_department_message = "1 for Course, 2 for Department"
# term_or_year_message = "1 for Term, 2 for Year"
#
# def user_interaction():
#     print(course_or_department_message)
#     is_course = input()
#     while is_course != '1' and is_course != '2':
#         print("Not a valid input")
#         is_course = input()
#
#     print(term_or_year_message)
#     is_term = input()
#     while is_term != '1' and is_term != '2':
#         print("Not a valid input")
#         is_term = input()
#

get_query_result(False, False, departmentsOfInterest, yearsOfInterest, True, True, "sample")