# Using Hashtags to Analysis Purpose and Technology Application of Open Source Project Related to COVID-19
## Overview
<b>Dataset and code for paper "Using Hashtags to Analysis Purpose and Technology A
pplication of Open Source Project Related to COVID-19"<b>
Under the background of covid-19, many related open source projects have 
emerged in the open source community. We want to know: What are the main 
uses of these open source projects? How have the concerns of the developers 
changed over time? What technologies are involved in the development of these 
projects and how are they related?
## Directory structure
<pre>ko_covid19:                      Root directory
│  data.db3:                          Dataset of this study
│
├─Data in the analysis process:       Store intermediate data
│
├─Data analysis:                      Store the code of data analysis
│      │association_analysis.py:      The code of association analysis 
│      │Co-word_clustering.py:        The code of co-word clustering
│      │hashtag_count.py:             Tag extraction results tag statistics
│      │word_frequency_analysis.py:   The code of word frequency analysis
│ 
└─ML:                                 Store the source code of the traditional models
    │  build_path.py:                 Create file paths for saving preprocessed data
    │  configs.py:                    Path configuration file
    │  crf.py:                        Source code of CRF algorithm implementation(Use CRF++ Toolkit)
    │  evaluate.py:                   Source code for result evaluation
    │  naivebayes.py:                 Source code of naivebayes algorithm implementation(Use KEA-3.0 Toolkit)
    │  preprocessing.py:              Source code of preprocessing function
    │  textrank.py:                   Source code of TextRank algorithm implementation
    │  tf_idf.py:                     Source code of TF-IDF algorithm implementation
    │  utils.py:                      Some auxiliary functions
    ├─CRF++:                          CRF++ Toolkit
    └─KEA-3.0:                        KEA-3.0 Toolkit
</pre>
## 3. Contributions
#####   The main contributions of this paper include the following. Analyzing the response of specific communities of practice to the pandemic will help facilitate better solutions for the community of practice in response to the COVID-19 and future pandemics. Summarizing the functionality of projects initiated by the IT community of practice during the pandemic and the technologies used will help create a larger pool of pre-existing technologies to address future crises. An examination of GitHub shows the differences in technology adoption during the pandemic between the communities of practice and the academic community. This can provide helpful insight into the rapid adoption of emerging technologies during the pandemic.
