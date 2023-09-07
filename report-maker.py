import argparse
import pandas as pd
import os
import matplotlib.pyplot as plt
import datetime

def create_excel_file(log_file, output_file):
    df = pd.read_csv(log_file, sep='\t+| +', engine='python')

    with pd.ExcelWriter(f'{output_file}.xlsx', engine='openpyxl') as writer:

        df.to_excel(writer, sheet_name='Raw Log Data', index=False)

        stats_df = df[['Connections', 'Inserts', 'Query', 'Updates', 'Deletes']].agg(['mean', 'max', 'min']).round(0)
        stats_df.to_excel(writer, sheet_name='Statistics')


def parse_log_file(log_file_path, num_lines):
    data = []
    with open(log_file_path, 'r') as file:
        lines = file.readlines()
        lines = lines[1:]
        step = max(len(lines) // num_lines, 1)
        for i in range(0, len(lines), step):
            line = lines[i]
            if " " in line:
                parts = line.strip().split(" ")
                timestamp_str = parts[-1]
                timestamp = datetime.datetime.strptime(timestamp_str, '%Y-%m-%d-%H:%M:%S.%f')
                data.append((timestamp.strftime('%H:%M'), int(parts[3]), int(parts[4]), int(parts[5]), int(parts[6])))
    return data


def create_graph(log_file_path, output_file_path, num_lines_to_plot=8):    
    data = parse_log_file(log_file_path, num_lines_to_plot)

    timestamps = [entry[0] for entry in data]
    inserts = [entry[1] for entry in data]
    queries = [entry[2] for entry in data]
    updates = [entry[3] for entry in data]
    deletes = [entry[4] for entry in data]

    plt.figure(figsize=(24, 16)) 

    plt.subplot(2, 2, 1)
    plt.plot(timestamps, inserts, marker='o', linewidth=1)
    plt.title('Inserts')
    plt.xlabel('Timestamp')
    plt.ylabel('Count')
    plt.ticklabel_format(style='plain', axis='y') 

    plt.subplot(2, 2, 2)
    plt.plot(timestamps, queries, marker='o', linewidth=1)
    plt.title('Queries')
    plt.xlabel('Timestamp')
    plt.ylabel('Count')
    plt.ticklabel_format(style='plain', axis='y') 

    plt.subplot(2, 2, 3)
    plt.plot(timestamps, updates, marker='o', linewidth=1)
    plt.title('Updates')
    plt.xlabel('Timestamp')
    plt.ylabel('Count')
    plt.ticklabel_format(style='plain', axis='y') 

    plt.subplot(2, 2, 4)
    plt.plot(timestamps, deletes, marker='o', linewidth=1)
    plt.title('Deletes')
    plt.xlabel('Timestamp')
    plt.ylabel('Count')
    plt.ticklabel_format(style='plain', axis='y') 

    plt.subplot(2, 2, 1)
    plt.gca().set_yticklabels(['{:,.0f}'.format(x) for x in plt.gca().get_yticks()])
    plt.subplot(2, 2, 2)
    plt.gca().set_yticklabels(['{:,.0f}'.format(x) for x in plt.gca().get_yticks()])
    plt.subplot(2, 2, 3)
    plt.gca().set_yticklabels(['{:,.0f}'.format(x) for x in plt.gca().get_yticks()])
    plt.subplot(2, 2, 4)
    plt.gca().set_yticklabels(['{:,.0f}'.format(x) for x in plt.gca().get_yticks()])

    plt.tight_layout()
    plt.subplots_adjust(hspace=0.2, wspace=0.2)
    plt.savefig(f'{output_file_path}.png')


def main(log_file_name, output_file_name, num_lines_to_plot):
    log_file_path = f'./reports/{log_file_name}'
    output_file_path = f'./reports/{output_file_name}'

    create_excel_file(log_file_path, output_file_path)
    create_graph(log_file_path, output_file_path, num_lines_to_plot)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='MongoDB server stats report maker.')
    parser.add_argument('-l', '--log', type=str, default='monitoring-mongodb.log', help='Log file name')
    parser.add_argument('-o', '--output', type=str, default='mongodb_stats', help='Output file name')
    parser.add_argument('-n', '--num_lines', type=int, default=8, help='Number of timestream points to plot')
    args = parser.parse_args()

    if os.path.exists('./reports') is False:
        os.mkdir('./reports')

    main(args.log, args.output, args.num_lines)
    print(f'Created report: {args.output}.xlsx')