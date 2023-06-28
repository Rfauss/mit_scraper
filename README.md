# mit_scraper
Downloading course material at https://ocw.mit.edu/ comes with a lot of bloat, this GUI uses the flet framework to find and scrape just the course material. 


<br/>

**Currently supported**:

Pdf files and zip folders. 

<br/>

**Planned Future Support**:

Mp4, jpeg, and plain text. Will evaluate other file formats as as necessary.

<br/>
<br/>

# Prerequisites

-Python >= 3.10
-

<br/>

-Python virtual environment manager (Anaconda recommended)
-
<br/>

-Pip
-

<br/>

-Git
-

<br/>
<br/>

# Installation 

Navigate to the folder you want to install to and clone repository into it using:  

```

git clone https://github.com/Rfauss/mit_scraper.git\
cd mit_scraper

```

Create a new virtual environment(Anaconda):

```
conda create --name mit_scraper python=3.10
```
Activate virtual environment(Anaconda):
```
conda activate mit_scraper
```

Install requirements:
```
pip install -r > requirements.txt
```

Run web scraper with:
```
python app.py 
```