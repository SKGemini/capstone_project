# Write...Read...Action!

In light of current cinema, many have turned to literary works as plot sources. While adapting them to screen is easier since a script is already in existence, translation from paper to film is difficult for certain genres and it's not practical to produce a cinematic adaption for every single book. I explored which features help predict the likelihood of a film adaptation for a book. 

As an avid reader, I enjoyed doing a deep dive into the research and identify books of various genres and topics--some of which I deem worthy for a movie but hasn't been made into fruition. This project can highlight "hidden gems" and help entities such as publishing companies and film production studios as a method of pre-screening manuscripts/books.

## Background

In a given year, there could be up to 70 films based on books. However, consider the following statistics:
```
- 129,864,880 books (and counting)
- 3,264,512 IMDB titles (and counting)
  - 30,548 titles with tag "Based On Novel"
```
Sources: [Mashable/Google](https://mashable.com/2010/08/05/number-of-books-in-the-world/#P1TH6qxOSmqg), [IMDb](https://www.imdb.com/search/keyword?keywords=based-on-novel)

Only 0.9% of cinematic titles are based on a novel and only 0.2% of books have a cinematic adaptation. 

<p align="center">
  <img src="https://cdn-images-1.medium.com/max/1600/0*R7TtgnXa5a__b4RT.png">
</p>

Similar projects and articles about books becoming movies:
- [Aligning Books to Movies](http://yknzhu.wixsite.com/mbweb) - provides descriptive explanations for visual content
- [Book Word Count vs Movie Length](https://www.overthinkingit.com/2013/08/12/book-word-count-movie-length-2/)

## Data Collection

I collected data from the following resources:

- [List of fiction works made into feature films](https://en.wikipedia.org/wiki/Lists_of_fiction_works_made_into_feature_films)
- [GoodReads API](https://www.goodreads.com/api/index#search.books)
- [GoodReads Dataset from Kaggle](https://www.kaggle.com/zygmunt/goodbooks-10k)
- [New York Times API](https://developer.nytimes.com)
- [Book-Crossing Dataset](http://www2.informatik.uni-freiburg.de/~cziegler/BX/)
- [IMDb](https://www.imdb.com/?ref_=nv_home)

Features considered:
```
- year of publication
- number of pages
- genre such as romance and historical fiction
- information about the author such as number of works in existence
- average Goodreads rating of book
- description of book
```

## Data Analysis
As this is a classification problem (has movie or not), I used logistic regression models for my predictions.

## Presentation
- pdf link to presentation
- web app
