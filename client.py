import pandas as pd

from Queries.Query_Processor import recentTerms, allTerms, recentYears, allYears, get_query_result

coursesOfInterest = ["WRIT-5", "COSC-10", "MATH-20"]
departmentsOfInterest = ["WRIT", "COSC", "MATH"]

termsOfInterest = ["15F", "18F", "19F", "15S", "18W"]
yearsOfInterest = [2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019]

get_query_result(is_courses=False, is_terms=False, academic_items=departmentsOfInterest, time_items=allYears,
                 plotting_grades=True, plotting_enrollments=True, outputFile="sample")