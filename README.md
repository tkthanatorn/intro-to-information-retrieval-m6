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

### Search through Elasticsearch
Path: `http://localhost:5000/search/elastic` <br>
| **Query Key** | **Query Type** | **Query Required** |
|---------------|----------------|--------------------|
| query         | str            | required           |