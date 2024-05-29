###########################################
### XAI Homework 3
### Spring 2022
### Ethan Eldridge, Paventhan Vivekanandan, 
### Kaitlynne Wilkerson
###########################################

import copy
import math
import time

def main ():
    """
    This function runs the main program. 
    """
    ## holds all cases and case feature meanings; initially empty
    cases = {}
    ranges = {'HolidayType': [], 'Price': [], 'NumberOfPersons': [], 'Region': [], 'Transportation': [], 'Duration': [], 'Season': [], 'Accommodation': [], 'Hotel': []}

    ## holds all conversation questions
    questions = ['What is your preferred destination?', 'How many people are taking the trip?', 'How long will your trip last?', 'What is your preferred means of transportation to get to the destination?', 'What season would you like to travel in?', 'What is your preferred level of accommodation?', 'What is your preferred type of holiday?']
    q_to_feat = {'What is your preferred destination?': 'Region', 'How many people are taking the trip?': 'NumberOfPersons', 'How long will your trip last?': 'Duration', 'What is your preferred means of transportation to get to the destination?': 'Transportation','What is your preferred level of accommodation?': 'Accommodation', 'What is your preferred type of holiday?': 'HolidayType', 'What season would you like to travel in?': 'Season'}

    # the weights are used to adjust the distance. So they are inversly correlated which means higher the weight lower the impact
    f_wts = {'HolidayType' : 2, 'NumberOfPersons' : 1, 'Region' : 1, 'Transportation' : 2, 'Duration' : 4, 'Season' : 3, 'Accommodation' : 5, 'Hotel' : 5}
    
    # uncomment this to make weights have no effect
    #f_wts = {'HolidayType' : 5, 'NumberOfPersons' : 5, 'Region' : 5, 'Transportation' : 5, 'Duration' : 5, 'Season' : 5, 'Accommodation' : 5, 'Hotel' : 5}

    ## keeps track of which questions have been answered
    answered = []

    ## keeps track of next 3 questions to be displayed to the user
    top_qs = []

    ## keeps track of target query data
    target = {'HolidayType': [], 'NumberOfPersons': [], 'Region': [], 'Transportation': [], 'Duration': [], 'Season': [], 'Accommodation': []}
    
    ## treating season as nominal
    season = {'March' : 'Spring', 'April' : 'Spring', 'May' : 'Spring', 'June' : 'Summer', 'July' : 'Summer', 'August' : 'Summer', 'September' : 'Autumn', 'October' : 'Autumn', 'November' : 'Autumn', 'December' : 'Winter', 'January' : 'Winter', 'February' : 'Winter', 'Spring' : 'Spring', 'Summer' : 'Summer', 'Autumn' : 'Autumn', 'Winter' : 'Winter', 'Arbitrary' : 'Arbitrary'}
    season_v = {'Arbitrary' : 0, 'Spring' : 1, 'Summer' : 2, 'Autumn' : 3, 'Winter' : 4}

    ## keeps track of when to end conversation
    c_flag = 1

    ## keeps track of when to ask a new q
    new_q = 0

    ## keeps track of cases retrieved
    ret_cases = []
    ret_cases_d = {} # to keep track of distance

    chosen_case = 0

    ## builds case base
    build_cases(cases, ranges)

    ####### start of conversation #######
    ## defines intial q to be asked
    q = questions[0]

    ## start of conversation loop; ended when user indicates want to end conversation or all questions have been asked
    while (c_flag == 1):
        ## checks to make sure there are still questions to be asked; if not, break the loop

        ## send q to conversation to be asked and get user input
        feat = q_to_feat[q]
        conversation(ranges, q, target, feat)
        answered += [q]
        new_q = 0

        ## choose the next 3 questions to be presented
        # Method: currently adds questions based on place in list and not asked status
        top_qs = []
        for i in questions:
            if len(top_qs) == 3:
                break
            elif i not in answered:
                top_qs += [i]

        ## retrieve cases from case base
        ret_cases_d = retrieve_cases(cases, feat, target, ret_cases_d, season, season_v, f_wts)
        
        # If there is no case information on the user's region, restart the process
        if (len(ret_cases_d)==0):
            print("\nSorry, we don't seem to have any info on trips fitting that description. Please select another region and try again.")
            answered = []
            time.sleep(3)
            continue

        ## display cases to user
        print("\n")
        print("Here are the top 3 cases that match the data provided so far: ")
        count = 1
        for i,d in ret_cases_d.items():
            i = eval(i)
            #print(str(count) + ": " + str(i['JourneyCode']) + ", " + str(round(d, 2)))
            # printing distance to act as similarity score
            print("{}: case code -> {}, distance -> {}".format(count, i['JourneyCode'], round(d, 2)))
            count += 1
            
            if count == 4:
                break
        print("\n")

        ## breaks the loop if all questions have been answered
        if len(answered) == 7:
            c_flag = 0
            break

        ## display next top qs to ask
        print("\n")
        print("Here are some relevant questions to refine your search results: ")
        count = 1
        for i in top_qs:
            print(str(count) + ": " + i)
            count += 1
        print("\n")

        ## loop choice question until new question is chosen or conversation ended
        while (new_q == 0):    
            ## present user a choice on where the conversation goes next
            print("\n")
            print("What would you like to do next?")
            print("1: View more information on a case. ")
            print("2: Select a new question. ")
            print("3: End the dialogue. (Note: this will terminate the search.)")
            print("\n")
            ans = input ("Please enter the number associated with your choice: ")
            print("\n********************************\n")
            ans = int(ans)

            ## check for data format
            ch = 1
            while (ch == 1):
                if ans != 1 and ans != 2 and ans != 3:
                    print ("\n")
                    print("Your entry was invalid. Try again. ")
                    ans = input ("Please enter the number associated with your choice: ")
                    print("\n********************************\n")
                    ans = int(ans)
                else:
                    ch = 0  

            ret_cases = list(map(lambda x: eval(x), list(ret_cases_d.keys())))
            ## call choice function to execute the choice
            new_q, q = choice (ans, ret_cases, top_qs, target)

            ## end conversation
            if new_q == -1:
                c_flag = 0
                if type(q) == int:
                    ind = 0
                    for i in range(len(ret_cases)):
                        if int(ret_cases[i]["JourneyCode"]) == int(q):
                            chosen_case = i
        

    #### Present top case found to user ##### 
    ### Should output: case number and description, adapt prices for differences between Number of Persons, Duration, and Season, output a description of differences in each w/ effect on price, and total price
    print("\n")
    print("Here is the best match to the provided data: ")
    for k,v in ret_cases[chosen_case].items():
        if k != 'Adapted_Price':
            print("{}: {}".format(k, v))
        else:
            mod_str = ""
            if target['NumberOfPersons'] != []:
                mod_str = mod_str + 'NumberOfPersons = ' + str(target['NumberOfPersons']) + ', '
            if target['Duration'] != []:
                mod_str = mod_str + 'Duration = ' + str(target['Duration']) + ', '
            if target['Season'] != []:
                mod_str = mod_str + 'Season = ' + target['Season'] + ', '
            if mod_str != "":
                print("### {} for {} is {} ###".format(k, mod_str, v))

    
    ####### Uncomment for debugging #########
    #print(len(answered))
    #print(target)
    #########################################



