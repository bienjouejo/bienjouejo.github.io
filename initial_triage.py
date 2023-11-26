import subprocess
import os
import sys
import re

def find_profile(dump_file):
    # Use volatility to find the profile for the given dump file
    command = f"volatility -f {dump_file} imageinfo"
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    
    # Extract the profile using regular expression
    profile_match = re.search(r"Suggested Profile\(s\) : (.+)", result.stdout)
    
    if profile_match:
        return profile_match.group(1).strip().split(",")[0]  # Get the first suggested profile
    else:
        return None

def run_volatility_command(dump_file, profile, command, output_folder):
    # Execute volatility command with the specified profile
    output_file = os.path.join(output_folder, f"{command}_output.txt")
    volatility_command = f"volatility -f {dump_file} --profile={profile} {command} > {output_file}"
    subprocess.run(volatility_command, shell=True)

def main():
    # Check if a dump file is provided as a command-line argument
    if len(sys.argv) != 2:
        print("Usage: python3 initial_triage.py <dump_file>")
        sys.exit(1)

    dump_file = sys.argv[1]
    output_folder = "result_initial_triage"

    # Find the profile for the dump file
    profile = find_profile(dump_file)

    if profile is not None:
        print(f"Profile found: {profile}")

        # Create a sub-folder named "browser"
        browser_folder = os.path.join(output_folder, "browser")
        os.makedirs(browser_folder, exist_ok=True)

        # Define Volatility commands to run
        volatility_commands = ["consoles", "iehistory"]  # Modified to include only these commands

        # Run each Volatility command and save output to a text file in the appropriate folder
        for command in volatility_commands:
            run_volatility_command(dump_file, profile, command, browser_folder)
            print(f"{command} command executed. Results saved to {browser_folder}/{command}_output.txt")

        # Additional commands to run
        other_commands = ["pslist", "netscan", "filescan"]

        for command in other_commands:
            run_volatility_command(dump_file, profile, command, output_folder)
            print(f"{command} command executed. Results saved to {output_folder}/{command}_output.txt")

    else:
        print("Profile not found. Unable to proceed.")

if __name__ == "__main__":
    main()
