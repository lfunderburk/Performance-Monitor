#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 22 10:41:19 2021

@author: laura.gf
"""

import pandas as pd
import os
import argparse
import plotly.io as pio
import plotly.express as px

def plot_uk_intensity(df,name):
    """


    Parameters
    ----------
    df :  DATAFRAME OBJECT
        Contains data with performance test results.
    name : STRING
        Name of file.

    Returns
    -------
    None.

    """
    
    # Create 
    full_fig  = px.line(df,
               y="query.lasted",
               x="Date/Time",
               title="Time taken per query",
               facet_col="query.type",
               labels={'query.lasted':"Time taken (s)"},
               hover_name="query.type",
               color_discrete_sequence=px.colors.qualitative.Safe,
               color='query.type')
    name_plot = ("_").join(["AllQueries",name,"hourly_performance.html"])
    pio.write_html(full_fig,name_plot,
                  auto_open=False)
    
    box_fig = px.box(df, x='query.type',
                     y='query.lasted',
                     title="Boxplot time taken per type of query",
                     hover_name="Date/Time",
                     labels={'query.lasted':"Time taken (s)",
                             'query.type':"Type of query"},
                     color_discrete_sequence=px.colors.qualitative.Safe,
                     color='query.type')
    name_plot2 = ("_").join(["AllQueries",name,"boxplot.html"])
    pio.write_html(box_fig,name_plot2,
                  auto_open=False)


def plot_performance(df,name):
    """
    

    Parameters
    ----------
    df :  DATAFRAME OBJECT
        Contains data with performance test results.
    name : STRING
        Name of file.

    Returns
    -------
    None.

    """
    try:
        full_fig  = px.line(df,
               y="query.lasted",
               x="Date/Time",
               facet_col="query.type",
               color='query.name',
               title="Time taken per query",
               hover_name="query.name",
               labels={"query.lasted": "Time (s)"})
        pio.write_html(full_fig,str(name) + "_hourly_performance.html",
                  auto_open=False)
        
        box_fig = px.box(df, x='query.type',
                     y='query.lasted',
                     title="Boxplot time taken per type of query",
                     hover_name="Date/Time",
                     labels={'query.lasted':"Time taken (s)",
                             'query.type':"Type of query"},
                     color_discrete_sequence=px.colors.qualitative.Safe,
                     color='query.name')
        name_plot2 = ("_").join(["AllQueries",name,"boxplot.html"])
        pio.write_html(box_fig,name_plot2,
                      auto_open=False)


        
    except:
        print("Warning - missing files for services")
        
  
def parse_csv_files(path):   
    """
    

    Parameters
    ----------
    path : TYPE
        DESCRIPTION.

    Returns
    -------
    files : TYPE
        DESCRIPTION.

    """
    # Initialize list of files
    files = []
    # r=root, d=directories, f = files
    for r, d, f in os.walk(path):
    # Iterate over fies found
        for file in f:
    # Check file is of type csv
            if '.csv' in file:
    # get file along with path
                files.append(os.path.join(r, file))
    return files
        
def getArguments():
    # Set up the command line parser
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=""
    )
    # Output results directory
    parser.add_argument("path")
    # Start Date
    #parser.add_argument("s_date")
    # End date
    #parser.add_argument("e_date")
    # End date
    parser.add_argument("keyword")
    # Verbosity flag
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Run the program in verbose mode.")
    # Unified scale flag
    parser.add_argument(
        "-s",
        "--scale",
        action="store_true",
        help="Scale the graphs so they are all on the same y-axis scale.")

    # Parse the command line arguements.
    options = parser.parse_args()
    return options   

if __name__=="__main__":
    
    # Command line arguments
    options = getArguments()
    path = options.path
    #s_date = options.s_date
    #e_date = options.e_date
    keyword = options.keyword
    # Read file names and store in list
    #path = "./logs/"
    files = parse_csv_files(path)
    #keyword = "intensity"
    
    # Iterate over files 
    all_dfs = []
    for i in range(len(files)):
        #print(files[i])
        df = pd.read_csv(files[i],sep=',')
        if "intensity.csv" in files[i]:
            df['query.type'] = "Intensity"
        if "intensity_factors.csv" in files[i]:
            df['query.type'] = "Intensity-Factors"
        if "stats" in files[i]:
            df['query.type'] = "Intensity-Stats"
        if "corrently" in files[i]:
            df["query.type"] = "Corrently-Stats"
        all_dfs.append(df) 
        
    # Put all csv content into a single dataframe
    all_the_data = pd.concat([all_dfs[i] for i in range(len(files))],sort=False)
    
    # data date and time manipulation
    all_the_data["Date/Time"] = all_the_data['query.date'] + " " +  all_the_data['query.time']
    all_the_data["Date/Time"] = pd.to_datetime(all_the_data['Date/Time'])
    
    # Sort data
    all_the_data.sort_values(by='Date/Time',inplace=True)

    # Remove outlier
    #all_the_data = all_the_data[all_the_data['query.lasted']<200]


    # Generate plots
    if keyword=="intensity":
        plot_uk_intensity(all_the_data, "CO2_UK_Emissions")
    elif keyword=="berlin":
        plot_performance(all_the_data,"BerlinEmissions")
