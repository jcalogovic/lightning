import os
import pandas as pd
import getpass
import urllib.request
from tqdm import tqdm


def return_time_elements(time_stamp):
    """Returns formatted strings of time stamps for HTML requests.

    :parameters time_range: pandas.tslib.Timestamp
    """
    yyyy = str(time_stamp.year)
    mm = "%02d" % (time_stamp.month,)
    dd = "%02d" % (time_stamp.day,)
    hr = "%02d" % (time_stamp.hour,)
    mins = "%02d" % (time_stamp.minute,)
    return yyyy, mm, dd, hr, mins


def get_data(start, end, username=None, password=None,
             data_path=os.path.abspath(".")+'/tmp_data'):
    """**Download data from Blitzorg**

    Using a specified time stamp for start and end, data is downloaded at a
    default frequency (10 minute intervals). If a directory called data is not
    present, it will be added to the cwd as the target for the downloads.

    :paramter start: string
    :parameter end: string
    :parameter freq: string

    :Example:

    >>> get_data(start="2015-02-01T06:30", end="2015-02-01T10:05")
    """
    dl_link = "http://data.blitzortung.org/Data_1/Protected/Strokes/"
    if not os.path.exists(data_path):
        os.makedirs(data_path)
    if not username:
        username = input("Username to access Blitzorg with:")
        password = getpass.getpass(
            prompt='Enter password for {0}:'.format(username))
    auth_handler = urllib.request.HTTPBasicAuthHandler()
    auth_handler.add_password(realm='Blitzortung',
                              uri='http://data.blitzortung.org',
                              user=username,
                              passwd=password)
    opener = urllib.request.build_opener(auth_handler)
    urllib.request.install_opener(opener)
    time_range = pd.date_range(start, end, freq='10min')
    for time_stamp in tqdm(time_range):
        tmp_link = dl_link+'/'.join(return_time_elements(time_stamp))\
                   + '.json.gz'
        tmp_name = "./tmp_data/bz-"+'-'.join(return_time_elements(time_stamp))\
                   + ".json.gz"
        if os.path.isfile(tmp_name):
            print("{0} exists. Aborting download attempt".format(tmp_name))
        else:
            try:
                urllib.request.urlretrieve(tmp_link, tmp_name)
            except Exception as inst:
                print(inst)
                print('  Encountered unknown error. Continuing.')