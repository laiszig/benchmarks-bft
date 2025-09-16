import pandas as pd
import matplotlib.pyplot as plt
import argparse
import os

def analyze_benchmarks(csv_path):
    """
    Analyzes the parsed benchmark data, generating tables and plots.
    """
    if not os.path.exists(csv_path):
        print(f"Error: CSV file not found at '{csv_path}'")
        return

    df = pd.read_csv(csv_path)
    
    # --- Generate Summary Table ---
    summary = df.groupby('protocol').agg({
        'throughput': ['mean', 'std', 'min', 'max'],
        'latency_avg_s': ['mean', 'std', 'min', 'max'],
        'avg_block_exec_time_ms': ['mean', 'std', 'min', 'max']
    }).round(2)

    print("--- Benchmark Summary ---")
    print(summary)
    print("\n")

    # Create a directory for plots if it doesn't exist
    plots_dir = 'analysis/plots'
    os.makedirs(plots_dir, exist_ok=True)

    # --- Generate Plots ---
    protocols = df['protocol'].unique()
    
    # 1. Throughput over Time
    plt.figure(figsize=(12, 6))
    for protocol in protocols:
        subset = df[df['protocol'] == protocol]
        plt.plot(subset['timestamp'], subset['throughput'], label=f'{protocol} Throughput', marker='o', linestyle='--')
    plt.title('Throughput Comparison Over Time')
    plt.xlabel('Time (s)')
    plt.ylabel('Throughput (req/s)')
    plt.legend()
    plt.grid(True)
    plt.savefig(os.path.join(plots_dir, 'throughput_comparison.png'))
    plt.close()

    # 2. Latency over Time
    plt.figure(figsize=(12, 6))
    for protocol in protocols:
        subset = df[df['protocol'] == protocol]
        plt.plot(subset['timestamp'], subset['latency_avg_s'], label=f'{protocol} Avg Latency', marker='o', linestyle='--')
    plt.title('Average Latency Comparison Over Time')
    plt.xlabel('Time (s)')
    plt.ylabel('Average Latency (s)')
    plt.legend()
    plt.grid(True)
    plt.savefig(os.path.join(plots_dir, 'latency_comparison.png'))
    plt.close()

    # 3. Block Execution Time over Time
    plt.figure(figsize=(12, 6))
    for protocol in protocols:
        subset = df[df['protocol'] == protocol]
        plt.plot(subset['timestamp'], subset['avg_block_exec_time_ms'], label=f'{protocol} Block Exec Time', marker='o', linestyle='--')
    plt.title('Block Execution Time Comparison Over Time')
    plt.xlabel('Time (s)')
    plt.ylabel('Avg Block Execution Time (ms)')
    plt.legend()
    plt.grid(True)
    plt.savefig(os.path.join(plots_dir, 'block_exec_time_comparison.png'))
    plt.close()

    print(f"Plots have been saved to the '{plots_dir}' directory.")

def main():
    parser = argparse.ArgumentParser(description='Analyze benchmark data from a CSV file.')
    parser.add_argument('--csv', type=str, default='analysis/benchmark_csv/benchmarks.csv', help='Path to the benchmark CSV file.')
    args = parser.parse_args()
    analyze_benchmarks(args.csv)

if __name__ == '__main__':
    main()
