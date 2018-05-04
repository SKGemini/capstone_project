import pandas as pd
import numpy as np
import itertools
from collections import Counter

def cleaned_data(df):
    '''
    INPUT: dataframe
    OUTPUT: dataframe
    For our Goodreads dataset, clean and organize the dataframe.
    '''
    df['average_rating'] = df['average_rating'].astype(float)
    df['num_works'] = df['num_works'].astype(float)
    df['pages'] = df['pages'].astype(float)
    df['month'] = df['month'].astype(float)
    df['year'] = df['year'].astype(float)

    df.columns = ['author', 'avg_rating', 'birth_date', 'book_id', 'death_date',
       'description', 'gender', 'hometown', 'image_url', 'is_series', 'isbn',
       'month', 'num_works', 'pages', 'rating_dist', 'tags', 'title', 'widget',
       'year']

    with open('booksmovies_list.txt',encoding="utf8") as f:
        allbooksmovies = f.read().splitlines()

    movies = []
    lst = list(df.title.values)
    for book in lst:
        if book.split('(')[0].strip() in allbooksmovies:
            movies.append(1)
        else:
            movies.append(0)

    df['has_movie'] = np.array(movies)

    tags = []
    for tag in list(df.tags.values):
        tags.append(tag.replace('[','').replace(']','').split(', '))
    all_tags = list(itertools.chain.from_iterable(tags)) #join list of lists
    counts = Counter(all_tags) #count frequency of tags
    mod_tag = []
    top_keys = set(dict(counts.most_common(500)).keys()) #find most common tags
    for tag in tags:
        mod_tag.append([x for x in tag if x in top_keys])
    genres = pd.DataFrame(np.array(mod_tag))
    genres.columns = ['mod_tags']
    mod_data = pd.merge(df,genres,left_index=True,right_index=True)
    s = pd.Series(mod_data['mod_tags'])
    all_books = pd.concat([mod_data.reset_index(),pd.get_dummies(s.apply(pd.Series).stack()).sum(level=0)],axis=1)

    data = all_books.drop(['index','book_id','author','birth_date','widget','isbn','hometown','image_url','tags','mod_tags'],axis=1)

    data['has_audiobook'] = data['audible'] + data['audio'] + data['audio-book'] + data['audio-books'] + data['audiobook'] + data['audiobooks']
    data['has_audiobook'] = data['has_audiobook'].apply(lambda x: 1 if x > 0 else 0)

    data['young_adult'] = data['ya'] + data['ya-books'] + data['ya-fiction'] + data['ya-fantasy'] + data['young-adult'] + data['young-adult-fiction'] + data['teen']
    data['young_adult'] = data['young_adult'].apply(lambda x: 1 if x > 0 else 0)

    data['childrens_fiction'] = data['childhood'] + data['children'] + data['children-s'] + data['children-s-books'] + data['childrens'] + data['childrens-books'] + data['kids'] + data['kids-books'] + data['juvenile']
    data['childrens_fiction'] = data['childrens_fiction'].apply(lambda x: 1 if x > 0 else 0)

    data['has_ebook'] = data['e-book'] + data['e-books'] + data['ebook'] + data['ebooks'] + data['kindle'] + data['kindle-books'] + data['nook']
    data['has_ebook'] = data['has_ebook'].apply(lambda x: 1 if x > 0 else 0)

    data['science_fiction'] = data['sci-fi'] + data['sci-fi-fantasy'] + data['fantasy-sci-fi'] + data['fantasy-scifi'] + data['science-fiction'] + data['science-fiction-fantasy'] + data['scifi'] + data['scifi-fantasy']
    data['science_fiction'] = data['science_fiction'].apply(lambda x: 1 if x > 0 else 0)

    data['is_classic'] = data['classic'] + data['classics'] + data['classic-literature']
    data['is_classic'] = data['is_classic'].apply(lambda x: 1 if x > 0 else 0)

    data['fantasy_fiction'] = data['fantasy'] + data['fantasy-sci-fi'] + data['fantasy-scifi']
    data['fantasy_fiction'] = data['fantasy_fiction'].apply(lambda x: 1 if x > 0 else 0)

    data['mystery_fiction'] = data['mysteries'] + data['mystery'] + data['mystery-crime'] + data['mystery-suspense'] + data['mystery-thriller']
    data['mystery_fiction'] = data['mystery_fiction'].apply(lambda x: 1 if x > 0 else 0)

    data['historical_fiction'] = data['historical'] + data['historical-fiction']
    data['historical_fiction'] = data['historical_fiction'].apply(lambda x: 1 if x > 0 else 0)

    data['non_fiction'] = data['non-fiction'] + data['nonfiction']
    data['non_fiction'] = data['non_fiction'].apply(lambda x: 1 if x > 0 else 0)

    data['dystopian_future'] = data['dystopia'] + data['dystopian']
    data['dystopian_future'] = data['dystopian_future'].apply(lambda x: 1 if x > 0 else 0)

    data = pd.merge(data, pd.get_dummies(data.gender),left_index=True,right_index=True)

    data['death_date'] = data['death_date'].apply(lambda x: 1 if x else 0)

    data['year'] = data['year'].fillna(data['year'].mean()).astype(int)

    data['is_series'] = data['is_series'].apply(lambda x: 1 if x else 0)

    years = pd.get_dummies(data.year)
    years_columns = list(years.columns)
    data = pd.merge(data,years,left_index=True,right_index=True)

    cleaned_data = data[['year','death_date','female','male','is_series','biography','autobiography','science_fiction','romance',
                     'is_classic','comedy','coming-of-age','fantasy_fiction', 'mystery_fiction','dystopian_future',
                     'historical_fiction','realistic-fiction','drama','horror','crime','suspense','paranormal',
                     'thriller','war','contemporary','chick-lit','action','young_adult','adult','animals','action',
                     'childrens_fiction','avg_rating','num_works','has_movie']+years_columns].fillna(0)

    return cleaned_data

#if __name__ == '__main__':
    #main()
