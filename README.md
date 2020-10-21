# FE_595_Homework_3-Sentiment_Sorting
Submission for FE 595 Homework #3- Sentiment Sorting

Disclaimer:\
This readMe assumes you are familiar with the purpose of this assignment.

Purpose:\
The file 'SentimentSorter.py' defines a SentimentSorter class containing all the functions necessary to read, analyse, and output sentiment/frequency results.

Data Preparation:\
SentimentSorter assumes that all data files passed to it are csv files in which the last two columns contain the Company Name and Company Purpose respectively.

Usage:
1) create a SentimentSorter object
2) call the 'loadData(path)' function with the path string to the folder containing your data files
3) to retrieve the N best and worse company ideas in the dataset call 'getNPolarizingCompanies(n)'
4) to retrieve the N most common words used in company purposes call 'getNMostCommonPurposeWords(n)'

Object Variables:
* data
  * a pandas dataframe containing all the Company Names and Company Purposes in the loaded data files

Function Descriptions:
* loadData(path)
  * path is the filepath string of the folder containing the data files
  * sets the 'data' variable of the SentimentSorter class to be a concatenated pandas dataframe of all files in the path location
* calcPurposeSentiment()
  * uses the textblob package to calculate sentiment scores for each company purpose
  * these purposes are appended to the class's 'data' variable as a new column
* getNBestCompanies(n)
  * sorts the dataset by sentiment score and returns a subset of the n highest-scoring companies
* getNWorstCompanies(n)
  * sorts the dataset by sentiment score and returns a subset of the n lowest-scoring companies
* printNPolarizingCompanies(n)
  * n has a default value of 1
  * calls 'getNBestCompanies' and 'getNWorstCompanies' respectively and prints out the purposes of the companies returned
* printNMostCommonPurposeWords(n, removeStopwords)
  * n has a default value of 10
  * removeStopwords has a default value of True
  * uses the nltk package to build a word frequency object on all text used in company purposes and prints the n most commonly used words
  * if removeStopwords is set to True, stopwords will not be considered in the frequency distribution
