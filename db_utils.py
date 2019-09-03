"""
    Author          :   Siddhi
    Created_date    :   2019/08/20  
    Modified Date   :   2019/09/26
    Description     :   Program utility function.       
"""


import pandas as pd


def insert_df_threaded(df, nworkers=4, *args, **kwargs):
    """
    Insert df using multi threading. Use this for large dataframesself.

    Parameters:
        df          (pandas.DataFrame)  : The dataframe you want to insert.
        nworkers    (int)               : The number of threads you want to useself.
        **kwargs                        : Parameters for pandas.DataFrame.to_sql
    """
    import math
    from multiprocessing.dummy import Pool as ThreadPool

    chunk = math.floor(df.shape[0] / nworkers)  # number of chunks
    chunks = [(chunk * i, (chunk * i) + chunk) for i in range(nworkers)]
    chunks.append((chunk * nworkers, df.shape[0]))
    pool = ThreadPool(nworkers)

    def worker(chunk):
        i, j = chunk
        df.iloc[i:j, :].to_sql(*args, **kwargs)

    pool.map(worker, chunks)
    pool.close()
    pool.join()


def read_table_sql(query, *args, **kwargs):
    """
        Read table from either query or table nameself.
        If the query is a single string, then the function will use read_sql_table
        else the function will use read_sql_query.
        query       (str)               : Query string or table name
        **kwargs                        : Parameters for pandas.read_sql or pandas.read_query
    """
    try:
        if len(query.split()) > 1:
            return pd.read_sql_query(query, *args, **kwargs)
        else:
            return pd.read_sql_table(query, *args, **kwargs)
    except Exception as e:
        raise e


def insert_df(df, *args, **kwargs):
    '''
    Use this to insert smaller dataframes

    Parameters:
        df          (pandas.DataFrame)  : The dataframe you want to insert
        **kwargs                        : Parameters for pandas.DataFrame.to_sql
    '''
    try:
        df.to_sql(
            index=False * args, **kwargs)
    except Exception as e:
        raise e
