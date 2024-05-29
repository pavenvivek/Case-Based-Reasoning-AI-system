import numpy as np

class KNN:
  #constructor to initialize the value of K
  def __init__(self,k): 
    self.k = k

  # where a and b are the two points and w is the weight, as per the instruction.
  def euclidean_distance(self,a,b,w = 1):
    return np.sqrt(np.sum(w*((a-b)**2)))
  
  #initializes the training data and training label
  def fitting(self,x,y):    
    self.xtrain_items = x  
    self.ytrain_items = y  

  #compute distance of each sample from the training data   
  def predicting(self,samples):    #s are the multiple samples
    distances = []
    for x in samples:              # take each value from samples
      for items in xtrain_items:   # find distance of that sample from every training data
        distances = [self.euclidean_distance(x, items)]  #gets all the distances

    return distances
  
  #measure the accuracy of the final predictions
  def final_prediction(self,x,y,samples):
    self.fitting(x,y)
    pred = self.predicting(samples)
    #accuracy = 
