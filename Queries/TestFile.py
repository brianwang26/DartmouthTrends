from Queries import TermQueries.py

# Term Options: TermQueries.allTerms, TermQueries.recentTerms
termsOfInterest = ["15F", "18F", "19F", "15S", "18W"]
coursesOfInterest = ["WRIT-5", "COSC-10"]
plotGrades = True
plotEnrollments = True

TermQueries.findCoursesTerms(coursesOfInterest, TermQueries.recentTerms, "sample", plotGrades, plotEnrollments)


