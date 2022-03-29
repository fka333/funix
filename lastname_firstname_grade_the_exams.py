import re
import pandas as pd



# TASK 2
def valid_check(file):
    print('**** ANALYZING ****')
    error_count = 0
    file_length = 0
    valid_list = []
    for line in file.readlines():
        file_length += 1
        line_split = line.strip().split(',')
        student_id_pattern = re.compile(r'(N\d{8})')
        if (len(line_split) != 26 or not student_id_pattern.match(line_split[0])):
            error_count += 1 # Not to be duplicated if one row match both conditions
            if len(line_split) != 26:
                print('Invalid line of data: does not contain exactly 26 values:')
                print(line)
            elif not student_id_pattern.match(line_split[0]):
                print('Invalid line of data: N# is invalid')
                print(line)
        else:
            valid_list.append(line_split) # for task 3
    if error_count == 0:
        print('No error found!')

    print('**** REPORT ****')    
    valid_count = file_length - error_count
    print(f'Total valid lines of data: {valid_count}')
    print(f'Total invalid lines of data: {error_count}')
    return valid_list

# TASK 3
answer_key = "B,A,D,D,C,B,D,A,C,C,D,B,A,B,A,C,B,D,A,C,A,A,B,D,D"
answer_list = answer_key.split(',')

def class_score(file, answer_list):
    valid_list = valid_check(file)
    total_scores = []
    for actual_answer_list in valid_list:
        student_score = 0
        for actual_answer, key in zip(actual_answer_list[1:], answer_list): # valid_list[1:] to remove student id
            if actual_answer == key:
                student_score += 4
            elif actual_answer == '':
                student_score += 0
            else:
                student_score += -1
        total_scores.append([actual_answer_list[0], student_score])
    
    sorted_scores = sorted([element[1] for element in total_scores])
    avg_score = sum(sorted_scores) / len(sorted_scores)
    middle = int(len(sorted_scores)/2)
    if len(sorted_scores)%2 == 0:
        median = sum([sorted_scores[middle-1], sorted_scores[middle]]) / 2
    else:
        median = sorted_scores[middle]
    
    print(f'Mean (average) score: {avg_score}')
    print(f'Highest score: {sorted_scores[-1]}')
    print(f'Lowest score: {sorted_scores[0]}')
    print(f'Range of scores: {sorted_scores[-1] - sorted_scores[0]}')
    print(f'Median score: {median}')
    return total_scores # for task 4

# TASK 4
def make_scores_file(file, answer_list, filename):
    total_class_scores = class_score(file, answer_list)
    file_to_write = f'.\Data Files\{filename}_grades.txt'

    with open(file_to_write, 'w') as f:
        for student_score in total_class_scores:
            f.write(student_score[0])
            f.write(',')
            f.write(str(student_score[1]))
            f.write('\n')


# TASK 5
# 5.1


# 5.2
def valid_check2(data):
    print('**** ANALYZING ****')
    invalid_len = data[(data[0].str.split(',').str.len() == 26) == False]
    invalid_student_id = data[(data[0].str.split(',').str[0].str.match(r'(N\d{8})') == True) == False]
    if len(invalid_len) + len(invalid_student_id) > 0:
        print('Invalid line of data: does not contain exactly 26 values:')
        print(invalid_len)

        print('Invalid line of data: N# is invalid')
        print(invalid_student_id)
    else:
        print('No error found!')

    print('**** REPORT ****')    
    valid_data = data[(~data.index.isin(invalid_len.index)) & (~data.index.isin(invalid_student_id.index))]
    print(f'Total valid lines of data: {len(valid_data)}')
    print(f'Total invalid lines of data: {len(invalid_len) + len(invalid_student_id)}')
    return valid_data

# 5.3
answer_key = "B,A,D,D,C,B,D,A,C,C,D,B,A,B,A,C,B,D,A,C,A,A,B,D,D"
answer_list = answer_key.split(',')

def scoring(actual_answer_list, answer_list):
    student_score = 0
    for actual_answer, key in zip(actual_answer_list, answer_list):
        if actual_answer == key:
            student_score += 4
        elif actual_answer == '':
            student_score += 0
        else:
            student_score += -1
    return student_score

def class_score2(data, answer_list):
    valid_data = valid_check2(data)[0].str.split(',', expand=True)
    valid_data.columns = ['student_id'] + [f'q{i}' for i in range(1, 26)]
    valid_data['score'] = valid_data.apply(lambda x: scoring(x[1:], answer_list), axis=1)

    total_scores = valid_data[['student_id', 'score']].values.tolist()
    sorted_scores = sorted([element[1] for element in total_scores])
    avg_score = sum(sorted_scores) / len(sorted_scores)
    middle = int(len(sorted_scores)/2)
    if len(sorted_scores)%2 == 0:
        median = sum([sorted_scores[middle-1], sorted_scores[middle]]) / 2
    else:
        median = sorted_scores[middle]
    
    print(f'Mean (average) score: {avg_score}')
    print(f'Highest score: {sorted_scores[-1]}')
    print(f'Lowest score: {sorted_scores[0]}')
    print(f'Range of scores: {sorted_scores[-1] - sorted_scores[0]}')
    print(f'Median score: {median}')
    return total_scores

# 5.4  
def make_scores_file2(data, answer_list, filename):
    total_class_scores = class_score2(data, answer_list)
    file_to_write = f'.\Data Files\{filename}_grades2.txt'

    with open(file_to_write, 'w') as f:
        for student_score in total_class_scores:
            f.write(student_score[0])
            f.write(',')
            f.write(str(student_score[1]))
            f.write('\n')

def main(method):
    filename = input("Enter a class file to grade (i.e. class1 for class1.txt): ")
    if method == 'tradition':
        try:
            file = open(f'./Data Files/{filename}.txt')
            print(f"Successfully opened {filename}.txt")
            make_scores_file(file, answer_list, filename)
        except:
            print('File cannot be found.')
    
    elif method == 'pandas':
        try:
            df = pd.read_csv(f'.\Data Files\{filename}.txt', sep='\n', header=None)
            make_scores_file2(df, answer_list, filename)
        except:
            print('File cannot be found.')


if __name__ == '__main__':
    while True:
        method = input('Enter way to handle tasks: traditional or pandas: ')
        if method not in ['tradition', 'pandas']:
            print('Other methods have not been implemented yet! Please key in `tradition` or `pandas`!')
        else:
            break
    main(method)
    

    
    



