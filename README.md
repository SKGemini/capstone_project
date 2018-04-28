# Write...Read...Action!

In light of current cinema, the market is demanding more and more material, thus many have turned to literary works as plot sources. While adapting them to screen is easier since a script is already in existence, translation from paper to film is difficult for certain genres and not every book is deemed "worthy" for such a resource-intensive project. Also, it's not feasible to produce a film adaption for every single book. So what features of a book entails it to have a cinematic adaption? This project will explore those features to see if one can predict the likelihood of a film adaptation for a book.

## Background

Given a certain year, there could be up to 70 films based on books. However, consider the following statistics:
```
- 129,864,880 books (and counting)
- 3,264,512 IMDB titles (and counting)
  - 30,548 titles with tag "Based On Novel"
```
Sources: [Mashable/Google](https://mashable.com/2010/08/05/number-of-books-in-the-world/#P1TH6qxOSmqg), [IMDb](https://www.imdb.com/search/keyword?keywords=based-on-novel)

Only 0.9% of cinematic titles are based on a novel and only 0.2% of books have a cinematic adaptation.

<p align="center">
  <img src="https://cdn-images-1.medium.com/max/1600/0*R7TtgnXa5a__b4RT.png">
  <caption align="bottom">{{Source: [The Writing Cooperative](https://writingcooperative.com/what-are-the-most-popular-literary-genres-6db5c69928cc)}}</caption>
</p>

I am appealing to two audiences: book/movie lovers and film producers. As an avid reader, I enjoy reading books of various genres and topics--some of which I deem worthy for a movie but hasn't been made into fruition. This project can highlight "hidden gems" or advocate for books. For film producers, this project potentially opens the possibility of pre-screening books to consider.

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
- publishing company
- number of pages
- genre
- bestsellers list
```

## Data Analysis
I explored the movies dataset to glean insights about how I should approach the books dataset. As this is a classification problem (movie or not), I used gradient boosting and logistic regression models for predictions. When exploring the books dataset, I plan to use ML algorithms to provide likelihoods for each book.
- [GoodReads Library](https://pypi.org/project/Goodreads/)




## Presentation
- Slideshow presentation about my data analysis (priority)
- Web app that operates like a recommender system where I can provide basic info about the work that I am interested in and see the likelihood that it will become a film (bonus)
