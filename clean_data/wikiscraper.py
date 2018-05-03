from bs4 import BeautifulSoup
import requests, csv, os, platform, unicodedata, json

def strip_accents(string):
    '''
    INPUT: string with accents
    OUTPUT: string with no accents
    Strip string of accents.
    '''
    return ''.join(c for c in unicodedata.normalize('NFD',string) if unicodedata.category(c) != 'Mn')

def scrape_table(url):
    '''
    INPUT: url
    OUTPUT: bs4.element.ResultSet
    Web scrape a wikipedia page for tables
    '''
    r = requests.get(url)
    soup = BeautifulSoup(r.content,"lxml")
    table_classes = {"class":["wikitable","infobox vevent","infobox biography vcard","infobox vbox", "infobox vcard"]}
    results = soup.findAll("table",table_classes)
    if not results:
        return ["Info", "missing"]
    else:
        return results

def urls_from_table(cell):
    '''
    INPUT: cell
    OUTPUT: url string or blank string
    Extract url otherwise blank
    '''
    base_url = 'https://en.wikipedia.org'
    urls = cell.findAll("a",href=True)
    if urls:
        valid_urls = []
        for a in urls:
            if 'wikipedia.org' in str(a['href']):
                valid_urls.append(a['href'])
            else:
                valid_urls.append(base_url+a['href'])
        return valid_urls
    else:
        return [""]

def clean_cells(table):
    '''
    INPUT: bs4.element.ResultSet
    OUTPUT: list
    Takes a wikitable and returns text and urls.
    '''
    cleaned_cells = []
    for row in table.findAll("tr"):
        cells = row.findAll(["th", "td"])
        for cell in cells:
            # Strip references from the cell
            references = cell.findAll("sup", {"class": "reference"})
            if references:
                for ref in references:
                    ref.extract()

            # Strip sortkeys from the cell
            sortkeys = cell.findAll("span", {"class": "sortkey"})
            if sortkeys:
                for ref in sortkeys:
                    ref.extract()

            # Strip footnotes from text and join into a single string
            text_items = cell.findAll(text=True)
            no_footnotes = [strip_accents(text) for text in text_items if text[0] != '[']

            url = urls_from_table(cell)
            cleaned = (''.join(no_footnotes)  # Combine elements into single string
                .replace('\xa0', ' ')  # Replace non-breaking spaces
                .replace('\n', ' ')  # Replace newlines
                .strip())
            cleaned_cells.append(cleaned.rsplit(',',1) + [url])
    return cleaned_cells

def infobox(table):
    '''
    INPUT: table
    OUTPUT: list
    Extracts information from wikitable.
    '''
    try:
        info = []
        for row in table(["th","tr"]):
            info.append([cell.text.strip().replace('\n',', ').replace('\xa0',' ') for cell in row(["th","td"])])
        return [x for x in info if x]
    except:
        return ['Info', 'missing']

def info(cells):
    '''
    INPUT: list
    OUTPUT: list of lists
    Extracts information from cells of tables.
    '''
    new = []
    for idx,cell in enumerate(cells):
        if idx % 2 == 0:
            book_info = [['Book',cell[0]],['Author', cell[1]]]
            urls = cell[-1]
            if 'https' in urls[0]:
                for url in urls:
                    book_table = scrape_table(url)[0]
                    book_info += infobox(book_table)[2:]
            else:
                book_info += [['Info','missing']]
            new.append([x for x in book_info if len(x) == 2])
        elif idx % 2 != 0:
            movie_info = [['Movie',cell[0]]]
            urls = cell[-1]
            if 'https' in urls[0]:
                movie_table = scrape_table(urls[0])[0] #Look at first movie
                movie_info += infobox(movie_table)[2:]
            else:
                movie_info += [['Info','missing']]
            new.append([x for x in movie_info if len(x) == 2])
    return new

def all_info(url, filename):
    '''
    INPUT: url, string
    OUTPUT: json file
    Extracts information from wikitables for a given url and writes it to a json file.
    '''
    wikitables = scrape_table(url)
    lists_dict = []
    for table in wikitables:
        cells = clean_cells(table)[2:]
        list_dict = []
        for each in info(cells):
            list_dict.append(dict(each))
        lists_dict += list_dict

    with open(filename+'.json','w') as f:
        json.dump(lists_dict,f)

