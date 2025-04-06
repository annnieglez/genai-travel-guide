from setuptools import setup, find_packages
import subprocess
import sys
import os
import platform
import shutil

def install_sqlite(version="3.35.4"):
    # Check if sqlite3 is already installed and the version is the right one
    try:
        result = subprocess.check_output(["sqlite3", "--version"], stderr=subprocess.STDOUT)
        installed_version = result.decode('utf-8').split()[0]
        if installed_version == version:
            print(f"SQLite {version} is already installed.")
            return
    except FileNotFoundError:
        pass  # sqlite3 is not installed

    print(f"Installing SQLite {version}...")

    # Define the SQLite download URL
    download_url = f"https://sqlite.org/2021/sqlite-autoconf-3350400.tar.gz"

    env = os.environ.copy()
    env["PATH"] = "/usr/local/bin:" + env.get("PATH", "")
    env["LD_LIBRARY_PATH"] = "/usr/local/lib:" + env.get("LD_LIBRARY_PATH", "")

    # Determine the system type to know how to install
    if platform.system() == "Linux":
        # Install dependencies
        subprocess.check_call(['sudo', 'apt-get', 'update'])
        subprocess.check_call(['sudo', 'apt-get', 'install', '-y', 'build-essential', 'wget', 'tar'])

        # Download and install the specific version of SQLite
        subprocess.check_call(['wget', download_url])
        subprocess.check_call(['tar', '-xzf', f"sqlite-autoconf-3350400.tar.gz"])
        os.chdir(f"sqlite-autoconf-3350400")
        subprocess.check_call(['./configure'])
        subprocess.check_call(['make'])
        subprocess.check_call(['sudo', 'make', 'install'])

        # Add SQLite to the system path
        #subprocess.check_call('echo "export PATH=$PATH:/usr/local/bin" >> ~/.bashrc', shell=True)
        #subprocess.check_call('source ~/.bashrc', shell=True)

    elif platform.system() == "Darwin":
        # Install using Homebrew on macOS
        subprocess.check_call(['brew', 'install', f"sqlite@{version}"])

    elif platform.system() == "Windows":
        print("Please install SQLite manually on Windows.")
        sys.exit(1)
    else:
        print(f"Unsupported platform: {platform.system()}, please ensure SQLite3 >= 3.35 is installed manually.")
        sys.exit(1)

# First install the required SQLite version
install_sqlite(version="3.35.4")

setup(
    name="iceland_travel_guide",
    version="0.1",
    packages=find_packages(),
    include_package_data=True,
    description="A GenAI-powered travel guide for Iceland",
    author="Annie Meneses Gonzalez",
    author_email="annieglez92@gmail.com",
    url="https://github.com/annnieglez/genai-travel-guide"
)