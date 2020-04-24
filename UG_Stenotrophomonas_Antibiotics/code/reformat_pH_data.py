#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 23 20:32:19 2019

@author: Tara
"""
import os
import os.path
import pandas as pd
import argparse
import re
import datetime

#file_name = "/Volumes/GoogleDrive/My Drive/UG_Stenotrophomonas_Antibiotics/data/raw/miranda_CV2008_lexofloxacin_48hr_chamber_091919.txt"
input_path =input('Enter directory path with raw files: ')
output_path=input_path
now = str(datetime.datetime.now())
date=now.split(' ')[0]

directory=os.listdir(input_path)
os.chdir(input_path)

rx_dict = { 
        'MIC8x': re.compile(r'B\t(.*)\t600'),
        'MIC4x': re.compile(r'C\t(.*)\t600'),
        'MIC2x': re.compile(r'D\t(.*)\t600'),
        'MIC1x': re.compile(r'E\t(.*)\t600'),
        'MIC0.5x': re.compile(r'F\t(.*)\t600'),
        'MIC0x': re.compile(r'G\t(.*)\t600'),
        }

def _parse_line(line):
    """
    Do a regex search against all defined regexes and
    return the key and match result of the first matching regex

    """

    for key, rx in rx_dict.items():
        match = rx.search(line)
        if match:
            return key, match
    # if there are no matches
    return None, None

correct_version = ('\n\nSoftware Version\t2.09.1\n')


df_final=pd.DataFrame([], columns=["OD", "ConcFormat", "pH", "Concentration"])
df_all=pd.DataFrame([], columns=["OD", "ConcFormat", "pH", "Concentration", "Person", "Strain", "Antibiotic", "Incubation","Oxygen", "ExperimentDate"])


for file in directory:
    if file.find('.txt') !=-1 & file.find('.pda')==-1:
        file_name=file
        with open(file_name ,'r') as f:
            if correct_version in f.read():
                print("Re-formatting file " + file_name)
            else:
                print(file_name + " This code is compatible with Gen5 version 2.09.1, which is different than your file version. Still re-formatting file, but please double check output format.")
        with open(file_name, 'r') as f:
            line=f.readline()
            df_final=pd.DataFrame([], columns=["OD", "ConcFormat", "pH", "Concentration"])
            file_name_short = file_name.split('/')[-1].split('.txt')[0].split('_')
            predet_mic = float(file_name_short[len(file_name_short)-1])
            while line:
                key,match = _parse_line(line)
               # print(key, match)
                if match!=None:
                    MIC_x_step0 = match[0]
                    MIC_x_entry = MIC_x_step0.split('\t')[2:11]
                    df_od = pd.DataFrame(MIC_x_entry, columns=['OD'])
                    df_MIC = pd.DataFrame([item for item in [key] for i in range(9)], columns=['ConcFormat'])
                    df_pH = pd.DataFrame(["pH5", "pH5", "pH5", "pH7", "pH7", "pH7", "pH9", "pH9", "pH9"], columns=["pH"])
                    df_step0=df_od.join(df_MIC)
                    df_step1=df_step0.join(df_pH)
                    actual_conc = str(float(key.split('MIC')[1].split('x')[0])*predet_mic)
                    actual_conc_df = pd.DataFrame([item for item in [actual_conc] for i in range(9)], columns=['Concentration'])
                    df_step2 = df_step1.join(actual_conc_df)
                    df_final = df_final.append(df_step2)
                line=f.readline()
                
            Person = pd.DataFrame([item for item in [file_name_short[0]] for i in range(9)], columns=["Person"])
            Strain = pd.DataFrame([item for item in [file_name_short[1]] for i in range(9)], columns=["Strain"])
            Antibiotic = pd.DataFrame([item for item in [file_name_short[2]] for i in range(9)], columns=["Antibiotic"])
            Incubation = pd.DataFrame([item for item in [file_name_short[3]] for i in range(9)], columns=["Incubation"])
            Oxygen = pd.DataFrame([item for item in [file_name_short[4]] for i in range(9)], columns=["Oxygen"])
            ExperimentDate = pd.DataFrame([item for item in [file_name_short[5]] for i in range(9)], columns=["ExperimentDate"])
            MIC=pd.DataFrame([item for item in [file_name_short[6]] for i in range(9)], columns=["PredetMIC"])
            
            df_final = df_final.join(Person)
            df_final = df_final.join(Strain)
            df_final = df_final.join(Incubation)
            df_final = df_final.join(Antibiotic)
            df_final = df_final.join(Oxygen)
            df_final = df_final.join(ExperimentDate)
            df_final = df_final.join(MIC)
            
            output_file_name=str(output_path)+str(file_name.split('/')[-1].split('.txt')[0]) + str("_REFORMATED")+str(".csv")
            j
            df_final.to_csv(output_file_name)
    
            f.close()
           
        df_all=df_all.append(df_final)


df_all.to_csv(output_path+str('ALLdata.csv'))
print("\n the combined, reformatted data file is named ALLdata.csv and located in the same input directory")


