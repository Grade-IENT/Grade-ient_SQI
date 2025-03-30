import csv
import math

# Subtract 1 standard error from the mean
def stat_processing(data):
    #indices for each questions data
    iterators=[list(range(7,12)),list(range(13,18)),list(range(19,24)),list(range(25,30)),list(range(31,36)),
            list(range(37,42)),list(range(43,48)),list(range(49,54)),list(range(55,60)),list(range(61,66))]

    #loop through questions and calculate means/errors
    scores=[]
    errors=[]
    for set in iterators:
        q1=float(data[set[0]])
        q2=float(data[set[1]])
        q3=float(data[set[2]])
        q4=float(data[set[3]])
        q5=float(data[set[4]])

        n=(q1+q2+q3+q4+q5)
        mean=((q1*1)+(q2*2)+(q3*3)+(q4*4)+(q5*5))/n
        std_dev=((((mean-1)**2)*q1)+(((mean-2)**2)*q2)+(((mean-3)**2)*q3)+(((mean-4)**2)*q4)+(((mean-5)**2)*q5) + 0.001)/(n-0.999)
        std_err=std_dev/math.sqrt(n)

        scores.append(mean)
        errors.append(std_err)
        
    #switch the sign of question 8s error 

    errors[7]=-errors[7]

    #calculate final score/error and subtract one standard error from final score
    scores_adj = [scores[i] - errors[i] for i in range(len(scores))]

    return scores_adj

# Weighted measure = linear combination of entries of vector
def weighted_measure(V):
    return 1/7*(V[0] + V[4] + V[6] + V[8] + V[9]) + 1/14*(V[1] + V[2] + V[3] + V[5])

# SQI = (weighted measure)*(Q8 penalty)
def calc_SQI(V):
    WM = weighted_measure(V)
    Q8 = V[7]
    Q8_penalty = 1 + (3 - Q8)*0.05
    return round(WM*Q8_penalty, 2)

# Consider rows with the same matching criteria to be the same
# Average these rows to collapse into single row
def collapse_csv(in_file_name, criteria):
    unique_lines = {} # hash table to store unique rows
    with open(in_file_name, 'r') as in_file:
        next(in_file) # skip first line
        reader = csv.reader(in_file)
        for line in reader:
            course_code, professor = line[2][:-3], line[4]
            if criteria == 'course-professor':
                key = (course_code, professor)
            elif criteria == 'course':
                key = course_code
            elif criteria == 'professor':
                key = professor

            if key not in unique_lines:
                for i in range(5, 67):
                    line[i] = float(line[i])
                for i in range(1, 11):
                    line[-i] = float(line[-i])
                unique_lines[key] = line
            else:
                cur = unique_lines[key]
                for i in range(5, 67):
                    cur[i] += float(line[i])
                for i in range(1, 11):
                    cur[-i] = (cur[-i] + float(line[-i]))/2
                unique_lines[key] = cur
    
    out_file_name = in_file_name[:-4] + f'_collapsed_{criteria}.csv'
    with open(out_file_name, 'w', newline = '') as out_file:
        writer = csv.writer(out_file)
        for line in unique_lines.values():
            line[0], line[1] = '_', '_'
            if criteria == 'course':
                line[4] = '_'
            elif criteria == 'professor':
                line[2], line[3] = '_', '_'
            writer.writerow(line)

# Takes in input CSV and generates output CSV of all entries
def generate_SQI_csv(in_file_name, criteria):
    out_file_name = in_file_name[:-4] + '_SQI.csv'
    with open(in_file_name, 'r') as in_file, open(out_file_name, 'w', newline = '') as out_file:
        reader = csv.reader(in_file)
        writer = csv.writer(out_file)
        for line in reader:
            ratings = stat_processing(line)
            SQI = calc_SQI(ratings)
            
            course_code, course_name, professor = line[2][:-3], line[3], line[4]
            if criteria == 'course-professor':
                writer.writerow([course_code, course_name, professor, SQI])
            elif criteria == 'course':
                writer.writerow([course_code, course_name, SQI])
            elif criteria == 'professor':
                writer.writerow([professor, SQI])

def main():
    depts = ['chem', 'cs', 'eng', 'math', 'physics']
    criterias = ['course-professor', 'course', 'professor']
    for dept in depts:
        for criteria in criterias:
            collapse_csv(f'{dept}_trunc.csv', criteria)
            generate_SQI_csv(f'{dept}_trunc_collapsed_{criteria}.csv', criteria)

if __name__ == '__main__':
    main()