import csv
import os

#p.csv constants#
P_ID        = 'p_id'
NAME        = 'name'
A_ID        = 'a_id'
DEP_ID      = 'dep_id'

#o.csv constants#
O_ID        = 'o_id'
P_ID        = 'p_id'
NUM         = 'num'
REORDERED   = 'reordered'

#out.csv constants#
DEP_ID      = 'dep_id'
TOT         = 'tot'
NUM_FIRST   = 'num_first'
PERCENT     = 'percent'

def get_index(dep_id_list, dep_id):
    '''
        Reuturns the index of the dep_id in the dep_id_list if found,
        else returns -1
    '''
    for i in range(len(dep_id_list)):
        if dep_id_list[i][0] == dep_id:
            return i
    return -1

def sort_list(list):
    '''
        Return a sorted list ascindingly according to the first column.
    '''
    return sorted(list, key=lambda l:l[0])

#get absolute paths of the files
p_directory     = os.path.join(os.getcwd(), '..', 'input', 'p.csv' )
o_directory     = os.path.join(os.getcwd(), '..', 'input', 'o.csv' )
out_directory   = os.path.join(os.getcwd(), '..', 'output', 'o.csv' )

#delete the old out.csv file if exists
if os.path.exists(out_directory):
  os.remove(out_directory)

dep_id_list = []
#read p.csv file
p_csv_file = open(p_directory, newline='')
p_reader = csv.DictReader(p_csv_file)
for row in p_reader:
    #get list of dep_id alng with tot
    dep_id = int(row[DEP_ID])
    if [dep_id, 1] not in dep_id_list:
        #if dep_id is not in the list, then append it along with tot = 1
        dep_id_list.append([dep_id, 1])
    else:
        #if dep_id is already in the list, then increment the tot
        dep_id_list[get_index(dep_id_list, dep_id)][1] += 1

#create out.csv
out_csv_file = open(out_directory, 'w', newline='')
fieldnames = [DEP_ID, TOT, NUM_FIRST, PERCENT]
writer = csv.DictWriter(out_csv_file, fieldnames=fieldnames)
#write the first coulmn names
writer.writeheader()

#order dep_id_list
dep_id_list = sort_list(dep_id_list)

for dep_id in dep_id_list:
    #for each dep_id search p.csv for p_id
    num_first = 0
    p_csv_file = open(p_directory, newline='')
    p_reader = csv.DictReader(p_csv_file)
    for p_row in p_reader:
        if int(p_row[DEP_ID]) == dep_id[0]:
            p_id = int(p_row[P_ID])
            #for each p_id search o.csv for reordered values
            o_csv_file = open(o_directory, newline='')
            o_reader = csv.DictReader(o_csv_file)
            for o_row in o_reader:
                if int(o_row[P_ID]) == p_id:
                    reordered = int(o_row[REORDERED])
                    if reordered == 0:
                        #set num_first to 1 if reordered = 0
                        num_first = 1
                        break
    
    record = {
        DEP_ID      : dep_id[0],
        TOT         : dep_id[1],
        NUM_FIRST   : num_first,
        PERCENT     : round(num_first/dep_id[1], 2)
    }
    #write the calculated values in out.csv
    writer.writerow(record)

out_csv_file.close()

out_csv_file = open(out_directory, newline='')
out_reader = csv.DictReader(out_csv_file)

#print field names
print('dep_id' + '\t\t' +'tot' + '\t\t' +'num_first' + '\t' + 'percent')
#print values
for row in out_reader:
    print(row[DEP_ID] + '\t\t' + row[TOT] + '\t\t' + row[NUM_FIRST] + '\t\t' + row[PERCENT])