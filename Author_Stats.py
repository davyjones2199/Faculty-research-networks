import pandas as pd
import json
import numpy as np
import os
from tqdm import tqdm
from tabulate import tabulate
import random
import matplotlib.pyplot as plt
from urllib.request import urlopen

class Author_Stats():
    def __init__(self,df,Stats):
        self.df = df
        self.Stats = Stats
        pass 
    def Show_Data(self,Open_Alex_ID):
        print(self.df[self.df["id"] == Open_Alex_ID])
        
    def List_Names(self):
        for i in range(len(self.df)):
            print(f"{self.df["id"][i]} : {self.df["display_name"][i]}")
    
    def Describe(self,Open_Alex_ID,return_=False):
        Years_with_multiple_institutes = []
        Years = []
        Institute = []
        No_of_works = []
        Citations = []
        Type = []
        
        person = self.df[self.df["id"] == Open_Alex_ID]
        print(f"Name : {np.array(person["display_name"])[0]}\nH-index : {np.array(person["H-index"])[0]}\nNo of works : {np.array(person["works_count"])[0]}\nCitations : {np.array(person["cited_by_count"])[0]}\n")
        for year in sorted(list(self.Stats[Open_Alex_ID].keys())):
            flag = False
            #print(f"Year : {year} Institute: {self.Stats[Open_Alex_ID][year]["display_name"]} Country: {self.Stats[Open_Alex_ID][year]["country_code"]} No. of works published : {self.Stats[Open_Alex_ID][year]["works_count"]} Citations : {self.Stats[Open_Alex_ID][year]["cited_by_count"]}")
            if len(self.Stats[Open_Alex_ID][year]["display_name"]) == 1 and len(self.Stats[Open_Alex_ID][year]["works_count"]) >0 :
                Years.append(year),Institute.append(self.Stats[Open_Alex_ID][year]["display_name"][0]),No_of_works.append(self.Stats[Open_Alex_ID][year]["works_count"][0]),Citations.append(self.Stats[Open_Alex_ID][year]["cited_by_count"][0]),Type.append(self.Stats[Open_Alex_ID][year]["type"][0])
            elif len(self.Stats[Open_Alex_ID][year]["display_name"]) == 1 and len(self.Stats[Open_Alex_ID][year]["works_count"]) ==0:
                Years.append(year),Institute.append(self.Stats[Open_Alex_ID][year]["display_name"][0]),No_of_works.append("Unknown"),Citations.append(("Unknown")),Type.append(self.Stats[Open_Alex_ID][year]["type"][0])
            elif len(self.Stats[Open_Alex_ID][year]["display_name"]) > 1:
                flag = True
                Years_with_multiple_institutes.append(year)
        person_dataframe = pd.DataFrame({"Years": Years, "Institute": Institute, "No of Works": No_of_works, "Citations": Citations, "Type": Type})
        print(tabulate(person_dataframe, headers = 'keys', tablefmt='psql'))
        if flag:
            for year in Years_with_multiple_institutes:
                print(f"The {len(self.Stats[Open_Alex_ID][year]["display_name"])} Institutes affiliated with in {year} are: ")
                for i in range(len(self.Stats[Open_Alex_ID][year]["display_name"])):
                    print(f"{i+1} : {self.Stats[Open_Alex_ID][year]["display_name"][i]} : {self.Stats[Open_Alex_ID][year]["type"][i]}")
                if len(self.Stats[Open_Alex_ID][year]["works_count"])>0:
                    print(f"No of works published in {year} are {self.Stats[Open_Alex_ID][year]["works_count"][0]}")
                    print(f"No of citations attained in {year} are {self.Stats[Open_Alex_ID][year]["cited_by_count"][0]}")
                else:
                    print(f"No of works published in {year} are unknown")
                    print(f"No of citations attained in {year} are unknown")
        print("\n-------------------------------------------------------\n")
        if return_:
            return Institute,Years
    
    def visualize(self,Open_Alex_ID):
        Institute,Years = self.Describe(Open_Alex_ID,return_=True)
        plt.figure(figsize=(20,10))
        plt.plot(Years,Institute,"-o",color = 'red')
        plt.xlabel("Years")
        plt.ylabel("Institute")
        #plt.show()
        
    def Get_Works(self,Open_Alex_ID,return_ = False, Show_Paper_names = True):
        work_count = np.array(self.df["works_count"][self.df['id']==Open_Alex_ID])[0]
        url = 'https://api.openalex.org/works?per-page='+ str(work_count) +'&sort=publication_year&filter=author.id:' + Open_Alex_ID[21:]
        #print(url)
        Papers = []
        with urlopen(url) as URL:
            papers = json.load(URL)
        for paper in papers['results']:
            Papers.append(paper)
        if papers['meta']['count'] > work_count:
            for i in range(int(np.floor(papers['meta']['count'])/work_count)):
                new_url = url + '&page=' + str(i+2)
                with urlopen(new_url) as URL:
                    papers = json.load(URL)
                    for paper in papers['results']:
                        Papers.append(paper)
        print(f"Name : {np.array(self.df['display_name'][self.df["id"]==Open_Alex_ID])[0]}")
        print(f"H-Index : {np.array(self.df["H-index"][self.df["id"]==Open_Alex_ID])[0]}")
        print(f"Open ALex ID: {Open_Alex_ID}\n------------------------------------------------------------------------------------------")
        if Show_Paper_names:
            i=1
            for paper in Papers:
                print(f"{i} - Title : {paper['display_name']}\nPublication Date : {paper["publication_date"]}\nPaper_Id: {paper['id']}\nNo of citations: {np.sum([year["cited_by_count"] for year in paper['counts_by_year']])}\n ")
                i += 1
        if return_ :
            return Papers