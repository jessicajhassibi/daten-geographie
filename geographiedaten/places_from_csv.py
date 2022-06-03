import csv

source = "../data/kv-ort-eigeneorte.csv"
target = "../data/places_from_db.csv"

with open(source, 'r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    
    with open(target, "w", newline ='') as new_file:
        ort_name = 'KV-ORT-Name'
        ort_id = 'KV-ORT-GND-ID'

        fieldnames = [ort_name, ort_id]

        csv_writer = csv.DictWriter(new_file, fieldnames=fieldnames)
        
        csv_writer.writeheader()
        
        for line in csv_reader:
            new_dict = {ort_name: line[ort_name], ort_id: line[ort_id]}
            csv_writer.writerow(new_dict)