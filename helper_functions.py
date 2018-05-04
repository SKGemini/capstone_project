import matplotlib.pyplot as plt
import numpy as np
import itertools, pickle, string
from sklearn.metrics import confusion_matrix
from bs4 import BeautifulSoup
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.decomposition import NMF, LatentDirichletAllocation
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer

# Write out to file
def pickle_model(model, filename):
    '''
    INPUT: model instance, string
    OUTPUT: file
    Save your model as a pickle file
    '''
    #Example filename = 'GB_model.pk'
    pk.dump(model, open(filename, 'w'), 2)

def write_to_file(filename,lst):
    '''
    INPUT: string, list
    OUTPUT: file
    Take in a string as filename and list and writes it to a text file.
    '''
    with open(filename,'w') as f:
        for item in lst:
            try:
                f.write(item)
                f.write(os.linesep)
            except:
                pass

# Cleaning string format
def clean_string(string):
    '''
    INPUT: string
    OUTPUT: string
    For given string, remove unnecessary characters
    '''
    return re.sub(r'\W+', ' ', string)

def htmltostring(df,column):
    '''
    For a given dataframe and column, each column value is changed
    from HTML to string format

    INPUT: dataframe, string

    OUTPUT: list of strings
    '''
    description = []
    for each in df[column].values:
        soup = BeautifulSoup(each,"lxml")
        description.append(soup.get_text().replace('\xa0','').replace('\n',''))
    return description

# NLP
def tokenize(doc):
    '''
    INPUT: string
    OUTPUT: list of strings
    Tokenize and stem/lemmatize the document.
    '''
    snowball = SnowballStemmer('english')
    return [snowball.stem(word) for word in word_tokenize(doc.lower())]

def vectorize(df,n_features=1000):
    '''
    INPUT: DATAFRAME
    OUTPUT: vectorized description
    Grab description from DataFrame and return vectorized description
    '''
    description = htmltostring(df,'description')
    vect = TfidfVectorizer(stop_words='english',max_df=0.95, min_df=2,max_features=n_features,tokenizer=tokenize)
    desc_vect = vect.fit_transform(description)

    return vect, desc_vect

def print_top_words(model, feature_names, n_top_words):
    '''
    INPUT: classifier, list of strings, integer
    OUTPUT: None
    '''
    for topic_idx, topic in enumerate(model.components_):
        message = "Topic #%d: " % topic_idx
        message += " ".join([feature_names[i]
                             for i in topic.argsort()[:-n_top_words - 1:-1]])
        print(message)
    print()

# For confusion matrix and performance metrics
def standard_confusion_matrix(y_true, y_pred):
    """Make confusion matrix with format:
                  -----------
                  | TP | FP |
                  -----------
                  | FN | TN |
                  -----------
    Parameters
    ----------
    y_true : ndarray - 1D
    y_pred : ndarray - 1D
    Returns
    -------
    ndarray - 2D
    """
    [[tn, fp], [fn, tp]] = confusion_matrix(y_true, y_pred)
    return np.array([[tp, fp], [fn, tn]])

def plot_confusion_matrix(cm, classes,normalize=False,title='Confusion matrix',cmap=plt.cm.Blues):
    '''
    INPUT: confusion matrix, list of labels, boolean, string
    OUTPUT: plot
    This function prints and plots the confusion matrix.
    Normalization can be applied by setting `normalize=True`.
    '''
    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        print("Normalized confusion matrix")
    else:
        print('Confusion matrix, without normalization')

    print(cm)

    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=45)
    plt.yticks(tick_marks, classes)

    fmt = '.2f' if normalize else 'd'
    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, format(cm[i, j], fmt),
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")

    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')

def movies_matrix(x_test,y_test,y_pred):
    '''
    INPUT: numpy array, numpy array, numpy array
    OUTPUT: plot
    '''
    #Make confusion matrix
    plot_confusion_matrix(standard_confusion_matrix(y_test,y_pred),classes=['movie','not_movie'],title='Confusion matrix, without normalization')
    outcomes = standard_confusion_matrix(y_test,y_pred).ravel() #np.array([[tp, fp], [fn, tn]])
    tp, fp, fn, tn = outcomes[0], outcomes[1], outcomes[2], outcomes[3]
    precision = tp / (tp + fp)
    recall = tp / (tp + fn)
    f1_score = 2 * precision * recall / (precision + recall)
    print("Accuracy: {}".format(log.score(x_test,y_test))) #Print accuracy score
    print("Precision: {}".format(precision))
    print("Recall: {}".format(recall))
    print("F1 Score: {}".format(f1_score))

def sampling(df,feature,majority_n, minority_n, sample_type='both'):
    '''
    INPUT: dataframe, string, integer, integer, string
    OUTPUT: dataframe, dataframe
    Take in dataframe and resample your data.
    '''
    df_majority = df[df[feature] == 0]
    df_minority = df[df[feature] == 1]

    df_minority_upsampled = resample(df_minority, replace = True, n_samples=majority_n,random_state=123)
    df_upsampled = pd.concat([df_majority,df_minority_upsampled])

    df_majority_downsampled = resample(df_majority, replace=False,n_samples=minority_n,random_state=123)
    df_downsampled = pd.concat([df_majority_downsampled,df_minority])

    if sample_type.lower() == 'up':
        return df_upsampled
    elif sample_type.lower() == 'down':
        return df_downsampled
    else:
        return df_upsampled, df_downsampled

#if __name__ == '__main__':
    #main()
