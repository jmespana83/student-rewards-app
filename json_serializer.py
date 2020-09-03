# json serializer
# uses PGClient, transforms

import json
import os
from postgres_client import PGClient

def pgToJSON(fetchHouseRecords):
    """module to convert and structure postgres 'student' table to JSON format"""

    # store records in corresponding houses. fetchHouseRecords return list of tuples
    gryffindor = fetchHouseRecords('Gryffindor')
    slytherin = fetchHouseRecords('Slytherin')
    ravenclaw = fetchHouseRecords('Ravenclaw')
    hufflepuff = fetchHouseRecords('Hufflepuff')

    # JSON will look similar to this structure

    objList = [
        {
            'house': 'Gryffindor',
            'total': 0,
            'students': []
        },
        {
            'house': 'Slytherin',
            'total': 0,
            'students': []
        },
        {
            'house': 'Ravenclaw',
            'total': 0,
            'students': []
        },
        {
            'house': 'Hufflepuff',
            'total': 0,
            'students': []
        }
    ]
    # list of list of tuples
    recordList = [gryffindor, slytherin, ravenclaw, hufflepuff]

    # using parallel list strategy to combine dictionaries with sql queries
    # will use sum function to add all points (index 4 or 5th element of each record)
    # use list comprehension to turn tuples into dictionaries sorted by score (index 4 or 5th element of each record)
    for i in range(0, 4):
        objList[i]['total'] = sum([record[4] for record in recordList[i]])
        # use list comprehension to create list of dictionaries
        objList[i]['students'] = [
            {
                'name': record[2],
                'points': record[4]
            }
            for record in recordList[i]
        ]
        # sort every student list in order from high points to lowest points
        objList[i]['students'] = sorted(objList[i]['students'], key=lambda d: d['points'], reverse=True)

    # write objList to new or existing JSON file named house_results:
    # will write to web/ directory since path is already changed in tigers_houses.py
    with open('house_results.json', 'w') as fh:
        json.dump(objList, fh, indent=4)