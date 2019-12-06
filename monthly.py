#pyhon3

import pandas as pd
import numpy as np
import csv
from datetime import datetime
import sys


print("")
print("Importing data . . . ")
print("")
df_repoff = pd.read_csv('repoffinput.csv', usecols = ['Organization Name (English)', 'Organization Name (Chinese)', 'Professional Supervisory Unit (English)', 'Professional Supervisory Unit (Chinese)', 'Organization Origin', 'Field of Work', 'Registration Location', 'Date of Registration', 'Permitted Area(s) of Operation', 'Month', 'Aging', 'Agriculture', 'Animal Protection', 'Arts and Culture', 'Civil Soc\'y Cap\'y building', 'Disabilities', 'Disaster Relief', 'Econ. Development', 'Education', 'Energy', 'Environment', 'Ethnic Affairs', 'Gender Issues', 'Health', 'Human Rights', 'Infrastructure', 'Int\'l Relations/Exchange', 'Labor', 'Law and Governance', 'LGBTQ Issues', 'Media', 'Migrants', 'Poverty Alleviation', 'Religion', 'Rural Issues/Devt', 'Sport', 'Technology', 'Tourism', 'Trade', 'Urban Issues/Devt', 'Youth', 'ALL OF CHINA', 'Anhui', 'Beijing', 'Chongqing', 'Fujian', 'Gansu', 'Guangdong', 'Guangxi', 'Guizhou', 'Hainan', 'Hebei', 'Heilongjiang', 'Henan', 'Hubei', 'Hunan', 'Inner Mongolia', 'Jiangsu', 'Jiangxi', 'Jilin', 'Liaoning', 'Ningxia', 'Qinghai', 'Shaanxi', 'Shandong', 'Shanghai', 'Shanxi', 'Sichuan', 'Tianjin', 'Tibet', 'Xinjiang', 'Xinjiang Bingtuan', 'Yunnan', 'Zhejiang', 'Unknown'])

df_tempact = pd.read_csv('tempactinput.csv', usecols = ['Organization Name (English)', 'Organization Name (Chinese)', 'Organization Origin', 'Start Date', 'End Date', 'Aging', 'Agriculture', 'Animal Protection', 'Arts and Culture', 'Civil Society Capacity Building', 'Disabilities', 'Disaster Relief', 'Economic Development', 'Education', 'Energy', 'Environment', 'Ethnic Affairs', 'Gender Issues', 'Health', 'Human Rights', 'Infrastructure', 'International Relations/Exchange', 'Labor', 'Law and Governance', 'LGBTQ Issues', 'Media', 'Migrants', 'Poverty Alleviation', 'Religion', 'Rural Issues/Development', 'Sport', 'Technology', 'Tourism', 'Trade', 'Urban Issues/Development', 'Youth', 'Field Unknown', 'Length in days', 'Length in months', 'All of China', 'Anhui', 'Beijing', 'Chongqing', 'Fujian', 'Gansu', 'Guangdong', 'Guangxi', 'Guizhou', 'Hainan', 'Hebei', 'Heilongjiang', 'Henan', 'Hubei', 'Hunan', 'Inner Mongolia', 'Jiangsu', 'Jiangxi', 'Jilin', 'Liaoning', 'Ningxia', 'Qinghai', 'Shaanxi', 'Shandong', 'Shanghai', 'Shanxi', 'Sichuan', 'Tianjin', 'Tibet', 'Xinjiang', 'Xinjiang Bingtuan', 'Yunnan', 'Zhejiang', 'Location Unknown'])


print("What is the last date you want included in the data? YYYY-MM-DD") #if you want to incorporate this more elegantly into the command line check out page 46 in Learn Python the Hard Way

input_date = input()
#input_date = '2019-11-30'

# https://www.journaldev.com/23365/python-string-to-datetime-strptime
data_cutoff = datetime.strptime(input_date, '%Y-%m-%d')
h1_date = datetime.strftime(data_cutoff, '%B %Y')
footnote_date = datetime.strftime(data_cutoff, '%B %-d, %Y')

