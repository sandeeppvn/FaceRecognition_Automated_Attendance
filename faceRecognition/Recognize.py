# import cv2
from .HausdorffMethod import hausdorff
from .Database import database

#Find the mean of hausdorff list, to remove duplicates
def mean_key_value_list(l):
    freq={}
    sum={}
    for x in l:
        if(x[1] in freq.keys()):
            freq[x[1]]+=1
            sum[x[1]]+=x[0]
        else:
            freq[x[1]]=1
            sum[x[1]]=x[0]
    result=[]
    for x in freq.keys():
        result.append([sum[x]/freq[x],x])
    return result

#Recognize the detected image
def recognize(test_points,method):
    hausdorff_list=[]
    templates = database()

    #For each template in the database,compare test_feature; 
    for template in templates:
        name,template_points = template
        #Here hausdrauff_dist value can either be hausdorff distance of 
        #1.All points togethor, 
        #2. Weighted summation of each feature, 
        #3.Line Hausdrauff Distance of features, 
        #4. Line hausdorff Distance of verenoi
        hausdorff_list.append([hausdorff(template_points,test_points,method),name])


    #Remove all hausdorff values which ae greater than threshold as they are not present in out database
    threshold = 200
    for i in range(len(hausdorff_list)-1,-1,-1):
        if(hausdorff_list[i][0]>=threshold):
            hausdorff_list.remove(hausdorff_list[i])

    #If no images matched closely, then the hausdorff list is empty
    if(len(hausdorff_list)==0):
        return "Not Found"

    #Find the mean of hausdorff list, to remove duplicates
    hausdorff_list = mean_key_value_list(hausdorff_list)
   
    # for i in hausdorff_list:
    #     print(i)

    #If multiple matches, find the min distance match from the database
    value,name = min(hausdorff_list)

    return name