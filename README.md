# Write...Read...Action!

Many films have turned to books as plot sources. It seems that any book can be considered to become a movie. But the translation from paper to film is difficult for certain genres and not every book is deemed "worthy" for such a huge project. Also, it's not feasible to produce a film adaption for every single book. So what features of a book entails it to have a film adaption? This project will explore those features to see if one can predict the likelihood of a film adaptation for a book.

## Background
I am appealing to two audiences: book/movie lovers and film producers. As an avid reader, I enjoy reading books of various genres and topics--some of which I deem worthy for a movie but hasn't been made into fruition. This project can highlight "hidden gems" or advocate for books. For film producers, this project potentially opens the possibility of pre-screening books to consider.

Similar projects to this one include:
- [Aligning Books to Movies](http://yknzhu.wixsite.com/mbweb) - provides descriptive explanations for visual content

## Data Collection

I collected data from the following resources:
```
- [List of fiction works made into feature films](https://en.wikipedia.org/wiki/Lists_of_fiction_works_made_into_feature_films)
- [GoodReads API](https://www.goodreads.com/api/index#search.books)
- [GoodReads Dataset from Kaggle](https://www.kaggle.com/zygmunt/goodbooks-10k)
- [New York Times API](https://developer.nytimes.com)
- [Book-Crossing Dataset](http://www2.informatik.uni-freiburg.de/~cziegler/BX/)
```

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

## Presentation
- Slideshow presentation about my data analysis (priority)
- Web app that operates like a recommender system where I can provide basic info about the work that I am interested in and see the likelihood that it will become a film (bonus)
