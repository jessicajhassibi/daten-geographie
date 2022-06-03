import ijson
import csv
import unicodedata as ud
 
def record_match(places_as_csv, json_filename, result_as_csv):
    csv_reader = csv.reader(places_as_csv)
    places = set()
    for row in csv_reader:
        places.add(row[0])

    records = ijson.items(json_filename, 'item.item')
    key_place_name = 'https://d-nb.info/standards/elementset/gnd#preferredNameForThePlaceOrGeographicName'
    key_place_variant_names = 'https://d-nb.info/standards/elementset/gnd#variantNameForThePlaceOrGeographicName'
    key_gnd_id = 'https://d-nb.info/standards/elementset/gnd#gndIdentifier'
    csv_writer = csv.writer(result_as_csv)


    for record in records: 
        try:
            place_name = record[key_place_name][0]['@value'] 
            place_name = ud.normalize('NFC',place_name)
            gnd_id = record[key_gnd_id][0]['@value']

            if place_name in places:
                row = [place_name, gnd_id]
                csv_writer.writerow(row)

            else:
                variant_names = []
                for entry in range(len(record[key_place_variant_names])):
                    variant_name = record[key_place_name][entry]['@value']
                    variant_names.append(variant_name)

                for variant_name in variant_names:
                    if variant_name in places:
                        row = [variant_name, gnd_id]
                        csv_writer.writerow(row)

        except:
            pass


def write_link_to_db(places_links_as_csv, db_conn):

    csv_reader = csv.reader(places_links_as_csv, delimiter = ",")
    db_cursor = db_conn.cursor()
    db_cursor.execute("SELECT `KV-ORT-Name`, `KV-ORT-GND-ID` FROM `kv-ort-eigeneorte`")
    result = db_cursor.fetchall()
    iterplaces = iter(result)
    next(iterplaces)

    for place in iterplaces:
        place_name = place[0]
        link = place[1]
        if link is None:
            for row in csv_reader:
                if row[0] == place_name:
                    new_link = row[1]
                    new_link = "http://d-nb.info/gnd/" + new_link

                    db_cursor.execute("UPDATE `kv-ort-eigeneorte` SET  `KV-ORT-GND-ID` = %s WHERE `KV-ORT-Name` = %s;",
                    (new_link, place_name))
                    db_conn.commit()

            places_links_as_csv.seek(0)
    
    db_cursor.close()
    db_conn.commit()
    db_conn.close()