import numpy as np
import pandas as pd

census_extension = pd.read_csv("/Users/ajordan/OneDrive - McGill University/LTBI-Aust-CEA-master/Census/Census 2011/3census_data_clean.csv")
print(census_extension)

#census_post1970 = census_extension%>%filter(YARP != 1970)
census_post1970 = census_extension[(census_extension.YARP != 1970)]

print(census_post1970)

#census_1970 = census_extension%>%filter(YARP == 1970)
census_1970 = census_extension[(census_extension.YARP == 1970)]

#census_1970$ID<-seq(1:nrow(census_1970))

x = list(range(1,len(census_1970)+1))
(census_1970.insert(loc = 2, column = 'ID', value = x, allow_duplicates = False))

#census_1970$YARPv2<-census_1970$YARP-census_1970$YOBP

census_1970 = census_1970.assign(YARPv2 = lambda y: y['YARP'] - y['YOBP'])
census_1970 = census_1970[(census_1970.YARPv2 >= 0)]

# Replicate rows while simultaneously creating new YARPS
# Should produce NA's that will be filled in later
# Slight change to this. AGE_GROUPS got injected a little differently this time so had to change from [h,3] to [h,4]
#in order to make sure that YARP column was correctly indexed. k <- as.numeric changed from [i,10] to [i,11] 
#so that YARPv2 would be indexed. ID=unlist(census_1970t[h,9] changed to [h,10] so that ID column would be indexed

#for (i in 1:nrow(census_1970)){
 # k<-as.numeric(census_1970[i,11])
 # h<-as.numeric(i)
 # for (i in 1:k){
  #    census_1970<-add_row(census_1970, ID=unlist(census_1970[h,10]), YARP=unlist(census_1970[h,4])-(1*i))
  #}
#}

#pd.concat
#test = {"Unnamed: 0": None,"AGEP":None, "ID":[census_1970.iloc[[1],[2]]], "AGE_GROUP": None, 'YARP':[(census_1970.iloc[[1],[4]]-(1*i))], "COO": None, 'census_year': 2011, 'YOBP': None, 'YARP_group': None, 'NUMP': None, 'YARPv2': None}

new_df = pd.DataFrame()
for i in range(0,len(census_1970.index)):
    k = int(census_1970.iloc[i]["YARPv2"])
    h = i
    for j in range(0,k):
        new_df = pd.DataFrame({"Unnamed: 0": None,"AGEP": None, "ID": int(census_1970.iloc[h]["ID"]), "AGE_GROUP": None, 'YARP': [(int(census_1970.iloc[h]["YARP"]-(1*j)))], "COO": None, 'census_year':[2011], 'YOBP': None, 'YARP_group': None, 'NUMP': None, 'YARPv2': None})
        census_1970 = census_1970.append(new_df)
print(census_1970)