def build_cases (cases, ranges):
    """
    This function builds the case base and value definitions using the case_base.txt file. Input: case base dictionary and dictionary designed to carry all possible values of each feature. Return: nothing. 
    """
    a = 0
    flag = 0
    junk = 0
    feats = ['HolidayType', 'Price', 'NumberOfPersons', 'Region', 'Transportation', 'Duration', 'Season', 'Accommodation', 'Hotel']
    new = {'JourneyCode': 0, 'HolidayType': 0, 'Price': 0, 'NumberOfPersons': 0, 'Region': 0, 'Transportation': 0, 'Duration': 0, 'Season': 0, 'Accommodation': 0, 'Hotel': 0}
    code = 0
    file = open("case_base.txt")
    ## uncomment for debugging
    #file = open('test.txt')
    data = file.readlines()

    ## builds cases from text data
    for i in data: 
        if 'defcase' in i:
            flag = 1
        elif flag == 1:
            if 'JourneyCode:' in i:
                value = i.split(":")
                value[1] = value[1].strip(" \n:,	")
                new['JourneyCode'] = value[1]
                code = value[1]
            elif 'HolidayType:' in i:
                value = i.split(":")
                value[1] = value[1].strip(" \n:,	")
                new['HolidayType'] = value[1]
            elif 'Price:' in i:
                value = i.split(":")
                value[1] = value[1].strip(" \n:,	")
                new['Price'] = value[1]
            elif 'NumberOfPersons:' in i:
                value = i.split(":")
                value[1] = value[1].strip(" \n:,	")
                new['NumberOfPersons'] = value[1]
            elif 'Region:' in i:
                value = i.split(":")
                value[1] = value[1].strip(" \n:,	")
                new['Region'] = value[1]
            elif 'Transportation:' in i:
                value = i.split(":")
                value[1] = value[1].strip(" \n:,	")
                new['Transportation'] = value[1]
            elif 'Duration:' in i:
                value = i.split(":")
                value[1] = value[1].strip(" \n:,	")
                new['Duration'] = value[1]
            elif 'Season:' in i:
                value = i.split(":")
                value[1] = value[1].strip(" \n:,	")
                new['Season'] = value[1]
            elif 'Accommodation:' in i:
                value = i.split(":")
                value[1] = value[1].strip(" \n:,	")
                new['Accommodation'] = value[1]
            elif 'Hotel:' in i:
                value = i.split(":")
                value[1] = value[1].strip(' "\n.:,	')
                new['Hotel'] = value[1]
                cases[code] = copy.copy(new)
                flag = 0

        ## builds value definitions for each feature
        if 'deftype' in i:
            flag = 2
            if "NumbOfPersons" in i:
                current = 'NumberOfPersons'
            else:
                for x in feats:
                    if x in i:
                        current = x
        elif flag == 2: 
            if current == 'Price' or current == 'NumberOfPersons' or current == 'Duration': 
                if ' range' in i:
                    for c in i:
                        if c.isalnum() == False and c != " " and c != "[" and c != "]" and c != "." and c != '\n':
                            junk = 1
                            break
                    if junk == 1:
                        junk = 0
                        pass
                    else:
                        value = i.split('[')
                        value[1] = value[1].strip(' [].	\n') 
                        a, b = value[1].split('..')
                        ranges[current] = [int(a), int(b)]
                        flag = 0
            else: 
                value = i.split('(')
                v = value[0].strip(' ')
                if '(' in i:
                    value[1] = value[1].strip("\n")
                if 'range' == v: 
                    for c in i:
                        if c.isalnum() == False and c != " " and c != "(" and c != ")" and c != "." and c != '\n':
                            junk = 1
                            break
                    if junk == 1:
                        junk = 0
                        pass
                    else:
                        #value = i.split('(')
                        value[1] = value[1].strip(' ().	\n')
                        s = value[1].split(" ")
                        ranges[current] = s
                        flag = 0

