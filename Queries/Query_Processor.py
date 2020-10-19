import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import matplotlib.backends.backend_pdf

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

# Create Recent Terms Option (since the first term that current seniors participated in)
recentTerms = ["16F", "17W", "17S", "17X", "17F", "18W", "18S", "18X", "18F", "19W", "19S", "19X", "19F", "20W"]

# Terms and Times Dictionary
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
def get_query_result(is_courses, is_terms, academic_items, time_items, plotting_grades, plotting_enrollments, outputFile):
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

    frames = []  # initialize resulting frames
    for academic_item in academic_items: # split courses by department and number
        if is_courses:
            tokens = academic_item.split("-")
            course_dept = tokens[0]
            course_num = float(tokens[1])
            academic_item = course_dept + "-" + str(course_num)
        frames.append(data_table[(data_table[academic_index] == academic_item) & (data_table[time_index].isin(time_items))])
    result = pd.concat(frames)
    result.to_csv(outputFile + ".csv", index=False)

    analytics_and_plotting(result, academic_index, time_index, plotting_grades, plotting_enrollments)
    # enrollment_analytics()

    # pdf = matplotlib.backends.backend_pdf.PdfPages("output.pdf")


def analytics_and_plotting(data_table, academic_index, time_index, plotting_grades, plotting_enrollments):
    curr_academic_item = data_table.iloc[0].loc[academic_index]
    curr_time_items = [data_table.iloc[0].loc[time_index]]
    curr_grades = [data_table.iloc[0].loc["Mean Points"]]
    curr_enrollments = [data_table.iloc[0].loc["Enrollments"]]

    for row in range(1, data_table.shape[0]):
        if data_table.iloc[row].loc[academic_index] != curr_academic_item:  # we have arrived at different course
            # analytics of previous course
            analyze_grades(curr_academic_item, curr_time_items, time_index, curr_grades)
            analyze_enrollments(curr_academic_item, curr_time_items, time_index, curr_enrollments)
            if plotting_grades:
                plot_grades(curr_academic_item, curr_time_items, time_index, curr_grades)
            if plotting_enrollments:
                plot_enrollments(curr_academic_item, curr_time_items, time_index, curr_enrollments)

            curr_academic_item = data_table.iloc[row].loc[academic_index]
            curr_time_items = [data_table.iloc[row].loc[time_index]]  # start new terms list
            curr_grades = [data_table.iloc[row].loc["Mean Points"]]  # start new grades list
            curr_enrollments = [data_table.iloc[row].loc["Enrollments"]]

        else:
            curr_time_items.append(data_table.iloc[row].loc[time_index])
            curr_grades.append(data_table.iloc[row].loc["Mean Points"])
            curr_enrollments.append(data_table.iloc[row].loc["Enrollments"])

    analyze_grades(curr_academic_item, curr_time_items, time_index, curr_grades)
    analyze_enrollments(curr_academic_item, curr_time_items, time_index, curr_enrollments)
    if plotting_grades:
        plot_grades(curr_academic_item, curr_time_items, time_index, curr_grades)
    if plotting_enrollments:
        plot_enrollments(curr_academic_item, curr_time_items, time_index, curr_enrollments)

# def enrollment_analytics(data_table, academic_index, time_index):
def plot_grades(curr_academic_item, curr_time_items, time_index, curr_grades):
    plt.plot(curr_time_items, curr_grades)
    plt.xlabel(time_index)
    plt.ylabel('Grades by ' + time_index)
    plt.legend([curr_academic_item])
    plt.figure()
    plt.show()

def analyze_grades(curr_academic_item, curr_time_items, time_index, curr_grades):
    time_array = convert_to_time(curr_time_items, time_index)
    x = np.array(time_array).reshape((-1, 1))
    y = np.array(curr_grades)
    model = LinearRegression()
    model.fit(x, y)
    model = LinearRegression().fit(x, y)
    r_sq = model.score(x, y)
    print('Analysis for Grades of ' + curr_academic_item)
    print('Coefficient of determination: ', str(round(r_sq, 3)))
    print('Mean: ' + str(round(sum(curr_grades) / len(curr_grades), 3)))
    print('Slope:', str(round(model.coef_[0], 3)))
    if time_index == 'Term':
        constant = 83
        constant_string = "20F"
    else:
        constant = 2020  # 20F = 20*4 + 3 = 83
        constant_string = "2020"
    y_pred = model.predict(np.array([constant]).reshape(-1, 1))[0]  # predict some number
    print('Prediction of Grade for ' + constant_string + ": " +  str(round(y_pred, 3)))
    print('\n')


def plot_enrollments(curr_academic_item, curr_time_items, time_index, curr_enrollments):
    plt.plot(curr_time_items, curr_enrollments)
    plt.xlabel(time_index)
    plt.ylabel('Enrollments by ' + time_index)
    plt.legend([curr_academic_item])
    plt.figure()
    plt.show()


def analyze_enrollments(curr_academic_item, curr_time_items, time_index, curr_enrollments):
    time_array = convert_to_time(curr_time_items, time_index)
    x = np.array(time_array).reshape((-1, 1))
    y = np.array(curr_enrollments)
    model = LinearRegression()
    model.fit(x, y)
    model = LinearRegression().fit(x, y)
    r_sq = model.score(x, y)
    print('Analysis for Enrollments of ' + curr_academic_item)
    print('Coefficient of determination: ', str(round(r_sq, 3)))
    print('Mean: ' + str(round(sum(curr_enrollments)/len(curr_enrollments), 3)))
    print('Slope:', str(round(model.coef_[0], 3)))
    if time_index == 'Term':
        constant = 83
        constant_string = "20F"
    else:
        constant = 2020  # 20F = 20*4 + 3 = 83
        constant_string = "2020"
    y_pred = model.predict(np.array([constant]).reshape(-1, 1))[0]  # predict some number
    print('Prediction of Enrollment for ' + constant_string + ": " + str(round(y_pred, 3)))
    print('\n')

def convert_to_time(list, time_index):
    if time_index == "Year":
        return list
    else:
        result = []
        for term in list:
            result.append(term_to_time_dict[term])
        return result
