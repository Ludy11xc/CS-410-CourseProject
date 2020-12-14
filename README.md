# CS-410-CourseProject

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

