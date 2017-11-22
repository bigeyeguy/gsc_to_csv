#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2015 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import argparse
import csv
import sys
import pandas as pd
from googleapiclient import sample_tools
from googleapiclient import errors



# Declare command-line flags.
argparser = argparse.ArgumentParser(add_help=False)
argparser.add_argument('property_uri', type=str,
                       help=('Site or app URI to query data for (including '
                             'trailing slash).'))
argparser.add_argument('start_date', type=str,
                       help=('Start date of the requested date range in '
                             'YYYY-MM-DD format.'))
argparser.add_argument('end_date', type=str,
                       help=('End date of the requested date range in '
                             'YYYY-MM-DD format.'))


def main(argv):
  service, flags = sample_tools.init(
      argv, 'webmasters', 'v3', __doc__, __file__, parents=[argparser],
      scope='https://www.googleapis.com/auth/webmasters.readonly')

  # First run a query to learn which dates we have data for. You should always
  # check which days in a date range have data before running your main query.
  # This query shows data for the entire range, grouped and sorted by day,
  # descending; any days without data will be missing from the results.
  '''request = {
      'startDate': flags.start_date,
      'endDate': flags.end_date,
      'dimensions': ['date']
  }
  response = execute_request(service, flags.property_uri, request)
  print_table(response, 'Available dates') '''

 
  # Get top queries for the date range, sorted by click count, descending.
  request = {
      'startDate': flags.start_date,
      'endDate': flags.end_date,
      'dimensions': ['query'],
      'rowLimit':5000
  }
  response = execute_request(service, flags.property_uri, request)
  print_table(response, 'Top Queries')

 
def execute_request(service, property_uri, request):
  """Executes a searchAnalytics.query request.
  Args:
    service: The webmasters service to use when executing the query.
    property_uri: The site or app URI to request data for.
    request: The request to be executed.
  Returns:
    An array of response rows.
  """
  return service.searchanalytics().query(
      siteUrl=property_uri, body=request).execute()


def print_table(response, title):
  """Prints out a response table.
  Each row contains key(s), clicks, impressions, CTR, and average position.
  Args:
    response: The server response to be printed as a table.
    title: The title of the table.
  """
  
  if 'rows' not in response:
    print 'Empty response'
    return

  rows = response['rows']

## PUT ABOVE INTO A PANDAS DATAFRAME ##
  rowsDF = pd.DataFrame(rows)
    
  rowsDF['keys'] = rowsDF['keys'].map(lambda x: str(x)[:-1])
  rowsDF['keys'] = rowsDF['keys'].map(lambda x: str(x)[2:])
  
  rowsDF.to_excel('New_file.xls', index = False)
  
  print('Done')
  print(rowsDF)

  ## I'll need a 2.7 venv to run this
  # since current py is 3.6
	
			
if __name__ == '__main__':
  main(sys.argv)