import os
import re
import pandas as pd
import argparse
from tqdm import tqdm
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def parse_benchmark_file(file_path):
    """
    Parses a single benchmark file and extracts relevant metrics.
    """
    all_data = []
    file_name = os.path.basename(file_path)
    protocol_match = re.search(r'\d+-(.+)\.txt', file_name)
    protocol = protocol_match.group(1) if protocol_match else 'unknown'

    with open(file_path, 'r') as f:
        content = f.read()
    logging.info(f"File content loaded, length: {len(content)}")

    reports = content.split('-- Report #')[1:]
    logging.info(f"Found {len(reports)} reports to process.")

    for i, report in enumerate(reports):
        logging.info(f"Processing report {i+1}/{len(reports)}")
        report_match = re.search(r'(\d+) @ t=([\d.]+)s --', report)
        if not report_match:
            logging.warning(f"No report match found for report {i+1}")
            continue
        
        report_num = int(report_match.group(1))
        timestamp = float(report_match.group(2))
        logging.info(f"  Report Num: {report_num}, Timestamp: {timestamp}")

        client_section_match = re.search(r'-- Client \d+\n(.*?)(?=\n-- |\Z)', report, re.DOTALL)
        if not client_section_match:
            logging.warning(f"  No client section found for report {report_num}")
            continue

        client_section = client_section_match.group(1)
        logging.info(f"  Client section found.")
        
        throughput_match = re.search(r'throughput\s+([\d.]+)req/s', client_section)
        req_exec_match = re.search(r'request-execute\s+avg:\s+([\d.]+)(?:s)?,\s+max:\s+([\d.]+)(?:s)?', client_section)

        throughput = float(throughput_match.group(1)) if throughput_match else 0.0
        latency_avg = float(req_exec_match.group(1)) if req_exec_match else 0.0
        latency_max = float(req_exec_match.group(2)) if req_exec_match else 0.0
        
        logging.info(f"  Throughput: {throughput}, Latency Avg: {latency_avg}, Latency Max: {latency_max}")

        node_sections = re.findall(r'-- Node (\d+)\n(.*?)(?=\n-- |\Z)', report, re.DOTALL)
        logging.info(f"  Found {len(node_sections)} node sections.")
        
        block_exec_avg_list = []
        message_proc_avg_list = []
        
        for node_id, node_section in node_sections:
            logging.info(f"    Processing node {node_id}")
            block_exec_match = re.search(r'block-execute\s+avg:\s+([\d.]+)(?:ms)?,\s+max:\s+([\d.]+)(?:ms)?', node_section)
            message_proc_avg_match = re.search(r'message-process\s+avg:\s+(-?[\d.]+)(?:ms)?', node_section)

            if block_exec_match:
                block_avg = float(block_exec_match.group(1))
                block_exec_avg_list.append(block_avg)
                logging.info(f"      Block Exec Avg: {block_avg}")
            else:
                logging.warning(f"      No block-execute match for node {node_id}")

            if message_proc_avg_match:
                msg_avg = float(message_proc_avg_match.group(1))
                message_proc_avg_list.append(msg_avg)
                logging.info(f"      Message Proc Avg: {msg_avg}")
            else:
                logging.warning(f"      No message-process match for node {node_id}")

        avg_block_exec_time = sum(block_exec_avg_list) / len(block_exec_avg_list) if block_exec_avg_list else 0.0
        avg_message_proc_time = sum(message_proc_avg_list) / len(message_proc_avg_list) if message_proc_avg_list else 0.0
        logging.info(f"  Avg Block Exec: {avg_block_exec_time}, Avg Msg Proc: {avg_message_proc_time}")

        all_data.append({
            'protocol': protocol,
            'file': file_name,
            'report_num': report_num,
            'timestamp': timestamp,
            'throughput': throughput,
            'latency_avg_s': latency_avg,
            'latency_max_s': latency_max,
            'avg_block_exec_time_ms': avg_block_exec_time,
            'avg_message_proc_time_ms': avg_message_proc_time
        })
        
    return all_data

def main():
    parser = argparse.ArgumentParser(description='Parse benchmark files and generate a CSV.')
    parser.add_argument('--dir', type=str, default='analysis/benchmark_files', help='Directory containing benchmark .txt files.')
    args = parser.parse_args()

    benchmark_dir = args.dir
    if not os.path.isdir(benchmark_dir):
        print(f"Error: Directory not found at '{benchmark_dir}'")
        # Create the directory if it doesn't exist
        print(f"Creating directory '{benchmark_dir}'...")
        os.makedirs(benchmark_dir)
        print("Please add your benchmark .txt files to this directory and run the script again.")
        return

    all_files_data = []
    file_list = [f for f in os.listdir(benchmark_dir) if f.endswith('.txt')]

    if not file_list:
        print(f"No .txt files found in '{benchmark_dir}'. Please add your benchmark files.")
        return
        
    print(f"Found {len(file_list)} benchmark files to parse.")

    for file_name in tqdm(file_list, desc="Parsing files"):
        file_path = os.path.join(benchmark_dir, file_name)
        all_files_data.extend(parse_benchmark_file(file_path))

    if not all_files_data:
        print("No data parsed. Exiting.")
        return

    df = pd.DataFrame(all_files_data)
    output_dir = 'analysis/benchmark_csv'
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, 'benchmarks.csv')
    df.to_csv(output_path, index=False)
    print(f"Successfully generated CSV file at: {output_path}")

if __name__ == '__main__':
    main()
