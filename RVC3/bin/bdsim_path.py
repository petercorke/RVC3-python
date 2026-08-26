#!/usr/bin/env python3

import RVC3.models as models
from pathlib import Path

def main():
    print(Path(models.__file__).parent)

if __name__ == "__main__":
    main()