def retrieve_cases (cases, f, target, ret_cases, season, season_v, f_wts):

    adapted_price = 0

    # retrieval for first question
    if ret_cases == {}:
        #new_ret_cases = {}
        for k,v in cases.items():
            if target[f] == v[f]:
                cases[k]['Adapted_Price'] = cases[k]['Price']
                ret_cases[str(cases[k])] = 0
        ret_cases = dict(sorted(ret_cases.items(), key=lambda item: item[1]))
    # If the attribute is nominal
    elif not str(target[f]).isdigit():
        new_ret_cases = {}
        
        if f == 'Season':
            for i,d in ret_cases.items():
                i = eval(i)
                if season[target[f]] == season[i[f]] or target[f] == 'Arbitrary':
                    new_ret_cases[str(i)] = 0 + d
                else:
                    # if requested season is during summer or summer increase cost by 10% else decrease by 10%
                    if season[target[f]] == "Summer" or season[target[f]] == "Spring":
                        adapted_price = int(i['Adapted_Price']) + (0.10 * int(i['Adapted_Price']))
                    else:
                        adapted_price = int(i['Adapted_Price']) - (0.10 * int(i['Adapted_Price']))

                    i['Adapted_Price'] = round(adapted_price, 2)
                        
                    new_ret_cases[str(i)] = (1.01-(f_wts[f]/5)) * math.sqrt((abs(season_v[season[target[f]]] - season_v[season[i[f]]]) ** 2) + (d ** 2))
        else:
            for i,d in ret_cases.items():
                i = eval(i)
                if target[f] == i[f]:
                    new_ret_cases[str(i)] = 0 + d
                else:
                    new_ret_cases[str(i)] = (1.01-(f_wts[f]/5)) * math.sqrt(2 + (d ** 2))
        ret_cases = dict(sorted(new_ret_cases.items(), key=lambda item: item[1]))
    # If the attribute is numerical
    else:
        new_ret_cases = {}
        for i,d in ret_cases.items():
            i = eval(i)
            if target[f] == int(i[f]):
                new_ret_cases[str(i)] = 0 + d
            else:
                if target[f] < int(i[f]):
                    adapted_price = int(i['Adapted_Price']) - (abs(target[f] - int(i[f])) * (int(i['Adapted_Price'])/int(i[f])))
                elif target[f] > int(i[f]):
                    adapted_price = int(i['Adapted_Price']) + (abs(target[f] - int(i[f])) * (int(i['Adapted_Price'])/int(i[f])))

                i['Adapted_Price'] = round(adapted_price, 2)

                new_ret_cases[str(i)] = (1.01-(f_wts[f]/5)) * math.sqrt((abs(target[f] - int(i[f])) ** 2) + (d ** 2))  # this corresponds to Euclidean distance
                
        ret_cases = dict(sorted(new_ret_cases.items(), key=lambda item: item[1]))

    return ret_cases