print("")
print("Just to be clear, you'll want to use \"" + footnote_date + "\" as the cutoff date, right?  With \"" + h1_date + "\" appearing in the graphics' headings?  y/n")
print("")
if input() == "y":
	print("")
	print ("Lovely. Computing . . .")
else:
	print("")
	print ("Yikes, sorry. Terminating program.")
	sys.exit("Closed.")



########## PUTTING IN SOME CHECKS TO MAKE SURE YOU'RE AWAKE ####################
# sort the registration dates https://stackoverflow.com/questions/28161356/sort-pandas-dataframe-by-date
df_repoff['Date of Registration'] = pd.to_datetime(df_repoff['Date of Registration'])
df_repoff = df_repoff.sort_values('Date of Registration')
# filter out the entries after the cutoff date  https://www.interviewqs.com/ddi_code_snippets/select_pandas_dataframe_rows_between_two_dates
date_filter = (df_repoff['Date of Registration'] <= data_cutoff)
df_repoff = df_repoff.loc[date_filter]
total_ROs = len(df_repoff)
print("")
print("Based on this data cutoff date, you should have " + str(total_ROs) + " total ROs included in this dataset. Is that correct?  y/n")
print("")
if input() == "y":
	print("")
	print ("Superb. Moving on . . .")
else:
	print("")
	print ("Something has gone terribly wrong. Terminating program.")
	sys.exit("Closed.")

# sort the TA start dates https://stackoverflow.com/questions/28161356/sort-pandas-dataframe-by-date
df_tempact['Start Date'] = pd.to_datetime(df_tempact['Start Date'])
df_tempact = df_tempact.sort_values('Start Date')
# filter out the entries after the cutoff date  https://www.interviewqs.com/ddi_code_snippets/select_pandas_dataframe_rows_between_two_dates
date_filter1 = (df_tempact['Start Date'] <= data_cutoff)
df_tempact = df_tempact.loc[date_filter1]
total_TAs = len(df_tempact)
print("")
print("Similarly, based on this data cutoff date, you should have " + str(total_TAs) + " total TAs included in this dataset. Is that correct?  y/n")
print("")
if input() == "y":
	print("")
	print ("LET'S DO THIS THEN")
else:
	print("")
	print ("Something has gone terribly wrong. Terminating program.")
	sys.exit("Closed.")
print("")
print("Here are some checks along the way so you can feel better about the data remaining intact:")
print("")




####################################
###### RO SECTION ############
####################################

####################################
# Country/Region of Origin of NGOs with Registered Representative Offices
# making a new column in the df that removes any place-specific references from RO names
df_repoff['repoff_name'] = df_repoff['Organization Name (English)'].str.split("(", expand = True)[0]
# getting the # of orgs from each country, first sorting countries alphabetically so it comes out all nice and pretty
df_repoff.sort_values('Organization Origin')
df_ro_origins = df_repoff.rename(columns={'Organization Origin': 'country'})
# grouping and then renaming the resulting new column https://stackoverflow.com/a/40872584/7841877
origins = df_ro_origins.groupby('country').size().to_frame('offices')
#print(origins)
#https://www.humblix.com/k9cBG3/how-to-save-a-dataframe-in-a-tabulation-delimited-file-tsv-in-python
origins.to_csv('outputs/ROorigin.tsv', sep = '\t')
origins.to_csv('archive/'+ input_date + '_ROorigin.tsv', sep = '\t')
print ("RO x country of origin total: " + str(origins.offices.sum()))
print("")

####################################
# Number of Representative Offices Registered in Each Province
# getting the # of orgs registered in each province, first sorting provinces alphabetically so it comes out all nice and pretty
df_repoff.sort_values('Registration Location')
#making the tsv for the bar chart
df_ro_regloc = df_repoff.rename(columns={'Registration Location': 'Province'})
reg_locs = df_ro_regloc.groupby('Province').size().to_frame('offices')
reg_locs.to_csv('outputs/ROprov.tsv', sep = '\t')
reg_locs.to_csv('archive/'+ input_date + '_ROprov.tsv', sep = '\t')
#making the tsv for the choropleth
df_ro_regloc_map = df_repoff.rename(columns={'Registration Location': 'name'})
reg_locs1 = df_ro_regloc_map.groupby('name').size().to_frame('total')
reg_locs1.to_csv('outputs/RObyprovChoro.tsv', sep = '\t')
print ("RO x provincial registrations: " + str(reg_locs.offices.sum()))
print("")

