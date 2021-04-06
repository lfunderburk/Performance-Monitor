#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  8 22:58:48 2021

@author: laura.gf
"""


import requests
from requests.exceptions import HTTPError
import time
from dateutil.relativedelta import relativedelta
from datetime import datetime
import pandas as pd
import sys

def query_entry_pt(url):
    """This function takes as input a URL entry point and returns the complete JSON response in a REST API
    
    Input:
        - url(string): complete url (or entry point) pointing at server 
        
    Output:
        - jsonResponse(json object): JSON response associated wtih query
    
    """
    try:
        # Time query
        start_time = time.time()
        # Using GET command 
        response = requests.get(url)
        total_time = time.time() - start_time
        # Raise issues if response is different from 200
        response.raise_for_status()
        # access JSOn content
        jsonResponse = response.json()
        return [jsonResponse,total_time]

    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')
        
def format_json_resp(json_resp,query_time,record_path_field,date,time,output_dir,base_url,entry_pt):
    """
    This function takes query result in JSON format and saves a CSV with results

    Parameters
    ----------
    json_resp : JSON object
        content of query.
    query_time : string
        time it took for the query to complete.
    record_path_field : string
        level necessary to flatten JSON.
    date : datetime object
        date of query.
    time : datetime object
        time of query.
    output_dir : string
        path to directory where CSV query results will be stored.
    base_url : string
        URL pointing at REST API.
    entry_pt : string
        complete query type.

    Returns
    -------
    None.

    """
    
    df = pd.json_normalize(json_resp,record_path=record_path_field)
    df['query.name'] = str(entry_pt.replace("/","_"))
    df['query.lasted'] = query_time
    df['query.date'] = date
    df['query.time'] = time
    
    full_file_name = [output_dir, "_pT_",str(date_f) ,"_" +str(time.replace(":","-")),
                      "_Query_Times_" ,str(base_url.split("//")[1].split(".")[1]) ,
                      "_"+ str(entry_pt.replace("/","_")) , ".csv"]
    df.to_csv(("").join(full_file_name),sep=",")


        
if __name__=="__main__":

    base_url = "https://api.carbonintensity.org.uk/"
    output_dir = "./logs/"
    
    # Get date
    dates = pd.to_datetime('today')
    dates_str = str(dates)
    date_f = dates_str.split(" ")[0]
    time_f = dates_str.split(" ")[1].split(".")[0]

    try:
        # Intensity
        entry_pt = "intensity"
        query_resp,time_q = query_entry_pt(base_url + entry_pt)
        print(time_q)
        
        # Generate dataframe
        format_json_resp(query_resp,time_q,"data",date_f,time_f, \
                                        output_dir,base_url,entry_pt)
            
    except:
        print("Could not complete query")
        sys.exit(0)
        

    
    try:
        # # Factors 
        entry_pt = "intensity/factors"
        query_resp_2,time_q2 = query_entry_pt(base_url + entry_pt)
        print(time_q2)
        
        # # Generate dataframe
        format_json_resp(query_resp_2,time_q2,"data",date_f,time_f, \
                                         output_dir,base_url,entry_pt)
    except:
        print("Could not complete query")
        sys.exit(0)
        
    try:
    
        # # From start date to end date intensity stats
        to_o = datetime.now()
        from_o_pref = to_o + relativedelta(months=-1)
        
        to_f = from_o_pref.strftime("%Y-%m-%dT%H:%MZ")
        from_o_f = to_o.strftime("%Y-%m-%dT%H:%MZ")
        entry_pt = "intensity/stats/"+to_f+"/"+from_o_f
        query_resp_3,time_q3 = query_entry_pt(base_url + entry_pt)
        print(time_q3)
        
        
        # Generate dataframe
        format_json_resp(query_resp_3,time_q3,"data",date_f,time_f, \
                                        output_dir,base_url,entry_pt)
            
    except:
        print("Could not complete query")
        sys.exit(0)