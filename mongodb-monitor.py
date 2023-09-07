import argparse
import time
from pymongo import MongoClient
import pandas as pd
import os

def connect_to_mongodb(uri):
    # Check for replicaSet in uri and replace with directConnection
    if 'replicaSet=rs0' in uri:
        uri = uri.replace('replicaSet=rs0', 'directConnection=true')

    client = MongoClient(uri)
    db = client.admin
    return db


def get_server_stats(db):
    return db.command('serverStatus')


def get_replica_status(db):
    is_master_result = db.command('isMaster')
    if 'setName' in is_master_result:
        if is_master_result['ismaster']:
            return 'Primary'
        else:
            return 'Secondary'


def display_server_stats(stats, db, fields, output_file, header=True):
    # Extract specific metrics from the stats dictionary
    metrics = {
        'Host': stats['host'].split('.')[0],
        'Status': get_replica_status(db),
        'Connections': stats['connections']['current'],
        'Inserts': stats['opcounters']['insert'],
        'Query': stats['opcounters']['query'],
        'Updates': stats['opcounters']['update'],
        'Deletes': stats['opcounters']['delete'],
        'GetMore': stats['opcounters']['getmore'],
        'Command': stats['opcounters']['command'],
        'CursorsTotal': stats['metrics']['cursor']['open']['total'],
        'CursorsNoTimeout': stats['metrics']['cursor']['open']['noTimeout'],
        'Timestamp': stats['localTime']
    }

    fields = [field.lower() for field in fields]
    selected_metrics = {key: value for key, value in metrics.items() if key.lower() in fields}

    # Convert the selected metrics dictionary to a DataFrame for tabular display
    df = pd.DataFrame(selected_metrics, index=[0])

    # Convert the DataFrame to a string and remove the index from the output
    table_str = df.to_string(header=header, index=False)

    # Write the DataFrame to the output file
    with open(f'./reports/{output_file}', 'a') as f:
        if table_str.strip().startswith('Host'):
            table_lst = table_str.strip().split()[:12]
            table_str = ' '.join(table_lst)
            print(table_str)
            f.write(table_str)
        else:
            table_lst = table_str.strip().split()
            table_lst[-2] = table_lst[-2] + '-' + table_lst[-1]
            table_lst.pop()
            table_str = ' '.join(table_lst)
            print(table_str)
            f.write('\n')
            f.write(table_str)

def main(uri, polling_interval, fields, output_file, existing_file=False):
    db = connect_to_mongodb(uri)
    if existing_file: 
        iteration_counter = 1
    else:
        iteration_counter = 0

    try:
        while True:
            server_stats = get_server_stats(db)
            if iteration_counter == 0:
                display_server_stats(server_stats, db, fields, output_file, header=True)
            else:
                display_server_stats(server_stats, db, fields, output_file, header=False)
            time.sleep(polling_interval)
            iteration_counter += 1
    except KeyboardInterrupt:
        print('\nMonitoring stopped by the user.')
    finally:
        db.client.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Real-time Amazon MongoDB server stats monitoring tool.')
    parser.add_argument('--uri', required=True, help='MongoDB connection URI.')
    parser.add_argument('-i', '--interval', type=int, default=1, help='Polling interval in seconds (Default: 1s).')
    parser.add_argument('-f', '--field', type=str, default='Host,Status,Connections,Inserts,Query,Updates,Deletes,GetMore,Command,CursorsTotal,CursorsNoTimeout,Timestamp',
                        help='Comma-separated fields to display in the output.')
    parser.add_argument('-o', '--output', type=str, default='monitoring-mongodb.log', help='Output file name.')
    args = parser.parse_args()

    fields = [field.strip() for field in args.field.split(',')]

    if os.path.exists('./reports') is False:
        os.mkdir('./reports')

    existing_file = False
    if os.path.exists(f'./reports/{args.output}'):
        output_method = input('File already exists. Do you want to overwrite [1] or append [2] to it? : ').strip()
        if output_method == '1':
            os.remove(f'./reports/{args.output}')
        elif output_method == '2':
            existing_file = True
            pass
        else:
            print('Invalid option. Exiting.')
            exit(1)

    main(args.uri, args.interval, fields, args.output, existing_file)
    print(f'Created report: {args.output}')