def conversation (ranges, q, target, feat):
    """
    This function asks questions, obtains user data and stores user data. Input: all possible feature value dictionary, the question to be asked, the target data dictionary, and the relevant feature being asked about. Return: nothing.
    """
    top_qs = []

    print("\n\n")
    print(q)
    count = 1
    if feat == 'Price' or feat == 'NumberOfPersons' or feat == 'Duration':
        start = ranges[feat][0]
        end = ranges[feat][1]
        while (1):
            ans = input ('Please input a number between ' + str(start) + " and " + str(end) + ": ")
            if start <= int(ans) <= end:
                break
        a = int(ans)
    else:
        for i in ranges[feat]:
            print(str(count) + ': ' + str(i))
            count += 1
        ans = input ('Please input the number of the answer that best matches: ')
        a = ranges[feat][int(ans)-1]
    target[feat] = a

def choice (c, ret_cases, top_qs, target):
    """
    This function executes each possible choice in the conversation once cases and new questions have been displayed. Input: a choice code, list of the top 3 cases and list of the top 3 questions. Return: a code indicating whether to ask a new question, end the conversation, or keep providing users choices and a question (real question if question is chosen, otherwise junk). 
    """
    response = 0
    q = 0
    ## user chooses to view a case
    if c == 1:
        view = True
        while view:
            print("Which case would you like to view?")
            count = 1
            for i in ret_cases:
                print(str(count) + ": " + str(i['JourneyCode']))
                count += 1
                
                if count == 4:
                    break
            print("\n")
            ans = input ("Please enter a number: ")
            ans = int(ans)

            ## check for data format
            ch = 1
            while (ch == 1):
                if ans != 1 and ans != 2 and ans != 3:
                    print ("\n")
                    print("Your entry was invalid. Try again. ")
                    ans = input ("Please enter the number associated with your choice: ")
                    ans = int(ans)
                else:
                    ch = 0
                    ## display selected case info
                    feats = ['HolidayType', 'Price', 'NumberOfPersons', 'Region', 'Transportation', 'Duration', 'Season', 'Accommodation', 'Hotel', 'Adapted_Price']
                    print("\nHere is more information on the case you selected: ")
                    id = ans-1
                    print('JourneyCode: ' + str(ret_cases[id]['JourneyCode']))
                    for i in feats:
                        if i == 'Price' or i == 'NumberOfPersons' or i == 'Duration':
                            print(i + ": " + str(ret_cases[id][i]))
                        elif i == 'Adapted_Price':
                            #print(i + ": " + str(ret_cases[id][i]))
                            mod_str = ""
                            if target['NumberOfPersons'] != []:
                                mod_str = mod_str + 'NumberOfPersons = ' + str(target['NumberOfPersons']) + ', '
                            if target['Duration'] != []:
                                mod_str = mod_str + 'Duration = ' + str(target['Duration']) + ', '
                            if target['Season'] != []:
                                mod_str = mod_str + 'Season = ' + target['Season'] + ', '
                            if mod_str != "":
                                print("{} for {} is {}".format(i, mod_str, ret_cases[id][i]))
                            else:
                                print("{} => {}".format(i, mod_str, ret_cases[id][i]))
                        else:
                            print(i + ": " + ret_cases[id][i])

            ## give user the option to end conversation by choosing one of the displayed cases 
            b = input("Does this case match your preferences? Please enter Y or N: ")
            while (1):
                if b == "Y" or b == "N":
                    break
                else: 
                    b = input("Input invalid. Please enter either Y or N: ")
            if b == "Y":
                response = -1
                d = ans-1
                q = int(ret_cases[d]['JourneyCode'])
                view = False
            else:   
                another = input("Would you like to view another case? Y or N: ")
                while (another != "Y") and (another != "N"):
                    another = input("Input invalid. Please enter either Y or N: ")
                if another == "Y":
                    continue
                else:
                    view = False

    ## user chooses to answer another question
    elif c == 2:
        print("Which question would you like to answer next?")
        count = 1
        for i in top_qs:
            print(str(count) + ": " + i)
            count += 1
        print("\n")
        ans = input ("Please enter a number: ")
        ans = int(ans)
                
        ## check for data format
        ch = 1
        while (ch == 1):
            if ans != 1 and ans != 2 and ans != 3:
                print ("\n")
                print("Your entry was invalid. Try again. ")
                ans = input ("Please enter the number associated with your choice: ")
                print("\n********************************\n")
                ans = int(ans)
            else:
                ch = 0
                
        q = top_qs[ans-1]
        response = 1


    ## user chooses to end conversation
    elif c == 3:
        print("\n\n")
        print("You have selected to terminate the search. ")
        response = -1
        q = "Terminated."

    return response, q


if __name__ == '__main__':
    main()