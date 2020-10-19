import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

data_by_course_and_term = pd.read_csv("/Users/brianwang/Desktop/DartmouthTrends/data/data_by_course_and_term.csv")
data_by_course_and_year = pd.read_csv("/Users/brianwang/Desktop/DartmouthTrends/data/data_by_course_and_year.csv")
data_by_department_and_term = pd.read_csv("/Users/brianwang/Desktop/DartmouthTrends/data/data_by_department_and_term.csv")
data_by_department_and_year = pd.read_csv("/Users/brianwang/Desktop/DartmouthTrends/data/data_by_department_and_year.csv")

# Create All Terms Option
termsW = [str(i)+"W" for i in range(11,21)]
termsS = [str(i)+"S" for i in range(11,20)]
termsX = [str(i)+"X" for i in range(11,20)]
termsF = [str(i)+"F" for i in range(11,20)]
allTerms = termsW + termsS + termsX + termsF

# Create Recent Terms Option (since the first term that last year's seniors participated in)
recentTerms = ["16F", "17W", "17S", "17X", "17F", "18W", "18S", "18X", "18F", "19W", "19S", "19X", "19F", "20W"]

# Create All Years and Recent Years Options
allYears = [2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019]
recentYears = [2016, 2017, 2018, 2019]

# Terms and Times Dictionary (convert term to integer values)
term_to_time_dict = {"11W": 44, "11S": 45, "11X": 46, "11F": 47,
                     "12W": 48, "12S": 49, "12X": 50, "12F": 51,
                     "13W": 52, "13S": 53, "13X": 54, "13F": 55,
                     "14W": 56, "14S": 57, "14X": 58, "14F": 59,
                     "15W": 60, "15S": 61, "15X": 62, "15F": 63,
                     "16W": 64, "16S": 65, "16X": 66, "16F": 67,
                     "17W": 68, "17S": 69, "17X": 70, "17F": 71,
                     "18W": 72, "18S": 73, "18X": 74, "18F": 75,
                     "19W": 76, "19S": 77, "19X": 78, "19F": 79,
                     "20W": 80}

# input: booleans for whether we are looking at courses or departments and terms or years
    # list of academic_items (courses/departments), list of time_items (terms/years) we are looking at
    # plotting_grades & plotting_enrollments (booleans on whether to plot grades/enrollments)
    # output File: name of CSV file to write data to
# output: data table for desired courses/departments for terms/years,
   #analytics and plotting (if wanted) of grades/enrollments
def get_query_result(is_courses, is_terms, academic_items, time_items, plotting_grades, plotting_enrollments, outputFile):
    # Select proper data table based on what academic item and time item we are examining
    if(is_courses):
        academic_index = 'Course Name'
        if is_terms:
            time_index = 'Term'
            data_table = data_by_course_and_term
        else:
            time_index = 'Year'
            data_table = data_by_course_and_year
    else:
        academic_index = 'Department'
        if is_terms:
            time_index = 'Term'
            data_table = data_by_department_and_term
        else:
            time_index = 'Year'
            data_table = data_by_department_and_year

    # Find data that much parameters of academic_items and time_items
    frames = []  # initialize resulting frames
    for academic_item in academic_items:
        if is_courses: # split courses by department and number (due to issue with floats)
            tokens = academic_item.split("-")
            course_dept = tokens[0]
            course_num = float(tokens[1]) # floats are the format the course number is in
            academic_item = course_dept + "-" + str(course_num)
        # Append frames that match parameters
        frames.append(data_table[(data_table[academic_index] == academic_item) & (data_table[time_index].isin(time_items))])
    result = pd.concat(frames)
    result.to_csv(outputFile + ".csv", index=False)

    # Analytics and Plotting (handled in helper functions below
    analytics_and_plotting(result, academic_index, time_index, plotting_grades, plotting_enrollments)


# input: data table with query result, academic_index (Course or Dept), time_index (Term of Year)
   # plotting_grades & plotting_enrollments (booleans on whether to plot grades/enrollments)
