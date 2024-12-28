import argparse
from SphinxDocGenerator import SphinxDocGenerator
import os

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--interface', type=str, default='GUI', choices=['GUI', 'TUI'])
    parser.add_argument('--path', 
                        type=str, 
                        default=os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

    args = parser.parse_args()

    generator = SphinxDocGenerator(path=args.path, interfaceType=args.interface)

    generator.run()

if __name__ == "__main__":
    main()