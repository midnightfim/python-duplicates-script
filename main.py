import json
import datetime

f = open("markup.crash")
data = json.load(f)

for i in data:
    print(i)

actorsArray = data['actors_id']

values = data['actors']

duplicateRecordsArray = []
longRecordsArray = []

for recordKey in values:
    record = values[recordKey]
    actorsInRecordArray = []
    isDuplicateRecord = False

    dateTime = list(recordKey.split(':'))
    ms = dateTime.pop(3)
    for item in dateTime:
        dateTime[dateTime.index(item)] = item.encode('ascii', 'ignore')

    date_time = datetime.datetime.strptime(':'.join(dateTime), "%H:%M:%S")
    a_timedelta = date_time - datetime.datetime(1900, 1, 1)
    seconds = a_timedelta.total_seconds() + float(ms)/1000

    utcFormatTimeFromStart = recordKey.split(':')

    for coords in record:
        if coords[coords.keys()[0]] in actorsInRecordArray:
            isDuplicateRecord = True
        else:
            actorsInRecordArray.append(coords[coords.keys()[0]])

    if isDuplicateRecord:
        duplicateRecordsArray.append({seconds: {'record': record, 'time': recordKey}})

    if len(record) >= 4:
        longRecordsArray.append({seconds: {'record': record, 'time': recordKey}})

with open('duplicates.json', 'w') as f:
    f.write(json.dumps({
        'length': len(duplicateRecordsArray),
        'duplicates': sorted(duplicateRecordsArray)
    }))

with open('long_records.json', 'w') as f:
    f.write(json.dumps({
        'length': len(longRecordsArray),
        'long_records': longRecordsArray
    }))
