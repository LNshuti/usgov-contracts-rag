import os
import re

def parse_wandb_logs(log_directory):
    log_files = [f for f in os.listdir(log_directory) if f.startswith("run")]
    data = []

    for log_file in log_files:
        with open(os.path.join(log_directory, log_file), 'r', errors='ignore') as file:
            for line in file:
                if "selected_table" in line:
                    match = re.search(r"selected_table (.+)", line)
                    if match:
                        data.append(match.group(1))
    return data

def main():
    # Specify the directory where wandb stores its log files
    log_directory = '../wandb/latest-run/'  

    selected_tables = parse_wandb_logs(log_directory)
    print("Selected Tables:", selected_tables)

if __name__ == "__main__":
    main()
