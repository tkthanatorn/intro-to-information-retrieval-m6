# Assignment Module 6

## Setup Steps
1. Install dependencies from `requirements.txt` by following command line:
```bash
pip install -r requirements.txt
```
2. Running the project through this command line:
```bash
# first choice
python main.py

# or second choice
make run
```

## Project Routing

### Search through Elasticsearch
Path: `http://localhost:5000/search/elastic` <br>
| **Query Key** | **Query Type** | **Query Required** |
|---------------|----------------|--------------------|
| query         | str            | required           |

### Search through Web Indexer
Path: `http://localhost:5000/search/manual` <br>
| **Query Key** | **Query Type** | **Query Required** |
|---------------|----------------|--------------------|
| query         | str            | required           |

### Search through Web Indexer, which combined BM25 and PageRank
Path: `http://localhost:5000/search/manual/page-rank` <br>
| **Query Key** | **Query Type** | **Query Required** |
|---------------|----------------|--------------------|
| query         | str            | required           |

## Discuss about how this new mix of scores makes finding things better or worse.
When I use `BM25` and `PageRank` together, I found the order of the result is too much difference when used `PageRank` because of when integrate `PageRank` and `BM25` together the weight of score of `PageRank` affect to the results example when I query about `software engineer` with `/search/manual` the results with the text "software engineer" are stay nearby, but when I query through `/search/manual/page-rank` the results will spread of other too much.