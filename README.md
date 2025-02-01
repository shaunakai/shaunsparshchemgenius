# shaunsparshchemgenius
Steam in AI project

How to run the program

1. Prerequisite
   i. Copy all the files to target location
   ii. install all dependencies viz. 
      openai ( 1.54.4): making Open API calls
	    Pymupdf(1.24.13): For data extraction, analysis, conversion & manipulation of PDF (and other) documents
      Pandas(2.2.3): For data structures and data analysis tools
	    Scikit-learn(1.5.2): Data analysis
	    Sentence_tranformers(3.3.0): For vector embedding using text and images from an input
	    Flask( 3.1.0): Web framework for web app
	    Tkinter: Graphical User Interface
   iii. Create python virtual environment and activate it
   iv. copy the input file to local directory (c:\temp): https://openstax.org/details/books/chemistry-2e/
   v. You will need an openAI API key to run the program:
       replace line 39 in continousQueryV2.py with your key
          client = OpenAI(api_key="<YOUR_API_KEY>")
2. run continousQueryV2.py
    Ex: (.venv) PS C:\Shaunak\AI Tutor\tutor1> python .\continousQueryV2.py
3. To safeguard it from running too many prompts and use up credit we have put up a limit of 25 queries in one session.
   Change this limit at line 101 in continousQueryV2.py

