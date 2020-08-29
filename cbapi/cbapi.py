import pandas as pd
import requests
import json
import datetime
import queue
import multiprocessing
import psutil
import numpy as np
import sys

RAPIDAPI_KEY = ''

def set_rapidapi_key(key):
    """ Setup the RAPIDAPI_KEY,
    you will need to register for an account and obtain your own access key
    
    Keyword arguments:
    key: string -- your rapid_key provided by ODM endpoints

    """
    global RAPIDAPI_KEY
    RAPIDAPI_KEY = key

def get_rapidapi_key():
    """ Return your RAPIDAPI_KEY 
    user don't need to call it
    """
    if len(RAPIDAPI_KEY) == 0:
        print("Please first set your rapid key using set_rapidapi_key")
    else:
        return RAPIDAPI_KEY

def trigger_api(query, tp):
    """ Makes a call to Crunchbase API and return a json 
    
    Keyword arguments:
    query: dict -- your request parameters
    tp: string -- 'organizations' or 'people'

    Return:
    json of the request:

        metadata
        data
            paging
                numer_of_pages
                current_page
            items
                type
                uuid
                properties (what we want)
    """
    rapid_key = get_rapidapi_key()
    headers = {
        'x-rapidapi-host': "crunchbase-crunchbase-v1.p.rapidapi.com",
        'x-rapidapi-key': rapid_key
    }
    
    url = "https://crunchbase-crunchbase-v1.p.rapidapi.com/odm-"+tp
    response = requests.request("GET", url, headers=headers, params=query)
    if(200 == response.status_code):
        return json.loads(response.text)
    else:
        return None


def get_data(query, tp, parallel=False, verbose=False):
    """ GET json data from trigger_api function and return a pandas Dataframe

    Keyword arguments:
    query: dict -- your request parameters
    tp: string -- 'organizations' or 'people'
    parallel: bool -- whether to use multiprocessing algorith to get multi-page
                      data, but in README.md in final project suggested milti-threading
                      but I'm not sure whether this will work or not because
                      python has GIL.
    Return:
    pd.Dataframe of the request

    """


    json_data = trigger_api(query, tp)
    number_of_pages = json_data['data']['paging']['number_of_pages']
    current_page = json_data['data']['paging']['current_page']

    if parallel == False:
        nThreads = 1
    else:
        # too many processes is unnecessary
        # make nThreads = #(physical CPU)
        nThreads = psutil.cpu_count(logical=False)
        if verbose == True and current_page==1:
            print(str(nThreads)+' processes used')
            sys.stdout.flush()

    properties = pd.DataFrame(json_data['data']['items'])['properties']
    df = pd.DataFrame(list(properties))

    if current_page != 1:
        # return the only page if this is not the first one
        # since this function is called recursively
        return df

    if number_of_pages == 1:
        # only one page, no need to further
        # access the other pages
        return df
    
    if verbose == True:
        print('page: 1/'+str(number_of_pages))
    
    
    
    # page 2,3,...,number_of_pages
    page_range = range(2, number_of_pages+1)
    # divide page range into nThreads chunks
    pages = np.array_split(list(page_range), nThreads)
    # the each process will get a chunk of pages and append
    # the result to df
    processes = []
    # queue to store the result of the worker
    q = queue.Queue()
    # lock the stdout when we output the message
    lock = multiprocessing.Lock()
    
    def worker(ret,page_list,lock):
        # ret is the queue that store the results
        for page in page_list:
            if verbose == True:
                lock.acquire()
                print('page: '+str(page)+'/'+str(number_of_pages))
                lock.release()
            query_worker = {**query, 'page':page}
            df_worker = get_data(query_worker, tp)
            ret.put(df_worker)

    for i in range(0,nThreads):
        p = multiprocessing.Process(target=worker, args=(q, pages[i],lock))
        processes.append(p)
        p.start()
        
    for process in processes:
        process.join()
    
    while q.empty() == False:
        df = df.append(q.get(),ignore_index=True)

    return df
        

def get_people(**kwargs):
    """ Get people information

    name
        STRING
        OPTIONAL
        A full-text query of name only

    locations
        STRING
        OPTIONAL
        Filter by location names (comma separated, AND'd together) e.g. locations=California,San Francisco

    socials
        STRING
        OPTIONAL
        Filter by social media identity (comma separated, AND'd together) e.g. socials=ronconway

    types
        STRING
        OPTIONAL
        Filter by type (currently, either this is empty, or is simply "investor")

    updated_since
        NUMBER
        OPTIONAL
        When provided, restricts the result set to Organizations where updated_at >= the passed value

    verbose
        BOOL
        OPTIONAL
        Run in the verbose mode

    parallel
        BOOL
        OPTIONAL
        Use multiprocessing to speed-up the multi-pages reading
    """
    verbose = kwargs.pop('verbose', False)
    parallel = kwargs.pop('parallel', False)
    return get_data(query = kwargs, tp='people', parallel=parallel, verbose=verbose)

def get_organizations(**kwargs):
    """Get organizations information

    updated_since
        NUMBER
        OPTIONAL
        When provided, restricts the result set to Organizations where updated_at >= the passed value

    name
        STRING
        OPTIONAL
        Full text search limited to name and aliases

    domain_name
        STRING
        OPTIONAL
        Text search of an Organization's domain_name (e.g. www.google.com)

    locations
        STRING
        OPTIONAL
        Filter by location names (comma separated, AND'd together) e.g. locations=California,San Francisco

    organization_types
        STRING
        OPTIONAL
        Filter by one or more types. Multiple types are separated by commas. Available types are "company", "investor", "school", and "group". Multiple organization_types are logically AND'd.

    verbose
        BOOL
        OPTIONAL
        Run in the verbose mode

    parallel
        BOOL
        OPTIONAL
        Use multiprocessing to speed-up the multi-pages reading
    """

    verbose = kwargs.pop('verbose', False)
    parallel = kwargs.pop('parallel', False)
    return get_data(query = kwargs, tp='organizations', parallel=parallel, verbose=verbose)