####################################
# Number of Representative Offices Permitted to Work in Each Province
# getting the # of orgs permitted to work in each province
work_provs = (df_repoff[['Anhui', 'Beijing', 'Chongqing', 'Fujian', 'Gansu', 'Guangdong', 'Guangxi', 'Guizhou', 'Hainan', 'Hebei', 'Heilongjiang', 'Henan', 'Hubei', 'Hunan', 'Inner Mongolia', 'Jiangsu', 'Jiangxi', 'Jilin', 'Liaoning', 'Ningxia', 'Qinghai', 'Shaanxi', 'Shandong', 'Shanghai', 'Shanxi', 'Sichuan', 'Tianjin', 'Tibet', 'Xinjiang', 'Xinjiang Bingtuan', 'Yunnan', 'Zhejiang']])
# making the tsv for the bar chart
# https://www.geeksforgeeks.org/python-pandas-dataframe-sum/
# https://stackoverflow.com/a/37084889/7841877
orgs_per_work_prov = work_provs.sum(axis = 0, skipna = True).astype(int).to_frame('offices').reset_index()
orgs_per_work_prov.rename(columns={"index": "Province"}, inplace = True)
orgs_per_work_prov.set_index("Province", inplace = True)
orgs_per_work_prov.to_csv('outputs/RObyAOO.tsv', sep = '\t')
orgs_per_work_prov.to_csv('archive/'+ input_date + '_RObyAOO.tsv', sep = '\t')
# making the tsv for the choropleth
orgs_per_work_prov1 = work_provs.sum(axis = 0, skipna = True).astype(int).to_frame('total').reset_index()
orgs_per_work_prov1.rename(columns={"index": "name"}, inplace = True)
orgs_per_work_prov1.set_index("name", inplace = True)
orgs_per_work_prov1.to_csv('outputs/RObyAOOchoro.tsv', sep = '\t')
#print(orgs_per_work_prov1)


####################################
# Number of Representative Offices Engaged in Certain Fields of Work
# getting the # of orgs working in each sector
sectors = (df_repoff[['Aging', 'Agriculture', 'Animal Protection', 'Arts and Culture', 'Civil Soc\'y Cap\'y building', 'Disabilities', 'Disaster Relief', 'Econ. Development', 'Education', 'Energy', 'Environment', 'Ethnic Affairs', 'Gender Issues', 'Health', 'Human Rights', 'Infrastructure', 'Int\'l Relations/Exchange', 'Labor', 'Law and Governance', 'LGBTQ Issues', 'Media', 'Migrants', 'Poverty Alleviation', 'Religion', 'Rural Issues/Devt', 'Sport', 'Technology', 'Tourism', 'Trade', 'Urban Issues/Devt', 'Youth']])
orgs_per_sector = sectors.sum(axis = 0, skipna = True).astype(int).to_frame('offices').reset_index()
orgs_per_sector.rename(columns={"index": "sector"}, inplace = True)
orgs_per_sector.set_index("sector", inplace = True)
orgs_per_sector.rename(index={'Civil Soc\'y Cap\'y building': "Capacity-Building", 'Int\'l Relations/Exchange': "International Relations", 'Rural Issues/Devt': "Rural Issues", 'Urban Issues/Devt': "Urban Issues"}, inplace=True)
#print(orgs_per_sector)
orgs_per_sector.to_csv('outputs/ROsector.tsv', sep = '\t')
orgs_per_sector.to_csv('archive/'+ input_date + '_ROsector.tsv', sep = '\t')


