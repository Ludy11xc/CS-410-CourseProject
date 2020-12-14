# CS-410-CourseProject

### Presentation

https://mediaspace.illinois.edu/media/1_8aiq79tk

### Objective

Reproducing results from a paper: 
"Mining Causal Topics in Text Data: Iterative Topic Modeling with Time Series Feedback"

### Problems

1. Data: The first problem encountered was obtaining the data in order used to produce the results.  Unfortunately, I missed the piazza post to request access to the NY times dataset.  So, I wrote a webscraper (data_scraper.py) to scrape articles from NY Times, which I was able to save in the data folder.  I only saved results which contained "bush" or "gore" so it was a manageable size to be uploaded.  For the Market data, I manually copied the data into a csv.

2. Scope: The second problem encountered was the scope of the problem.  After reading through the paper and doing a couple of hours of research, I discovered this would be a very complex result to produce, especially working as an individual, and factoring in my own gaps of knowledge involving the algorithm to be implemented.  I was unable to completely recreate the algorithm using time stamp series feedback.

### Results

I used an LDA model to find the top 3 words from topics discovered from the relevant documents.  These are the results.

| Top 3 Words in Significant Topics |
| ---------- |
| party nader vote |
| tax plan social |
| oil price juniper |
| street music sunday |
| company court death |
| debate right candidate |
| city game old |
| clinton cheney know |
| school test student |
| clinton lazio mr_clinton |

Looking at these words, we can definitely see some topics that were very relevant to the presidential election.  Many of these words were also mined from the algorithm used in the paper.

### Setup/Run Code

\* If desired, set up virtual env. Then, to set up the code: \*

```
# Clone repo, could take a couple seconds-minutes depending on download speed because of data (20-30 MB)
git clone https://github.com/Ludy11xc/CS-410-CourseProject.git

# Navigate into repo
cd CS-410-CourseProject

# Install dependencies.  If EnvironmentError is encountered, rerun with --user
pip install -r requirements.txt
```

If you would like to run the websraper, you can with 
```
python data_scrapper.py
```
However, know that it will most likely take multiple hours to complete, and the data has already been scraped and is present in the data folder.

Then to run the code,

```
# Run this to get results from current model
python lda.py

# OR, run this to train a new model and get new results
python lda.py train
```
