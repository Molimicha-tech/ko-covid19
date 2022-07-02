# Using Hashtags to Analysis Purpose and Technology Application of Open Source Project Related to COVID-19
## Overview
<b>Dataset and code for paper "Using Hashtags to Analysis Purpose and Technology A
pplication of Open Source Project Related to COVID-19"</b>

Under the background of covid-19, many related open source projects have 
emerged in the open source community. We want to know: What are the main 
uses of these open source projects? How have the concerns of the developers 
changed over time? What technologies are involved in the development of these 
projects and how are they related?

## Directory structure
<pre>ko_covid19:                      Root directory
│  data.db3:                          The dataset used in this study is stored in a SQLite database
│
├─Data in the analysis process:       Storage of intermediate data
│
├─Data preprocessing:                   
│      │ translate.py:                 Translate data from other languages into English
│      └─text_processing.py:           Delete stop words and other special characters
│
├─Synonym hashtag processing:
│      │ exist_tag_count.py:           Statistics on existing tags
│      │ get_similar_hashtags.py:      Get the 10 most semantically similar topic tags
│      │ get_word2vec_corpus.py:       Generating a word vector training corpus
│      │ replace_hashtags.py:          Use the synonym dictionary to replace the synonym
│      │ select_core_tags.py:          Source code of the selection of core topic tags
│      └─train_word2vec.py:            Train word2vec
│
├─Tag classification:
│      │ KNN.py:                       Source code of KNN
│      │ LogisticRegression.py:        Source code of LogisticRegression
│      │ model_select.py:              Source code of model test
│      │ NB.py:                        Source code of NB
│      │ RandomForest.py:              Source code of RandomForest
│      │ SVM.py:                       Source code of SVM
│      │ tag_classification.py:        Source code of classification
│      └─Text2vec.py:                  Source code of text to vector
│ 
└─Data analysis:                       
       │ association_analysis.py:      Source code of association analysis 
       │ Co-word_clustering.py:        Source code of co-word clustering
       │ hashtag_count.py:             Source code of tag statistics of tag extraction results
       └─word_frequency_analysis.py:   Source code of word frequency analysis
</pre>
## Contributions
The main contributions of this paper include the following. Analyzing the response of specific communities of practice to the pandemic will help facilitate better solutions for the community of practice in response to the COVID-19 and future pandemics. Summarizing the functionality of projects initiated by the IT community of practice during the pandemic and the technologies used will help create a larger pool of pre-existing technologies to address future crises. An examination of GitHub shows the differences in technology adoption during the pandemic between the communities of practice and the academic community. This can provide helpful insight into the rapid adoption of emerging technologies during the pandemic.
## Citation
Please cite the following paper if you use this code and dataset in your work.
>Liang Tian, Chengzhi Zhang. Using Hashtags to Analysis Purpose and Technology Application of Open-Source Project Related to COVID-19. Knowledge Organization, 2022 (in press). 