####################################
# Number of Representative Offices Registered per Month
# getting # of orgs registered each month https://stackoverflow.com/a/46624663/7841877
reg_month = df_repoff['Date of Registration'].groupby(df_repoff['Date of Registration'].dt.to_period("M")).agg('count')
#print(reg_month)
export_csv = reg_month.to_csv ('collateral/reg_month.csv', header=True)
list = []
with open('collateral/reg_month.csv', 'r') as file_in:
	reader = csv.reader(file_in)
	next(reader)
	for row in reader:
		date_format1 = datetime.strptime(row[0], '%Y-%m')
		row[0] = datetime.strftime(date_format1, '%B %Y')
		list.append(row)
#print(list)
# https://riptutorial.com/python/example/26946/writing-a-tsv-file
with open('outputs/ROregdate.tsv', 'w') as out_file:
	tsv_writer = csv.writer(out_file, delimiter='\t')
	tsv_writer.writerow(['week', 'number'])
	for l in list:
		tsv_writer.writerow(l)
with open('archive/'+ input_date + '_ROregdate.tsv', 'w') as out_file:
	tsv_writer = csv.writer(out_file, delimiter='\t')
	tsv_writer.writerow(['week', 'number'])
	for l in list:
		tsv_writer.writerow(l)


####################################
# Number of Representative Offices per Foreign NGO
# this gets the number of all organizations having 1 repoff, 2 repoffs, etc.
unique_repoffs = df_repoff.groupby('repoff_name').size().value_counts().to_frame('number').reset_index()
unique_repoffs.sort_values('index', inplace = True)
unique_repoffs.rename(columns={'index': 'offices'}, inplace=True)
unique_repoffs.set_index("offices", inplace = True)
#print (unique_repoffs)
unique_repoffs.to_csv('outputs/ROmultoffices.tsv', sep = '\t')
unique_repoffs.to_csv('archive/'+ input_date + '_ROmultoffices.tsv', sep = '\t')





####################################
###### TA SECTION ############
####################################

####################################
# Country/Region of Origin of Foreign NGOs Carrying out Temporary Activities
# getting the # of orgs from each country, first sorting countries alphabetically so it comes out all nice and pretty
df_tempact.sort_values('Organization Origin')
df_ta_origin = df_tempact.rename(columns={'Organization Origin': 'country'})
origins1 = df_ta_origin.groupby('country').size().to_frame('activities')
#print(origins)
origins1.to_csv('outputs/TAorigin.tsv', sep = '\t')
origins1.to_csv('archive/'+ input_date + '_TAorigin.tsv', sep = '\t')
print ("TA x country of origin: " + str(origins1.activities.sum()))
print("")


####################################
# Number of Temporary Activities Held in Each Province
# getting the # of TAs in each province
TA_provs = (df_tempact[['All of China', 'Anhui', 'Beijing', 'Chongqing', 'Fujian', 'Gansu', 'Guangdong', 'Guangxi', 'Guizhou', 'Hainan', 'Hebei', 'Heilongjiang', 'Henan', 'Hubei', 'Hunan', 'Inner Mongolia', 'Jiangsu', 'Jiangxi', 'Jilin', 'Liaoning', 'Ningxia', 'Qinghai', 'Shaanxi', 'Shandong', 'Shanghai', 'Shanxi', 'Sichuan', 'Tianjin', 'Tibet', 'Xinjiang', 'Xinjiang Bingtuan', 'Yunnan', 'Zhejiang', 'Location Unknown']])
#df_work_provs = df_repoff.loc[work_provs]
# https://www.geeksforgeeks.org/python-pandas-dataframe-sum/
TAs_per_prov = TA_provs.sum(axis = 0, skipna = True).astype(int).to_frame('activities').reset_index()
#making the tsv for the bar chart
TAs_prov_bar = TAs_per_prov.rename(columns={"index": "Province"})
TAs_prov_bar.set_index("Province", inplace = True)
TAs_prov_bar.to_csv('outputs/TAprovince.tsv', sep = '\t')
TAs_prov_bar.to_csv('archive/'+ input_date + '_TAprovince.tsv', sep = '\t')
#making the tsv for the choropleth
TAs_prov_map = TAs_per_prov.rename(columns={"index": "name", "activities":"total"})
TAs_prov_map.set_index("name", inplace = True)
#print(TAs_prov_map)
TAs_prov_map.to_csv('outputs/TAbyprovChoro.tsv', sep = '\t')


