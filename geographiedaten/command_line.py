import gzip
import fire
import helpers
#python command_line.py match "../data/places_from_db.csv" "../data/example.jsonld" "../data/example_to_put_in_db.csv"import mysql.connector as mariadb
#from mysql.connector import errorcode
import random
import time
import sys
import os

def hello(name):
    print(f"Hello {name}!")

def places_match(source1, source2, target):
    """
    Matches gnd Geografikum Records of source2 with places in source1.
    Output of Information in target for each record as [place_name, gnd_link].

    Args:
        source1 (str): 1st input file in CSV format.
        source2 (str): 2nd input file in JSONLD.GZ format.
        target (str): Output file in CSV format.
    """

    with open(source1, "r", encoding="utf8") as fin1:
        with gzip.open(source2, 'rt', encoding="utf8") as fin2: # without gzip for example
 #       with open(source2, 'rt', encoding="utf8") as fin2: 
            with open(target, "w", newline='', encoding="utf8") as fout:
                helpers.record_match(fin1, fin2, fout)


def links_to_db(host_name, db_name, source):
    """
    Writes gnd-link of place to place in database table "kv-eigeneorte" if no link already there.

    Args:
        host_name (str): Host name for database
        db_name (str): Name of database
        source (str): Input file in CSV format
    """


    conn = mariadb.connect(
        host= host_name,
        database= db_name,
        user= input("User: "),    
        password= input("Password: "))                          

    with open(source, 'r', encoding="utf8") as fin:
        helpers.write_link_to_db(fin, conn)


def main(): 
    fire.Fire({
        'hello': hello,
        'match': places_match,
        'write': links_to_db
    })
    
if __name__ == "__main__":
    main()

