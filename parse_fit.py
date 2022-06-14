#!/usr/bin/env python
from pathlib import Path
import fitparse

flds = [
    'timestamp',
    'motor_power',
    'power',
    'cadence',
    'speed',
    'distance',
    'altitude',
    'currAssist',
    'curCurrentScale',
    'curProfileScale',
    'batCurrCap1',
    'motorTemp',
]

def parse(data_dir):

    for fn_path in data_dir.glob('*.fit'):

        # create output file path
        fout_path = Path(fn_path).with_suffix('.csv')
        fout_name = fout_path.name.replace('ride__', '')
        fout_path = fout_path.with_name(fout_name)
        if fout_path.exists():
            continue

        print(f'Parsing: {fn_path}')
        # Load the FIT file
        fitfile = fitparse.FitFile(str(fn_path))

        # write the header row with field names to the file
        fout = open(fout_path, 'w')
        fout.write(','.join(flds) + '\n')

        # Iterate over all messages of type "record"
        # (other types include "device_info", "file_creator", "event", etc)
        for record in fitfile.get_messages("record"):
            
            if len(record.fields) < 15:
                continue
            rec = {}
            # Records can contain multiple pieces of data (ex: timestamp, latitude, longitude, etc)
            for data in record:
                if data.name in flds:
                    rec[data.name] = str(data.value)

            if float(rec['speed']) == 0.0:
                continue
            vals = [rec[fld] for fld in flds]
            fout.write(','.join(vals) + '\n')   

if __name__ == "__main__":
    data_dir = Path.home() / Path('gdrive/Recreation/bike/fit-data/')
    parse(data_dir)