####################################
# Number of Temporary Activities in Certain Fields of Work
# getting the # of orgs working in each sector
TA_sectors = (df_tempact[['Aging', 'Agriculture', 'Animal Protection', 'Arts and Culture', 'Civil Society Capacity Building', 'Disabilities', 'Disaster Relief', 'Economic Development', 'Education', 'Energy', 'Environment', 'Ethnic Affairs', 'Gender Issues', 'Health', 'Human Rights', 'Infrastructure', 'International Relations/Exchange', 'Labor', 'Law and Governance', 'LGBTQ Issues', 'Media', 'Migrants', 'Poverty Alleviation', 'Religion', 'Rural Issues/Development', 'Sport', 'Technology', 'Tourism', 'Trade', 'Urban Issues/Development', 'Youth', 'Field Unknown']])
TAs_per_sector = TA_sectors.sum(axis = 0, skipna = True).astype(int).to_frame('activities').reset_index()
TAs_per_sector.rename(columns={"index": "sector"}, inplace = True)
TAs_per_sector.set_index("sector", inplace = True)
TAs_per_sector.rename(index={'Civil Society Capacity Building': "Capacity-Building", 'International Relations/Exchange': "International Relations", 'Rural Issues/Development': "Rural Issues", 'Urban Issues/Development': "Urban Issues"}, inplace=True)
#print(TAs_per_sector)
TAs_per_sector.to_csv('outputs/TAsector.tsv', sep = '\t')
TAs_per_sector.to_csv('archive/'+ input_date + '_TAsector.tsv', sep = '\t')


####################################
# Lengths of Temporary Activities, in Months
# getting the lengths of TAs in months, first combining 11 and 12 "months" https://stackoverflow.com/a/31888920/7841877
df_tempact['Length in months'].replace(12, 11, inplace=True)
df_ta_month = df_tempact.rename(columns={"Length in months": "length"})
monthlength = df_ta_month.groupby('length').size().to_frame('number')
# have to rename the indexes to be ready for the data viz, but have to do it AFTER the groupby so it doesn't re-order them alphabetically   https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.rename.html
monthlength.rename(index={0: "0-1 Month", 1: "1-2 Months", 2: "2-3 Months", 3: "3-4 Months", 4: "4-5 Months", 5: "5-6 Months", 6: "6-7 Months", 7: "7-8 Months", 8: "8-9 Months", 9: "9-10 Months", 10: "10-11 Months", 11: "11-12 Months"}, inplace=True)
#print(monthlength)
monthlength.to_csv('outputs/TAlengthmonth.tsv', sep = '\t')
monthlength.to_csv('archive/'+ input_date + '_TAlengthmonth.tsv', sep = '\t')
print ("TA x lengths of activities: " + str(monthlength.number.sum()))
print("")

####################################
# Lengths of Temporary Activities Lasting Less than One Month
# getting the lengths of TAs in days, first filtering out any activities over a month long
df_ta_day = df_tempact.rename(columns={"Length in days": "length"})
day_filter = (df_ta_day['length'] <= 30)
daylength = df_ta_day.loc[day_filter].groupby('length').size().to_frame('number')
# have to rename the indexes to be ready for the data viz  https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.rename.html
daylength.rename(index={0: "1 Day", 1: "2 Days", 2: "3 Days", 3: "4 Days", 4: "5 Days", 5: "6 Days", 6: "7 Days", 7: "8 Days", 8: "9 Days", 9: "10 Days", 10: "11 Days", 11: "12 Days", 12: "13 Days", 13: "14 Days", 14: "15 Days", 15: "16 Days", 16: "17 Days", 17: "18 Days", 18: "19 Days", 19: "20 Days", 20: "21 Days", 21: "22 Days", 22: "23 Days", 23: "24 Days", 24: "25 Days", 25: "26 Days", 26: "27 Days", 27: "28 Days", 28: "29 Days", 29: "30 Days", 30: "31 Days"}, inplace=True)
#print(daylength)
daylength.to_csv('outputs/TAlengthday.tsv', sep = '\t')
daylength.to_csv('archive/'+ input_date + '_TAlengthday.tsv', sep = '\t')