# output: analytics and plotting (if requested) for the courses/departments we have queried
def analytics_and_plotting(data_table, academic_index, time_index, plotting_grades, plotting_enrollments):
    # Iterate through table and analyze the data of different courses separately
    curr_academic_item = data_table.iloc[0].loc[academic_index] # current course/department
    curr_time_items = [data_table.iloc[0].loc[time_index]] # current term/year
    curr_grades = [data_table.iloc[0].loc["Mean Points"]] # list of grades for this course/department
    curr_enrollments = [data_table.iloc[0].loc["Enrollments"]] # list of enrollments for this course/department

    for row in range(1, data_table.shape[0]):
        if data_table.iloc[row].loc[academic_index] != curr_academic_item:  # we have arrived at new course/department
            # analytics of previous course/department
            analyze_grades(curr_academic_item, curr_time_items, time_index, curr_grades)
            analyze_enrollments(curr_academic_item, curr_time_items, time_index, curr_enrollments)
            if plotting_grades:
                plot_grades(curr_academic_item, curr_time_items, time_index, curr_grades)
            if plotting_enrollments:
                plot_enrollments(curr_academic_item, curr_time_items, time_index, curr_enrollments)

            # start keeping track of next course/department we are on
            curr_academic_item = data_table.iloc[row].loc[academic_index]
            curr_time_items = [data_table.iloc[row].loc[time_index]]  # start new terms list
            curr_grades = [data_table.iloc[row].loc["Mean Points"]]  # start new grades list
            curr_enrollments = [data_table.iloc[row].loc["Enrollments"]]

        else: # continue adding data for this current course/department
            curr_time_items.append(data_table.iloc[row].loc[time_index])
            curr_grades.append(data_table.iloc[row].loc["Mean Points"])
            curr_enrollments.append(data_table.iloc[row].loc["Enrollments"])

    # analytics of final course/department in our query
    analyze_grades(curr_academic_item, curr_time_items, time_index, curr_grades)
    analyze_enrollments(curr_academic_item, curr_time_items, time_index, curr_enrollments)
    if plotting_grades:
        plot_grades(curr_academic_item, curr_time_items, time_index, curr_grades)
    if plotting_enrollments:
        plot_enrollments(curr_academic_item, curr_time_items, time_index, curr_enrollments)


# input: academic_item = this specific course/dept, list of times,
    #  time_index (Terms or Years), list of grades
# output: analysis of grades for this specific course/dept across the list of times (rounded to 3 digits)
def analyze_grades(academic_item, times_list, time_index, grades_list):
    time_array = convert_to_time(times_list, time_index) # convert times to integers
    x = np.array(time_array).reshape((-1, 1))
    y = np.array(grades_list)

    # perform simple linear regression on data using scikit-learn
    model = LinearRegression()
    model.fit(x, y)
    model = LinearRegression().fit(x, y)
    r_sq = model.score(x, y)

    # print results of analyses
    print('Analysis of Grades for ' + academic_item + ':')
    print('\t Coefficient of determination: ', str(round(r_sq, 3)))
    print('\t Mean: ' + str(round(sum(grades_list) / len(grades_list), 3))) # mean of data
    print('\t Average Change in Grade Per ' + time_index + ": " + str(round(model.coef_[0], 3)))

    # make prediction for future time
    if time_index == 'Term':
        constant = 83 # 20F = 20*4 + 3 = 83
        constant_string = "20F"
    else:
        constant = 2020
        constant_string = "2020"
    y_pred = model.predict(np.array([constant]).reshape(-1, 1))[0]  # predict for future date
    print('\t Prediction of Grade for ' + constant_string + ": " +  str(round(y_pred, 3)))
    print('\n')


# input: academic_item = this specific course/dept, list of times,
    #  time_index (Terms or Years), list of enrollments
# output: analysis of enrollments for this specific course/dept across the list of times (rounded to 3 digits)
def analyze_enrollments(academic_item, times_list, time_index, enrollments_list):
    time_array = convert_to_time(times_list, time_index)  # convert times to integers
    x = np.array(time_array).reshape((-1, 1))
    y = np.array(enrollments_list)

    # perform simple linear regression on data using scikit-learn
    model = LinearRegression()
    model.fit(x, y)
    model = LinearRegression().fit(x, y)
    r_sq = model.score(x, y)

    # print results of analyses
    print('Analysis of Enrollments for ' + academic_item + ":")
    print('\t Coefficient of determination: ', str(round(r_sq, 3)))
    print('\t Mean: ' + str(round(sum(enrollments_list) / len(enrollments_list), 3)))  # mean of data
    print('\t Average Change in Enrollment Per ' + time_index + ": " + str(round(model.coef_[0], 3)))

    # make prediction for future time
    if time_index == 'Term':
        constant = 83  # 20F = 20*4 + 3 = 83
        constant_string = "20F"
    else:
        constant = 2020
        constant_string = "2020"
    y_pred = model.predict(np.array([constant]).reshape(-1, 1))[0]  # predict for future date
    print('\t Prediction of Enrollment for ' + constant_string + ": " + str(round(y_pred, 3)))
    print('\n')


# input: academic_item = this specific course/dept, list of times,
    #  time_index (Terms or Years), list of grades
# output: plot of grades for this specific course/dept across the list of times
def plot_grades(academic_item, times_list, time_index, grades_list):
    plt.plot(times_list, grades_list)
    plt.xlabel(time_index)
    plt.ylabel('Grades by ' + time_index)
    plt.legend([academic_item])
    plt.figure()
    plt.show()


# input: academic_item = this specific course/dept, list of times,
    #  time_index (Terms or Years), list of enrollments
# output: plot of enrollments for this specific course/dept across the list of times
def plot_enrollments(academic_item, times_list, time_index, enrollments_list):
    plt.plot(times_list, enrollments_list)
    plt.xlabel(time_index)
    plt.ylabel('Enrollments by ' + time_index)
    plt.legend([academic_item])
    plt.figure()
    plt.show()


# input: list of times, time_index (Terms of Years)
# output: converted time list into numbers
def convert_to_time(times_list, time_index):
    if time_index == "Year":
        return times_list
    else:
        result = []
        for term in times_list:
            result.append(term_to_time_dict[term])
        return result