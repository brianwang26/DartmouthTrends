from Queries import TermQueries

# List courses you are interested in
coursesOfInterest = ["WRIT-5", "COSC-10"]

# List terms you are interested in
# Term Options: TermQueries.allTerms, TermQueries.recentTerms
termsOfInterest = ["15F", "18F", "19F", "15S", "18W"]

# Specify whether or not you want to plot grades/enrollments
plotGrades = True
plotEnrollments = True

TermQueries.findCoursesTerms(coursesOfInterest, TermQueries.recentTerms, "sample", plotGrades, plotEnrollments)