####################################
# Number of Temporary Activities Initiated per Month
# getting # of TAs initiated each month https://stackoverflow.com/a/46624663/7841877
df_ta_start = df_tempact.rename(columns={"Start Date": "week"})
TA_month = df_ta_start['week'].groupby(df_ta_start['week'].dt.to_period("M")).agg('count').to_frame('number')
#print(TA_month)
export_csv1 = TA_month.to_csv ('collateral/TA_month.csv', header=True)
list = []
with open('collateral/TA_month.csv', 'r') as file_in:
	reader = csv.reader(file_in)
	next(reader)
	for row in reader:
		date_format1 = datetime.strptime(row[0], '%Y-%m')
		row[0] = datetime.strftime(date_format1, '%B %Y')
		list.append(row)
#print(list)
# https://riptutorial.com/python/example/26946/writing-a-tsv-file
with open('outputs/TAstartdate.tsv', 'w') as out_file:
	tsv_writer = csv.writer(out_file, delimiter='\t')
	tsv_writer.writerow(['week', 'number'])
	for l in list:
		tsv_writer.writerow(l)
with open('archive/'+ input_date + '_TAstartdate.tsv', 'w') as out_file:
	tsv_writer = csv.writer(out_file, delimiter='\t')
	tsv_writer.writerow(['week', 'number'])
	for l in list:
		tsv_writer.writerow(l)
print ("TA x start date: " + str(TA_month.number.sum()))
print("")


####################################
# Number of Temporary Activities per Foreign NGO
# this gets the number of TAs per NGO
num_TAs = df_tempact.groupby('Organization Name (English)').size().value_counts().reset_index()
#print (num_TAs)
num_TAs.rename(columns={"index": "activities", 0: "number"}, inplace = True)
# finding largest # of activities for one org, to use later when building the bar chart
max_num = num_TAs["activities"].max()
num_TAs["activities"].replace([6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,90,91,92,93,94,95,96,97,98,99,100,max_num],['6-10','6-10','6-10','6-10','6-10','11-20','11-20','11-20','11-20','11-20','11-20','11-20','11-20','11-20','11-20','21-30','21-30','21-30','21-30','21-30','21-30','21-30','21-30','21-30','21-30','31-40','31-40','31-40','31-40','31-40','31-40','31-40','31-40','31-40','31-40','41-100','41-100','41-100','41-100','41-100','41-100','41-100','41-100','41-100','41-100','41-100','41-100','41-100','41-100','41-100','41-100','41-100','41-100','41-100','41-100','41-100','41-100','41-100','41-100','41-100','41-100','41-100','41-100','41-100','41-100','41-100','41-100','41-100','41-100','41-100','41-100','41-100','41-100','41-100','41-100','41-100','41-100','41-100','41-100','41-100','41-100','41-100','41-100','41-100','41-100','41-100','41-100','41-100','41-100','41-100','41-100','41-100','41-100','41-100','41-100','101+'], inplace=True)
#print (num_TAs)
#https://www.shanelynn.ie/summarising-aggregation-and-grouping-data-in-python-pandas/
test = num_TAs.groupby("activities").agg({"number": "sum"})
# https://stackoverflow.com/a/30010004/7841877
test1 = test.reindex([1,2,3,4,5,'6-10','11-20','21-30','41-100','101+'])
#print (test1)
test1.to_csv('outputs/TAmultact.tsv', sep = '\t')
test1.to_csv('archive/'+ input_date + '_TAmultact.tsv', sep = '\t')


print(". . . done making tsvs for Github and for archive. Now updating html files . . .")
print("")




####################################
###### HTML SECTION ############
####################################

fin = open("html_inputs/ROorigin_input.html", "rt")
fout = open("outputs/ROorigin.html", "wt")
for line in fin:
	fout.write(line.replace('H1_DATE', h1_date))
fin.close()
fout.close()

