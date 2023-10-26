import subprocess
import os
import sys

def find_profile(dump_file):
    # Use volatility to find the profile for the given dump file
    command = f"volatility -f {dump_file} imageinfo"
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    
    # Extract the profile from the result
    profile_lines = result.stdout.split('\n')
    for line in profile_lines:
        if line.startswith("Suggested Profile"):
            return line.split(":")[1].strip()

    return None

def run_volatility_command(dump_file, profile, command, output_file):
    # Execute volatility command with the specified profile
    volatility_command = f"volatility -f {dump_file} --profile={profile} {command} > {output_file}"
    subprocess.run(volatility_command, shell=True)

def main():
    # Check if a dump file is provided as a command-line argument
    if len(sys.argv) != 2:
        print("Usage: python3 initial_triage.py <dump_file>")
        sys.exit(1)

    dump_file = sys.argv[1]
    
    # Find the profile for the dump file
    profile = find_profile(dump_file)

    if profile is not None:
        print(f"Profile found: {profile}")

        # Define Volatility commands to run
        volatility_commands = ["pslist", "netscan", "filescan"]

        # Run each Volatility command and save output to a text file
        for command in volatility_commands:
            output_file = f"{command}_output.txt"
            run_volatility_command(dump_file, profile, command, output_file)
            print(f"{command} command executed. Results saved to {output_file}")

    else:
        print("Profile not found. Unable to proceed.")

if __name__ == "__main__":
    main()
