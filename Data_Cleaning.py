import pandas as pd
import json
import numpy as np
import os
from tqdm import tqdm
from tabulate import tabulate
import random
import matplotlib.pyplot as plt
from urllib.request import urlopen

def search(x,array):
    for i in array:
        if i==x:
            return True
        return False
    
def fixer(array):
    new_dic = {key: [] for key in array[0].keys()}
    for dic in array:
        for key in dic.keys():
            new_dic[key].append(dic[key])
    return new_dic

def disambiguation(data):
    new_data = []
    for author in tqdm(data):
        Add = True
        for id in non_singular_ids:
            if id == author["id"]:
                Add = False
        if Add:
            new_data.append(author)
    return new_data

non_singular_ids = ['https://openalex.org/A5026885152',
 'https://openalex.org/A5011515634',
 'https://openalex.org/A5007423881',
 'https://openalex.org/A5017341592',
 'https://openalex.org/A5078640076',
 'https://openalex.org/A5029730097',
 'https://openalex.org/A5013301721',
 'https://openalex.org/A5069649653',
 'https://openalex.org/A5037250488',
 'https://openalex.org/A5019673689',
 'https://openalex.org/A5073935513',
 'https://openalex.org/A5062411161',
 'https://openalex.org/A5064415452',
 'https://openalex.org/A5000850500',
 'https://openalex.org/A5019934270',
 'https://openalex.org/A5032044327',
 'https://openalex.org/A5043408742',
 'https://openalex.org/A5054911388',
 'https://openalex.org/A5026188012',
 'https://openalex.org/A5015146406',
 'https://openalex.org/A5069870244',
 'https://openalex.org/A5084656904',
 'https://openalex.org/A5014524737',
 'https://openalex.org/A5026191520',
 'https://openalex.org/A5026418075',
 'https://openalex.org/A5079456301',
 'https://openalex.org/A5089629100',
 'https://openalex.org/A5004863476',
 'https://openalex.org/A5053330477']

path = "C:\\Users\\ACER\\Downloads\\Telegram Desktop\\results\\authors"
file_list = os.listdir(path="C:\\Users\\ACER\\Downloads\\Telegram Desktop\\results\\authors")
combined_counts_by_year = []
data = {"results": []}

print(f"Collecting Files")
for file in tqdm(file_list):
    f = open(path + "\\" + file, encoding='utf8')
    singular_data = json.load(f)
    for author_data in singular_data["results"]:
        if len(author_data['counts_by_year']) != 0:
            data["results"].append(author_data)
    f.close()
    
necessary_keys = ['id', 'orcid', 'display_name', 'works_count', 'cited_by_count','created_date','works_api_url']
Authors = {key : [] for key in necessary_keys}
Authors["No of Alternative Names"],Authors["H-index"] = [],[]
print(f"\n Creating a dataframe")
for author in tqdm(data["results"]):
    for key in necessary_keys:
        Authors[key].append(author[key])
    Authors["No of Alternative Names"].append(len(author['display_name_alternatives']))
    Authors["H-index"].append(author['summary_stats']['h_index'])
df = pd.DataFrame(Authors)

#Works_Year = {author["id"]: fixer(author["counts_by_year"]) for author in new_data["results"]}
combined_details = ['display_name','type','country_code','works_count','cited_by_count']
details = ['display_name','type','country_code']
print("Creating a dictionary to store the data")
Stats = {author["id"]: {year: {detail: [] for detail in combined_details} for year in fixer(author["counts_by_year"])["year"]} for author in tqdm(new_data["results"])}
details = ['display_name','type','country_code']
#print(Stats)
print("Appending to stored dictionary")
for author in tqdm(new_data["results"]):
    #works = fixer(author["counts_by_year"])
    #print(Stats[author["id"]].keys())
    for affiliation in author["affiliations"]:
        #print(affiliation["years"])
        for i in range(len(affiliation['years'])):
            if not(search(x= affiliation['years'][i],array=list(Stats[author["id"]].keys()))):
                Stats[author['id']][affiliation['years'][i]] = ({detail: [] for detail in combined_details})
                for detail in details:
                    Stats[author["id"]][affiliation['years'][i]][detail].append(affiliation["institution"][detail])
            else:
                for detail in details:
                    Stats[author["id"]][affiliation['years'][i]][detail].append(affiliation["institution"][detail])
    #print(author)
    for year_record in author["counts_by_year"]:
        #print(author['id'])
        #print(year_record['year'])
        Stats[author['id']][year_record["year"]]['works_count'].append(year_record['works_count'])
        Stats[author['id']][year_record["year"]]['cited_by_count'].append(year_record['cited_by_count'])
#print(Stats["https://id.org/0000-0001-5751-5396"])
#print(Works_Year["https://id.org/0000-0001-5751-5396"])
with open("Stats.txt", "w") as fp:
    json.dump(Stats, fp)  # encode dict into JSON
print("Done writing dict into .txt file")

necessary_keys = ['id', 'orcid', 'display_name', 'works_count', 'cited_by_count','created_date',"works_api_url"]
Authors = {key : [] for key in necessary_keys}
Authors["No of Alternative Names"],Authors["H-index"] = [],[]
print(f"\n Creating a dataframe")
for author in tqdm(new_data["results"]):
    for key in necessary_keys:
        Authors[key].append(author[key])
    Authors["No of Alternative Names"].append(len(author['display_name_alternatives']))
    Authors["H-index"].append(author['summary_stats']['h_index'])
df_new = pd.DataFrame(Authors)
df_new.to_csv("Author_Details.csv")