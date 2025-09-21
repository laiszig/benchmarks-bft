import pandas as pd
import argparse
import os

def summarize_benchmarks(csv_path):
    """
    Analyzes the parsed benchmark data, generating meaningful summary tables.
    """
    if not os.path.exists(csv_path):
        print(f"Error: CSV file not found at '{csv_path}'")
        return

    df = pd.read_csv(csv_path)

    # --- Data Cleaning ---
    # Filter out the long tail of zero-throughput data points at the end of runs.
    # This is crucial for calculating meaningful statistics.
    cleaned_df = df[df['throughput'] > 0].copy()

    if cleaned_df.empty:
        print("No data with throughput greater than zero was found. Cannot generate summary.")
        return

    # --- Calculate Summary Statistics ---
    # Define the aggregations we want to compute.
    aggregations = {
        'mean': 'mean',
        'median': 'median',
        'std_dev': 'std',
        'p95': lambda x: x.quantile(0.95),
        'p99': lambda x: x.quantile(0.99),
        'max': 'max'
    }

    # Group by protocol and calculate stats for throughput and block execution time
    throughput_summary = cleaned_df.groupby('protocol')['throughput'].agg(**aggregations).round(2)
    block_time_summary = cleaned_df.groupby('protocol')['avg_block_exec_time_ms'].agg(**aggregations).round(2)

    # --- Display Tables ---
    print("--- Throughput Summary (req/s) ---")
    print("Analysis based on data where throughput > 0.")
    print(throughput_summary)
    print("\n" + "="*40 + "\n")
    
    print("--- Average Block Execution Time Summary (ms) ---")
    print("Analysis based on data where throughput > 0.")
    print(block_time_summary)
    print("\n")


def main():
    parser = argparse.ArgumentParser(description='Summarize benchmark data from a CSV file.')
    parser.add_argument('--csv', type=str, default='analysis/benchmark_csv/benchmarks.csv', help='Path to the benchmark CSV file.')
    args = parser.parse_args()
    summarize_benchmarks(args.csv)

if __name__ == '__main__':
    main()
