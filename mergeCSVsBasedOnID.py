#  @author Dr. Milto Miltiadou
#  @date March 2023
#  @version 1.0
#
## package mergeCSVsBasedOnID
#  @brief Method that takes as input two csv files and a column identifier. It then merges the files horizontally based on this identifier. 
#  @param[in] icsv1       : input csv file 1
#  @param[in] icsv2       : input csv file 2
#  @param[in] indentifier : the label of the column that the merge will be based on 
#
#  how to run: python mergeCSVsBasedOnID.py -icsv1 <icsv1.csv> -icsv2 <icsv1.csv> -label <labelIdentifier> 
#
#
# example:  python "C:/Users/mm2705/Documents/Cambridge/Scripts/PythonScriptsFLF/mergeCSVsBasedOnID.py" -icsv1 "C:/Users/mm2705/Documents/Cambridge/Scripts/SampleData/TestIndClassSentinel2b_reduced_c.csv" -icsv2 "C:/Users/mm2705/Documents/Cambridge/Scripts/SampleData/fieldDatawithIds.csv" -label "index" -ocsv  "C:/Users/mm2705/Documents/Cambridge/Scripts/SampleData/mergedcsv.csv"
#


import argparse
import pandas as pd
import numpy as np

# parsing command line inputs
parser = argparse.ArgumentParser()
parser.add_argument("-icsv1",
     required=True,
     help="Input csv file 1",
     metavar='<string>')
parser.add_argument("-icsv2",
     required=True,
     help="Input csv file 2",
     metavar='<string>')
parser.add_argument("-label",
     required=True,
     help="The label of the column that the merge will be based on",
     metavar='<string>')
parser.add_argument("-ocsv",
     required=True,
     help="The name of the output merged csv file",
     metavar='<string>')

params = vars(parser.parse_args())
icsv1  = params["icsv1"]
icsv2  = params["icsv2"]
label  = params["label"]
ocsv   = params["ocsv" ]

print ("icsv1 = ", icsv1) 
print ("icsv2 = ", icsv2)
print ("label = ", label)
print ("ocsv  = ", ocsv ) 




df1 = pd.read_csv(icsv1)
df2 = pd.read_csv(icsv2)

mergedDF = pd.merge(df1, df2,on=label,how='outer')

mergedDF.to_csv(ocsv, index=False)



print("   ***   EXIT   ***")