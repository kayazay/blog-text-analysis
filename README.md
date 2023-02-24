# Text Analysis Tool

This script is a text analysis tool that takes in a list of URLs to articles and returns a pandas dataframe containing various calculated variables such as the number of positive and negative words in the text, the polarity score, the subjectivity score, and the number of personal pronouns.

## Getting Started

### Prerequisites

- Python 3.x
- pandas
- requests
- re
- nltk
- bs4
- pyphen

### Installation

You can install the required packages by running the following command in your terminal:

```sh
pip3 install pandas requests nltk bs4 pyphen
```

### Usage

1. Clone or download the script.
2. Install the required packages.
3. Prepare a list of URLs to articles and save it in an Excel file. The file should be named `input.xlsx` and must have a column named URL containing the URLs.
4. Open the terminal and navigate to the directory where the script is saved.
5. Run the script by typing the following command in the terminal:

    ```sh
    python bkf.py
    ```

6. The script will output the resulting dataframe to the root directory.

## Functionality

The script performs the following tasks:

1. Imports the required libraries and sets up stopwords and positive/negative words for use.
2. Defines a function that scrapes the content of a given URL, tokenizes the content, and calculates various variables needed in the analysis.
3. Imports an Excel file containing URLs and applies the function to each URL to calculate the variables.
4. Outputs the resulting dataframe to the root directory.
