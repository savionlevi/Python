import subprocess
import sys
from datetime import datetime


def memory_test(iterations):
    iterations = iterations * 1000000
    for i in range(iterations):
        command = "ps x -o rss,vsz,command | awk \'NR>1 {$1=int($1/1024)\"M\"; $2=int($2/1024)\"M\";}{ print ;}\' | grep \"<process_name>\""
        output = subprocess.check_output(command, shell=True).decode(sys.stdout.encoding).strip()
        memory = output.split("M")[0]
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")

        if i%50==0:
            print("Memory used: "+memory +"M")
        if i%500==0:
            print("Current Time =", current_time)

def main():
    memory_test(100)

if __name__ == '__main__':
    main()
