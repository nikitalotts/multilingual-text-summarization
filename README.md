# Multilingual Text Summarization

This project is an implementation of [Luhn's Heuristic Method for text summarization](https://iq.opengenus.org/luhns-heuristic-method-for-text-summarization/)

The project was implemented in the 8th module of the 3rd year of [Higher IT School](https://hits.tsu.ru/), [Tomsk State University](https://www.tsu.ru/), [Tomsk](https://en.wikipedia.org/wiki/Tomsk).


## Algorithm

The project use Luhn's method which was first described in [this](http://web.stanford.edu/class/linguist289/luhn57.pdf) paper in 1957.

##  Installation

The project does not require installation, just download, unpack the files of this repository and install requirements*.

\* Run following command in shell:

``` 
$ pip install -r requirements.txt
```

## User manual

The system works through the following CLI command:

&nbsp;&nbsp;&nbsp;&nbsp;summarize:
```$ python path/to/summarizer.py summarize --parameter=value```

```
Summarizes the text file at the specified path.

Parameters:
    path (str): The path to the .txt file.
Returns:
    .txt file which contains summarized text from the input file
```


### References
* [Luhn’s Heuristic Method for text summarization](https://iq.opengenus.org/luhns-heuristic-method-for-text-summarization/)
* [A Statistical Approach to Mechanized Encoding and Searching of Literary Information](https://www.semanticscholar.org/paper/A-Statistical-Approach-to-Mechanized-Encoding-and-Luhn/076077a5771747ad7355120f1ba64cfd603141c6)


### Author
*Nikita Lotts, 3rd grade student in Tomsk State University (Tomsk)*