def infobox_book(url):
    '''
    INPUT: url
    OUTPUT: list of lists
    Extract information from wikitables for a given url.
    '''
    try:
        page = requests.get(url, params={'action': 'raw'}).text
        info = []
        for line in page.splitlines():
            if line.startswith('| '):
                length = line.replace('{{','').replace('}}','').split('=')
                name = length[0].rstrip()

                if name == '| genre':
                    list_genre = length[1].replace('[[','').replace(']]','').lower().lstrip().split(',')
                    info.append(['genres',str(list_genre)])

                if name == '| country':
                    info.append(['country',length[1].replace(']]','').replace('[[','').strip()])

                if name == '| release_date':
                    info.append(['release_date',length[1]])

                if name == '| pages':
                    if length[1]:
                        page = [int(s) for s in length[1].split() if s.isdigit()][0]
                    else:
                        page = 'None'
                    info.append(['pages',page])

                if name == '| preceded_by' and length[1]:
                    info.append(['preceded_by','y'])

                if name == '| followed_by' and length[1]:
                    info.append(['followed_by','y'])
        return info
    except:
        return [['Info','missing']]

def infobox_author(url):
    '''
    INPUT: url
    OUTPUT: list of lists
    Extract information from wikitables for a given url.
    '''
    try:
        page = requests.get(url, params={'action': 'raw'}).text
        info = []
        for line in page.splitlines():
            if line.startswith('| '):
                length = line.replace('{{','').replace('}}','').split('=')
                name = length[0].rstrip()

                if name == '| birth_date':
                    d = ''.join(length[1:]).split('|')
                    date = '-'.join([str(s) for s in d if s.isdigit()][:3])
                    info.append(['birth_date',date])

                if name == '| death_date':
                    d = ''.join(length[1:]).split('|')
                    date = '-'.join([str(s) for s in d if s.isdigit()][:3])
                    info.append(['death_date',date])

                if name == '| spouse':
                    info.append(['is_married','y'])

                if name == '| children' and length[1]:
                    info.append(['has_children','y'])

                if name == '| nationality':
                    info.append(['nationality',length[1].replace(']]','').replace('[[','')])

                if name == '| alma_mater' and length[1]:
                    info.append(['has_alma_mater'],'y')
        return info
    except:
        return [['Info','missing']]

def retrieve_info(table):
    '''
    INPUT: bs4.element.ResultSet
    OUTPUT: list of lists
    Extract information from wikitables.
    '''
    base_url = 'https://en.wikipedia.org'
    #retrieve_info(table0)
    cleaned_cells = []
    for row in table.findAll("tr")[2:]:
        cells = row.findAll(["th", "td"])
        for index,cell in enumerate(cells):
            if index % 2 == 0:
                links = cell.findAll("a",href=True)
                urls = [link.get('href') for link in links]
                titles = [link.get('title') for link in links]
                text_items = cell.findAll(text=True)
                text = [text_items[0],text_items[-1]]
                all_info = []
                if urls:
                    if titles[0] == text[0]:
                        if 'wikipedia.org' in urls[0]:
                            all_info += [['book',text[0]]] + infobox_book(urls[0])
                        else:
                            all_info += [['book',text[0]]] + infobox_book(base_url+urls[0])

                    elif len(titles) == 1:
                        if titles[0] == text[1]:
                            if 'wikipedia.org' in urls[0]:
                                all_info += [['author',text[1]]] + infobox_author(urls[0])
                            else:
                                all_info += [['author',text[1]]] + infobox_author(base_url+urls[0])

                    elif len(titles) == 2:
                        if titles[1] == text[1]:
                            if 'wikipedia.org' in urls[1]:
                                all_info += [['author',text[1]]] + infobox_author(urls[1])
                            else:
                                all_info += [['author',text[1]]] + infobox_author(base_url+urls[1])
                    else:
                        all_info += [['Info','missing']]
                cleaned_cells.append(all_info)
    return cleaned_cells

def all_together(url):
    '''
    INPUT: url
    OUTPUT: list of lists
    Extract information from wikitables for a given url.
    '''
    wikitables = scrape_table(url)
    all_info = []
    for table in wikitables:
        all_info += retrieve_info(table)
    return [dict(each) for each in all_info]
#if __name__ == '__main__':
    #all_info(sysarg[0],sysarg[1])
