import matplotlib.pyplot as plt
import numpy as np
import itertools, pickle

def pickle_model(model, filename):
    '''
    INPUT: model instance, string
    OUTPUT: file
    Save your model as a pickle file
    '''
    #Example filename = 'GB_model.pk'
    pk.dump(model, open(filename, 'w'), 2)

def clean_string(string):
    '''
    INPUT: string
    OUTPUT: string
    For given string, remove unnecessary characters
    '''
    return re.sub(r'\W+', ' ', string)

def htmltostring(df,column):
    '''
    INPUT: dataframe, string
    OUTPUT: list of strings
    For a given dataframe and column, each column value is changed
    from HTML to string format
    '''
    description = []
    for each in df[column].values:
        soup = BeautifulSoup(each,"lxml")
        description.append(soup.get_text().replace('\xa0','').replace('\n',''))
    return description

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
    #all_info(sysarg[0],sysarg[1])
