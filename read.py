import pandas as pd
import math

file = open("AviationData.txt","r")
aviation_data = []
for line in file:
    aviation_data.append(line)
    
aviation_list = []
for row in aviation_data:
    aviation_list.append(row.split("|"))
print(len(aviation_list))
print(aviation_list[10])
lax_code = []
for row in aviation_list:
    enter_row = 0
    for col in row:
        if "LAX94LA336" in col and enter_row == 0:
            enter_row = 1
            lax_code.append(row)
    #for col in row:
print(lax_code)
print(len(lax_code))

#it perhaps is not the most efficient or compact way
#to search through aviation_data.txt

#linear time algorithm
#read in the dataset assign first row to columns
aviation_df = pd.DataFrame(aviation_list[1:]) 
cols = []
for i in aviation_list[0]:
    cols.append(i.strip())
aviation_df.columns = cols
 
print(aviation_df.head(10))

def linear_time(row):
    #this function will return row immediately upon     finding first instance
    for col in row:
        if "LAX94LA336" in col:
            return 1
    return 0

lax_keep = aviation_df.apply(linear_time,axis=1)
lax_code_linear = aviation_df[lax_keep==1]
print(lax_code_linear)

#log_n time algorithm 
#here let's sort each column
def search(col,string):
    upper_bound = len(col)-1
    lower_bound = 0
    # Set the index of the first split (remember to use math.floor)
    index = math.floor((upper_bound + lower_bound) / 2)
    # First guess at index (remember to format the guess)
    guess = col[index]
    while(guess!=string and upper_bound > lower_bound):
        if string > guess:
            lower_bound = index+1
        elif string < guess:
            upper_bound = index-1
        index = math.floor((upper_bound-lower_bound)/2+lower_bound)
        guess = col[index]
        if guess == string:
            return index
    
keep_rows = []

#for i in range(0,32):
#    aviation_df.sort_values(by=i,axis=0)
#    keep_rows.append(search(aviation_df[:]#[i],"LAX94LA336"))

#print(keep_rows)

#The hash table consumes quite a bit more memory while the linear time alogorithm takes longer.

print("Aviation DF:", aviation_df.shape)
aviation_dict_list = []
lax_dict = []
print(aviation_df.head(2))
print(type(aviation_df))
for i, row in aviation_df.iterrows():
    #aviation_dict_list.append({key:value for (key,value) in row})
    d = row.to_dict() 
    aviation_dict_list.append(d)
   # try:
  #      d = {key:value for (key,value) in row}
   #     print(d)
     #   aviation_dict_list.append(d)
    #except ValueError:
     #   print("ValueError")
    
print(len(aviation_dict_list))
print(aviation_dict_list[0:2]) 
for i in aviation_dict_list:
    for key in i.keys():
        if "LAX94LA336" in i[key]:
          lax_dict.append(i)
           
print(lax_dict)

#searching through a dictionary seems more time intenstive

#Count how many accidents occurred in each U.S. state
state_data = []
for i in aviation_df["Location"]:
    try:
        state = i.split(",")[1]
    except IndexError:
        state = ""
    state = state.strip()
    state_data.append(state)

country = []
for row in aviation_df["Country"]:
    country.append(row.strip())

aviation_df["Country"] = country
#aviation_df["fatal"] = fatal
#aviation_df["serious"] = serious
aviation_df["state"]=state_data
print(aviation_df["state"].head(5))
select = "United States" == aviation_df["Country"]
US_data = aviation_df[select==1]
print(US_data.shape)
state_accidents = {}
for s in US_data["state"]:
    if s in state_accidents:
        state_accidents[s] += 1
    else:
        state_accidents[s] = 1
max_key = ""
max_val = 0
for k,v in state_accidents.items():
    if v > max_val:
        max_key = k
        max_val = v
        
print(state_accidents) 
print(max_key, max_val)

monthly_injuries = []
import datetime
date_list = []
for d in US_data["Event Date"]:
    dt = d.split("/")
    try:
        date_val = datetime.date(int(dt[2]),int(dt[0]),1)
    except IndexError:
        date_val = datetime.date(1900,1,1)
    date_list.append(date_val)
    
US_data["date"] = date_list



#monthly_injuries = pd.DataFrame(index=US_data["date"].unique(),columns=["injuries"])
#print(monthly_injuries.shape)
#print(monthly_injuries.head(5))

US_data["Total Serious Injuries"] =pd.to_numeric(US_data["Total Serious Injuries"],errors='coerce')
US_data["Total Fatal Injuries"] =pd.to_numeric(US_data["Total Fatal Injuries"],errors='coerce')
US_data = US_data.fillna(value=0)

print(US_data.head(5))
monthly_injuries = {}

for d in US_data["date"].unique():
    month_data = US_data[US_data["date"]==d]
    monthly_injuries[d] = sum(month_data["Total Serious Injuries"]+month_data["Total Fatal Injuries"])

print(monthly_injuries)
monthly_injuries_df =pd.DataFrame.from_dict(monthly_injuries,orient="index")
monthly_injuries_df["injuries"]=monthly_injuries_df[0]
monthly_injuries_df["date"]=monthly_injuries_df.index
print(monthly_injuries_df.head())

#   
#    monthly_injuries[d]["serious"]=sum(month_data["Total Serious Injuries"])
#    monthly_injuries[d]["fatal"]=sum(month_data["Total Fatal Injuries"])


#Now create a line plot
import matplotlib.pyplot as plt

fig = plt.figure()
monthly_injuries_df.plot("date","injuries",kind="line",color='red')
plt.show()

#state_accidents = aviation_df

#determine which state had the most accidents overall

#Additional exercises:
#map out accidents using basemap library
#count number of accidents by air carrier
#count number of accidents by airplane make and model
#figure out percentage of accidents that occur under adverse wea