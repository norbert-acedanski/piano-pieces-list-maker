# piano-pieces-list-maker

# About The Project
Script allows me to create random list of piano pieces based on some factors for my piano concerts.
This project is a predecessor of __piano-list-preparation__.

# Built With
Python 3.9.10

# Getting started

### Working with piano-pieces-list-preparation:
The entire logic is located in the `main.py` file.  
It is function-based, not class based.  
Uses pandas to open and extract data from `.xlsx` file.  
After that filtering is applied to get only the pieces, composer/performer names and duration from the data collected.  
Main function that filters pieces is called `exclude_pieces`.  
It accepts data, that you want to get rid of the current piano pieces list.  
After removing all unnecessary pieces you can shuffle them based on desired duration or desired number of pieces.  
Then you can print it in a nice way.

# Usage
Allows tme to choose a list of piano pieces for upcoming concert based on requirements.

# Licence
Distributed under the MIT License. See LICENSE file for more information.
