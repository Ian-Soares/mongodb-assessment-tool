# MongoDB assessment & report 
These 2 tools will monitor your MongoDB cluster in a log file, calculate the mean, min and max of CRUD Operations, create a spreadsheet and a visual graph of it.

The cluster collected informations will be:

|Host|Status|Connections|Inserts|Query|Updates|Deletes|GetMore|Command|CursorsTotal|CursorsNoTimeout|Timestamp|
|---|---|---|---|---|---|---|---|---|---|---|---| 
|example-mongodb-rs0|Primary|wxyz|wxyz|wxyz|wxyz|wxyz|wxyz|wxyz|x|y|yyyy-mm-dd hh:mm:ss.sss|

| Monitoring tool inspired in https://github.com/awslabs/amazon-documentdb-tools/blob/master/monitoring/docdb-stat

### Requirements

**Clone repository**
```
git clone https://github.com/Ian-Soares/mongodb-assessment-tool.git
```
**Install dependencies**
```
cd mongodb-assessment-tool
python3 -m pip install --upgrade pip
pip install -r requirements.txt
```

## Monitoring tool usage
**The monitoring tool accepts the following arguments:**

```
# python3 mongodb-monitor.py --help
usage: mongodb-monitor.py [-h] --uri URI [-i INTERVAL] [-hi HEADER_INTERVAL] [-f FIELD]

Real-time Amazon DocumentDB server stats monitoring tool.

options:
  -h, --help            show this help message and exit
  --uri URI             DocumentDB connection URI.
  -i INTERVAL, --interval INTERVAL
                        Polling interval in seconds (Default: 1s).
  -f FIELD, --field FIELD
                        Comma-separated fields to display in the output.
  -o OUTPUT, --output
                        Output file name
```

### Examples

Get stats every 5 seconds:

```
python3 mongodb-monitor.py --uri "mongodb://<user>:<pass>@<docdb-instance-endpoint>:27017" -i 5 -o monitoring-mongodb.log
```
| By default, this will create a directory ./reports and a .log file, that will be appended every i seconds

Get specific stats, for example to output just write operations:

```
python3 mongodb-monitor.py --uri "mongodb://<user>:<pass>@<docdb-instance-endpoint>:27017" -f inserts,updates,deletes
```


## Report tool usage
The report tool accepts the following arguments:
```
# python3 report-maker.py --help                                            
usage: report-maker.py [-h] [-l LOG] [-o OUTPUT] [-n NUM_LINES]

MongoDB server stats report maker.

options:
  -h, --help            show this help message and exit
  -l LOG, --log LOG     Log file name
  -o OUTPUT, --output OUTPUT
                        Output file name
  -n NUM_LINES, --num_lines NUM_LINES
                        Number of timestream points to plot
```

### Examples
Specify input log file (inside reports directory):
```
python3 report-maker.py --log "monitoring-mongodb.log" -n 8
```

Specify both input and output names:
```
python3 report-maker.py --log "monitoring-mongodb.log" --output "cluster1-mongodb"
```
### Results
After running those two scripts, there will be created 3 files:
1. ./reports/xyz.log  - **Log file** with **raw data** from the monitoring script
2. ./reports/xyz.xlsx - **Excel file** with the data in columns and the statistics of it: **mean, min and max** values
3. ./reports/xyz.png  - **Image** with a data **graph**