fin = open("html_inputs/ROprov_input.html", "rt")
fout = open("outputs/ROprov.html", "wt")
for line in fin:
	fout.write(line.replace('H1_DATE', h1_date))
fin.close()
fout.close()

fin = open("html_inputs/RObyprovchoro_input.html", "rt")
fout = open("outputs/RObyprovchoro.html", "wt")
for line in fin:
	fout.write(line.replace('H1_DATE', h1_date))
fin.close()
fout.close()

fin = open("html_inputs/RObyAOO_input.html", "rt")
fout = open("outputs/RObyAOO.html", "wt")
for line in fin:
	fout.write(line.replace('H1_DATE', h1_date))
fin.close()
fout.close()

fin = open("html_inputs/RObyAOOchoro_input.html", "rt")
fout = open("outputs/RObyAOOchoro.html", "wt")
for line in fin:
	fout.write(line.replace('H1_DATE', h1_date).replace('FOOTNOTE_DATE', footnote_date))
fin.close()
fout.close()

fin = open("html_inputs/ROsector_input.html", "rt")
fout = open("outputs/ROsector.html", "wt")
for line in fin:
	fout.write(line.replace('H1_DATE', h1_date))
fin.close()
fout.close()

fin = open("html_inputs/ROregdate_input.html", "rt")
fout = open("outputs/ROregdate.html", "wt")
for line in fin:
	fout.write(line.replace('H1_DATE', h1_date))
fin.close()
fout.close()

fin = open("html_inputs/ROmultoffices_input.html", "rt")
fout = open("outputs/ROmultoffices.html", "wt")
for line in fin:
	fout.write(line.replace('H1_DATE', h1_date))
fin.close()
fout.close()

fin = open("html_inputs/TAorigin_input.html", "rt")
fout = open("outputs/TAorigin.html", "wt")
for line in fin:
	fout.write(line.replace('H1_DATE', h1_date).replace('FOOTNOTE_DATE', footnote_date))
fin.close()
fout.close()

fin = open("html_inputs/TAprovince_input.html", "rt")
fout = open("outputs/TAprovince.html", "wt")
for line in fin:
	fout.write(line.replace('H1_DATE', h1_date).replace('FOOTNOTE_DATE', footnote_date))
fin.close()
fout.close()

fin = open("html_inputs/TAchoro_input.html", "rt")
fout = open("outputs/TAchoro.html", "wt")
for line in fin:
	fout.write(line.replace('H1_DATE', h1_date).replace('FOOTNOTE_DATE', footnote_date))
fin.close()
fout.close()

fin = open("html_inputs/TAsector_input.html", "rt")
fout = open("outputs/TAsector.html", "wt")
for line in fin:
	fout.write(line.replace('H1_DATE', h1_date).replace('FOOTNOTE_DATE', footnote_date))
fin.close()
fout.close()

fin = open("html_inputs/TAlengthmonth_input.html", "rt")
fout = open("outputs/TAlengthmonth.html", "wt")
for line in fin:
	fout.write(line.replace('H1_DATE', h1_date).replace('FOOTNOTE_DATE', footnote_date))
fin.close()
fout.close()

fin = open("html_inputs/TAlengthday_input.html", "rt")
fout = open("outputs/TAlengthday.html", "wt")
for line in fin:
	fout.write(line.replace('H1_DATE', h1_date).replace('FOOTNOTE_DATE', footnote_date))
fin.close()
fout.close()

fin = open("html_inputs/TAstartdate_input.html", "rt")
fout = open("outputs/TAstartdate.html", "wt")
for line in fin:
	fout.write(line.replace('H1_DATE', h1_date))
fin.close()
fout.close()

fin = open("html_inputs/TAmultact_input.html", "rt")
fout = open("outputs/TAmultact.html", "wt")
for line in fin:
	fout.write(line.replace('H1_DATE', h1_date))
fin.close()
fout.close()


print(". . . aaaaand everything should be done.")
print("")
print("Don't forget: when uploading to Github, do the tsvs in one traunch first, wait a little bit, and then do the htmls.")
print("")
