# B652 HW2
# Lalit Pandey
# Paventhan Vivekanandan
# Zachary Wilkerson

import pandas as pd
import numpy as np
import math
import KNN

#====================================================
# Data processing (Zach)
#   Input: read from xlsx file provided by David
#   Output: pandas dataframe, with column titles:
#       [District, Address, Bedrooms, Sitting Rooms, Source] and then class value Rent

# initializeCaseBase
# Reads data from provided file into a case base, represented as a pandas DataFrame object.
#   This specific reader assumes that the input data is for HW2
# Parameters:
#   inputFilename = the source file for case data, must be xlsx format (default filename is
#                   "hw2 rent prediction data.xlsx")
#   sheetName = the sheet to be read from the input file to create the case base, assumes
#               all data are from the same sheet (default sheet name is "hw2 rent prediction data")
# Returns: a pandas DataFrame representing the case base
def initializeCaseBase(inputFilename:str="hw2 rent prediction data.xlsx",\
                        sheetName:str="hw2 rent prediction data"):

    # Read input Excel file
    df = pd.read_excel(inputFilename, sheet_name=sheetName)

    # Split the Type field into two numeric fields for bedrooms and sitting rooms
    bedrooms = []
    sittingRooms = []
    for _, case in df.iterrows():
        temp = case["Type"]
        bedrooms.append(int(str(temp)[0]))
        sittingRooms.append(int(str(temp)[1]))
    df["Bedrooms"] = bedrooms
    df["Sitting Rooms"] = sittingRooms

    # Normalize Bedrooms and Sitting Rooms numeric fields to be on [0,1] to avoid implicit weighting
    for col in ("Bedrooms", "Sitting Rooms"):
        df[col] = (df[col] - df[col].min()) / (df[col].max() - df[col].min())

    # Drop Type field, which is now unnecessary, and Case Number field, which is meaningless
    df = df.drop("Case Number", axis=1)
    df = df.drop("Type", axis=1)

    # print(df)
    return df

#====================================================
# KNN (Lalit)
#   Input: Zach's pandas dataframe
#   Output: prediction (i.e., list of neighbor entries [features and Rent prediction]
#       and their distances from the query)

class KNN_retrieval:

    def __init__(self, k):
        self.k = k

    def nominal_distance(self, a, b, w=1):
        if a == b:
            return 0
        else:
            return w

    def euclidean_distance(self, a, b, w=1):
        return w*((a-b)**2)

    def find_neighbors(self, df, x, w):
        distances = []
        for i in range(df.shape[0]):
            f1 = self.nominal_distance(df.iloc[i]['District'], x['District']) * w['District']
            f2 = self.nominal_distance(df.iloc[i]['Address'], x['Address']) * w['Address']
            f3 = self.nominal_distance(df.iloc[i]['Source'], x['Source']) * w['Source']
            f4 = self.euclidean_distance(df.iloc[i]['Bedrooms'], x['Bedrooms']) * w['Bedrooms']
            f5 = self.euclidean_distance(df.iloc[i]['Sitting Rooms'], x['Sitting Rooms']) * w['Sitting Rooms']
            distances.append((df.iloc[i], math.sqrt(f1+f2+f3+f4+f5)/5))
        distances.sort(key=lambda x: x[1])
        return distances[:self.k]


#====================================================
# Adaptation (Paventhan)
#   Input: Lalit's list of neighbor information
#   Output: formal prediction/error

class KNN_adaptation:

    def __init__(self, k, w):
        self.caseBase = initializeCaseBase()
        self.k = k
        self.w = w

    def predict(self):
        retrieval = KNN_retrieval(self.k)
        error = []
        for i in range(self.caseBase.shape[0]):
            potentialNeighbors = pd.concat([self.caseBase.iloc[0:i], self.caseBase.iloc[i+1:]])
            testCase = self.caseBase.iloc[i]
            nearestNeighbors = retrieval.find_neighbors(potentialNeighbors, testCase, self.w)
            prediction = 0.0
            for neighbor, distance in nearestNeighbors:
                #opportunity for adaptation
                #opportunity for weighted average vote
                prediction += neighbor["Rent"]
            prediction /= self.k
            error.append(abs(testCase["Rent"] - prediction))
        return error

    def cbr_adpt_predict(self):
        retrieval = KNN_retrieval(self.k)
        error = []
        for i in range(self.caseBase.shape[0]):
            potentialNeighbors = pd.concat([self.caseBase.iloc[0:i], self.caseBase.iloc[i+1:]])
            testCase = self.caseBase.iloc[i]
            nearestNeighbors = retrieval.find_neighbors(potentialNeighbors, testCase, self.w)
            prediction = 0.0
            for neighbor, distance in nearestNeighbors:
                #opportunity for adaptation
                #opportunity for weighted average vote
                #print ("i: {}, neighbor: {}, distance: {}".format(i, neighbor, distance))
                sr_dis = neighbor["Sitting Rooms"] - testCase["Sitting Rooms"]
                adj_amt1 = neighbor["Rent"] * .20
                
                if sr_dis > 0:
                    adj_amt1 = -adj_amt1
                elif sr_dis == 0:
                    adj_amt1 = 0

                br_dis = neighbor["Bedrooms"] - testCase["Bedrooms"]
                adj_amt2 = neighbor["Rent"] * .60
                
                if br_dis > 0:
                    adj_amt2 = -adj_amt2
                elif br_dis == 0:
                    adj_amt2 = 0
                
                prediction += (neighbor["Rent"] + adj_amt1 + adj_amt2)
            prediction /= self.k
            error.append(round(abs(testCase["Rent"] - prediction), 1))
        return error


#=====
#Extra stuff/test code

# Quick test function to make sure that preprocessing is working correctly
#   Note that Rent field is in a different order, but since this is a DataFrame, it doesn't matter
# def testDriver():
#     print(initializeCaseBase())

# def testKNN(k):
#     classifier = KNN.KNN(k)
#     df = initializeCaseBase()
#     for i in range(df.shape[0]):
#         train_x = pd.concat([df.iloc[0:i], df.iloc[i+1:]]).drop("Rent", axis=1)
#         train_y = pd.concat([df.iloc[0:i], df.iloc[i+1:]])["Rent"]
#         test_x = df.iloc[i].drop("Rent")
#         test_y = df.iloc[i]["Rent"]
#         classifier.final_prediction(train_x, train_y, test_x)
# testKNN(1)

def KNN_driver():
    w = pd.Series({
        "District":2.0,
        "Source":.1,
        "Bedrooms":1.15,
        "Sitting Rooms":1.05,
        "Address":.1
    })
    knn = KNN_adaptation(2, w)
    err_lst = knn.predict()
    print(err_lst)
    print("Before CBR Aapdation: average error={}".format(sum(err_lst)/len(err_lst)))
    err_lst = knn.cbr_adpt_predict()
    print(err_lst)
    print("After CBR Adapdation: average error={}".format(sum(err_lst)/len(err_lst)))

KNN_driver()
