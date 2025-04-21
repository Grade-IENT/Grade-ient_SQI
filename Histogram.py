import numpy as np
import matplotlib.pyplot as plt

def get_SQIs(file_name):
    SQIs = []
    with open(file_name, 'r') as file:
        for line in file:
            SQIs.append(float(line.split(',')[-1]))
    return SQIs

def plot_all_SQIs(dept, dept_abbr):
    fig, axs = plt.subplots(ncols = 3)

    SQIs = get_SQIs(f'courses\\{dept}\\{dept_abbr}_trunc_collapsed_course_SQI.csv')
    ax = axs[0]
    ax.hist(SQIs, [x/2 for x in range(11)])
    ax.set_title(f'{dept} Course SQIs')
    ax.set_xlabel('SQI')
    ax.set_ylabel('Frequency')
    mean, median = np.mean(SQIs), np.median(SQIs)
    ax.axvline(mean, color = 'r')
    ax.axvline(median, color = 'lime')

    SQIs = get_SQIs(f'courses\\{dept}\\{dept_abbr}_trunc_collapsed_professor_SQI.csv')
    ax = axs[1]
    ax.hist(SQIs, [x/2 for x in range(11)])
    ax.set_title(f'{dept} Professor SQIs')
    ax.set_xlabel('SQI')
    ax.set_ylabel('Frequency')
    mean, median = np.mean(SQIs), np.median(SQIs)
    ax.axvline(mean, color = 'r')
    ax.axvline(median, color = 'lime')

    SQIs = get_SQIs(f'courses\\{dept}\\{dept_abbr}_trunc_collapsed_course-professor_SQI.csv')
    ax = axs[2]
    ax.hist(SQIs, [x/2 for x in range(11)])
    ax.set_title(f'{dept} Course-Professor SQIs')
    ax.set_xlabel('SQI')
    ax.set_ylabel('Frequency')
    mean, median = np.mean(SQIs), np.median(SQIs)
    ax.axvline(mean, color = 'r')
    ax.axvline(median, color = 'lime')

    plt.suptitle(f'{dept} SQIs')
    plt.show()

depts = ['Chemistry', 'Computer Science', 'Engineering', 'Math', 'Physics']
dept_abbrs = ['chem', 'cs', 'eng', 'math', 'physics']
for dept, dept_abbr in zip(depts, dept_abbrs):
    plot_all_SQIs(dept, dept_abbr)