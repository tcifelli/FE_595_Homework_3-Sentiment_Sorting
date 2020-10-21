import pandas as pd
import os
from textblob import TextBlob #used for sentiment analysis
import nltk #used for word frequency

#contains all functions necessary for completion of the assignment
class SentimentSorter:
    def __init__(self):
        self.data = None #a pandas dataframe of company names and purposes

    #assumes all files in the path location have the name and purpose data as their last two columns respectively
    #concatenates those files into a dataframe
    def loadData(self, pathToDataFiles):
        allData = [pd.read_csv(file).iloc[:, -2:] for file in os.scandir(pathToDataFiles)]
        namedData = [frame.set_axis(['Company Name', 'Purpose'], axis=1, inplace=False) for frame in allData]
        self.data = pd.concat(namedData, ignore_index=True)

    #uses textblobs to retrieve sentiment scores for all company purposes
    def calcPurposeSentiment(self):
        self.data['Purpose Sentiment'] = pd.Series([TextBlob(purpose).sentiment.polarity for purpose in self.data["Purpose"]])

    #sorts and retrieves the n highest-scoring companies by sentiment score
    def getNBestCompanies(self, n):
        sortedData = self.data.sort_values(by=['Purpose Sentiment'])
        bestCompanies = sortedData.tail(n)
        return bestCompanies

    #sorts and retrieves the n lowest-scoring companies by sentiment score
    def getNWorstCompanies(self, n):
        if "Purpose Sentiment" not in self.data.columns:
            self.calcPurposeSentiment()

        sortedData = self.data.sort_values(by=['Purpose Sentiment'])
        worstCompanies = sortedData.head(n)
        return worstCompanies

    #prints the n best and worst company ideas in the dataset by sentiment score
    def printNPolarizingCompanyIdeas(self, n = 1):
        if "Purpose Sentiment" not in self.data.columns:
            self.calcPurposeSentiment()

        print("Best" + (" Idea:" if n == 1 else " Ideas:"))
        bestCompanies = self.getNBestCompanies(n)
        for purpose in bestCompanies['Purpose']:
            print(purpose)

        print("\nWorst" + (" Idea:" if n == 1 else " Ideas:"))
        worstCompanies = self.getNWorstCompanies(n)
        for purpose in worstCompanies['Purpose']:
            print(purpose)

    #uses nltk to build a word frequency distribution and return the n most common words used in company purposes
    #if 'removeStopwords' is True, stopwords will not be included in the distribution
    #referenced from https://stackoverflow.com/questions/28392860/print-10-most-frequently-occurring-words-of-a-text-that-including-and-excluding
    def printNMostCommonPurposeWords(self, n = 10, removeStopwords = True):
        if "Purpose Sentiment" not in self.data.columns:
            self.calcPurposeSentiment()

        allWords = nltk.tokenize.word_tokenize(self.data['Purpose'].str.cat(sep=" "))
        if removeStopwords:
            stopwords = nltk.corpus.stopwords.words('english')
            allWordDist = nltk.FreqDist(word.lower() for word in allWords if word not in stopwords)
        else:
            allWordDist = nltk.FreqDist(word.lower() for word in allWords)

        mostCommonWords = allWordDist.most_common(n)

        print("Most Common Purpose Words:")
        for word in mostCommonWords:
            print(word[0])

#example run of SentimentSorter functionality
def main():
    pathToDataFiles = "Data"
    sentimentSorter = SentimentSorter()
    sentimentSorter.loadData(pathToDataFiles)
    sentimentSorter.printNPolarizingCompanyIdeas()
    sentimentSorter.printNMostCommonPurposeWords()


if __name__ == "__main__":
    main()
