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

plotGrades = True,
get_query_result(False, False, departmentsOfInterest, yearsOfInterest, True, True, "sample")
