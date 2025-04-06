from setuptools import setup, find_packages
import sys
import platform



def install_sqlite():
    if os.environ['pysqlite3']:
        if platform.system() == "Linux":
            sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

install_sqlite()

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
