import csv
import gzip
import unicodedata as ud

import fire
import ijson


def is_valid(record):
    key_preferred_name = 'https://d-nb.info/standards/elementset/gnd#preferredNameForThePlaceOrGeographicName'
    return key_preferred_name in record


def record_name(record):
    key_preferred_name = 'https://d-nb.info/standards/elementset/gnd#preferredNameForThePlaceOrGeographicName'
    place_name = record[key_preferred_name][0]['@value'] 
    place_name = ud.normalize('NFC', place_name)
    return place_name


def record_gnd_id(record):
    key_gnd_id = 'https://d-nb.info/standards/elementset/gnd#gndIdentifier'
    gnd_id = record[key_gnd_id][0]['@value']
    return gnd_id


def record_to_row(record):
    place = record_name(record)
    gnd_id = record_gnd_id(record)
    row = {'ort': place, 'gnd_id': gnd_id}
    return row


def run(places, geografikum, output):
    """
    Matches GND Geografikum Records with places.
    Output CSV header: ort, gnd_id.

    Args:
        places (str): Places table in CSV format.
        geografikum (str): Geografikum file in JSONLD.GZ format.
        output (str): Output file in CSV format.
    """
    with open(places, "r", encoding="utf8") as fin1:
        with gzip.open(geografikum, 'rt', encoding="utf8") as fin2:
            with open(output, "w", newline='', encoding="utf8") as fout:
                writer = csv.DictWriter(fout, fieldnames=['ort', 'gnd_id'])
                writer.writeheader()

                places_reader = csv.DictReader(fin1)
                places = { row['KV-ORT-Name'] for row in places_reader }

                for record in ijson.items(fin2, 'item.item'):
                    if not is_valid(record):
                        continue
                    
                    place = record_name(record)
                    if place in places:
                        row = record_to_row(record)
                        writer.writerow(row)


def main(): 
    fire.Fire(run)
    

if __name__ == "__main__":
    main()
