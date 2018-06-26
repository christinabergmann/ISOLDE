# ISOLDE
Here you can find the materials for the practical exercises and demonstrations of the Computational Modelling tutorial at ISOLDE 2018 in Potsdam. 


### Which sort of files are in this repository?

There are five different types of files, which can be identified by their file type:
1. '.pdf' The lecture slides from both days of the tutorial, which you can open for example with Adobe Acrobat Reader.  
2. '.ipynb' The Jupyter notebooks from the practical part, for instructions how to open and edit them see below.  
3. '.cor' Corpus data for the statistical learning exercise. Both corpora were hand-created, the first is based on descriptions from the source paper (Saffran, Aslin, & Newport, 1996), the second one is a syllabified (but orthographic) representation of Experiment 3b in pelucchi, Hay, & Saffran (2009). The files are in a simple text format, and you can open them with any text editor.     
4. '.csv' corpus and uptake data for the vocabulary learning exercise (one packed in a '.zip' file), the corpora were obtained as follows: The vocabulary data was downloaded from Wordbank: http://wordbank.stanford.edu/analyses?name=item_data and the input corpus is the Brent corpus from CHILDES, which can be downloaded in a convenient format via http://gandalf.talkbank.org:8080/childes2csv/  You can open the files with spreadsheet software such as Excel.  
5. '.py' files contain the "solution" to the exercises in simple python format. You can open them with any text editor.


### How to complete the practical exercises and demos?

There are two options to complete the exercises and run the demos.

*Option 1: Offline, using Anaconda (or similar)*

1. Download Anaconda (which contains all parts of python you will need and more): 
https://www.anaconda.com/download/
(Graphical installer available for Windows and iOS, no admin rights necessary, all scripts have been tested with python 3.6)  
2. Download this repository (button top left: download zip) and unpack it.    
3. Open Anaconda, launch jupyter
4. A browser should open, navigate in the browser to the directory where you saved the extracted files
5. Open the notebooks (a new tab will appear), they are the files ending with ".ipynb"

For the statistical learning exercise, the "solutions" are in the file "bigram_model_ref.py"

*Option 2: Online, using mybinder*

1. Open this link in your browser: [![Binder](https://mybinder.org/badge.svg)](https://mybinder.org/v2/gh/christinabergmann/ISOLDE/master)
2. Open the notebooks (a new tab will appear), they are the files ending with ".ipynb"


**Note**: Your edits will not be saved, download the file to keep your changes to it.

