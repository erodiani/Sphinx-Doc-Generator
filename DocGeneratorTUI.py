import os
import sys
source = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(source)
from DocGenerator import DocGenerator

def main():
    docGenerator = DocGenerator(interfaceType="TUI")
    docGenerator.run()

if __name__ == "__main__":
    main()