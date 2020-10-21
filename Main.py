import pandas as pd
import os
from textblob import TextBlob
import nltk

class SentimentSorter:
    def __init__(self):
        self.data = None
        self.purposeSentiment = None

    def loadData(self, pathToDataFiles):
        allData = [pd.read_csv(file).iloc[:, -2:] for file in os.scandir(pathToDataFiles)]
        namedData = [frame.set_axis(['Company Name', 'Purpose'], axis=1, inplace=False) for frame in allData]
        self.data = pd.concat(namedData, ignore_index=True)

    def calcPurposeSentiment(self):
        self.data['Purpose Sentiment'] = pd.Series([TextBlob(purpose).sentiment.polarity for purpose in self.data["Purpose"]])

    def getNBestCompanies(self, n):
        sortedData = self.data.sort_values(by=['Purpose Sentiment'])
        bestCompanies = sortedData.tail(n)
        return bestCompanies

    def getNWorstCompanies(self, n):
        sortedData = self.data.sort_values(by=['Purpose Sentiment'])
        worstCompanies = sortedData.head(n)
        return worstCompanies

    def printNPolarizingCompanies(self, n = 1):
        print("Best" + (" Idea:" if n == 1 else " Ideas:"))
        bestCompanies = self.getNBestCompanies(n)
        for purpose in bestCompanies['Purpose']:
            print(purpose)

        print("\nWorst" + (" Idea:" if n == 1 else " Ideas:"))
        worstCompanies = self.getNWorstCompanies(n)
        for purpose in worstCompanies['Purpose']:
            print(purpose)

    #referenced from https://stackoverflow.com/questions/28392860/print-10-most-frequently-occurring-words-of-a-text-that-including-and-excluding
    def printNMostCommonPurposeWords(self, n = 10, removeStopwords = True):
        allWords = nltk.tokenize.word_tokenize(self.data['Purpose'].str.cat(sep=" "))
        if removeStopwords:
            stopwords = nltk.corpus.stopwords.words('english')
            allWordDist = nltk.FreqDist(word.lower() for word in allWords if word not in stopwords)
        else:
            allWordDist = nltk.FreqDist(word.lower() for word in allWords)
        mostCommonWords = allWordDist.most_common(10)

        print("Most Common Purpose Words:")
        for word in mostCommonWords:
            print(word[0])

def main():
    pathToDataFiles = "Data"
    sentimentSorter = SentimentSorter()
    sentimentSorter.loadData(pathToDataFiles)
    sentimentSorter.calcPurposeSentiment()
    sentimentSorter.printNPolarizingCompanies()
    sentimentSorter.printNMostCommonPurposeWords()


if __name__ == "__main__":
    main()
