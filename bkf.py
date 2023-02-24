# importing of libraries
import requests, re, nltk
from nltk.tokenize import sent_tokenize
from bs4 import BeautifulSoup
import pandas as pd
import pyphen


# Import positive words here
with open('./txts/positive-words.txt', 'r', encoding='latin-1') as f:
    pos_txt = re.findall(r'\w+', f.read())

# Import negative words here
with open('./txts/negative-words.txt', 'r', encoding='latin-1') as f:
    neg_txt = re.findall(r'\w+', f.read())

# Import stopwords here
nltk.download(['punkt', 'stopwords'])
stpwords = nltk.corpus.stopwords.words('english')
for file in ("Auditor", "Currencies", "DatesandNumbers", "Generic", "GenericLong", "Geographic", "Names"):
    with open('./txts/StopWords_'+file+'.txt', 'r', encoding='latin-1') as f:
        all_words = re.findall(r'\w+', f.read())
        each_stpword = [word for word in all_words if word.isupper()]
        stpwords += each_stpword
stpwords = [stp.lower() for stp in stpwords]


def scrape_tokenize(link):
    '''
    Make a request to the blog and get the page content.
    '''
    HEADERS = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "en-US,en;q=0.9",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/106.0.0.0 Safari/537.36 "
    }
    try:
        page = requests.get(link, headers=HEADERS)
        soup = BeautifulSoup(page.content, 'html.parser')
        soup_content = soup.select('div.td-post-content')
        article = [part.get_text('. ', strip=True) for part in soup_content][0]
        article = article.lower()
    except:
        return (None,) * 12
    '''
    Work on text gotten to calculate and derive variables needed in this analysis.
    '''
    # tokenize text collected into words
    tokenized_words = re.findall(r'\b\w+\b', article)
    # remove stopwords
    removed_stpwords = [word for word in tokenized_words if word not in stpwords]
    # total length of characters
    char_len = sum([len(char) for char in tokenized_words])
    # number of syllables per word
    dic = pyphen.Pyphen(lang='en')
    syllable_per_word = [dic.inserted(word).count('-')+1 for word in tokenized_words]
    '''
    We now try to get the actual variables that are required.
    There are about 10 in total.
    '''
    # 8. number of words with more than 2 syllables
    cmplx_word_count = sum([1 for syll in syllable_per_word if syll>2])
    # 9. number of words of the text
    word_count = len(tokenized_words)
    # 1. number of positive words in text that excludes stopwords
    pos_count = sum([1 for word in removed_stpwords if word in pos_txt])
    # 2. number of negative words in text that excludes stopwords
    neg_count = sum([1 for word in removed_stpwords if word in neg_txt])
    # 3. calculate polarity score
    polarity_score = (pos_count - neg_count) / (pos_count + neg_count)
    # 4. calculate subjectivity score
    subjectivity_score = (pos_count + neg_count) / (word_count)
    # 5. average length of sentence
    avg_sen_len = word_count / len(sent_tokenize(article))
    # 6. percentage of complex words
    percent_complex_words = cmplx_word_count / word_count
    # 7. fog index
    fog_index = 0.4 * (avg_sen_len + percent_complex_words)
    # 10. syllables per word
    avg_syllables = sum(syllable_per_word) / word_count
    # 11. number of personal pronouns
    personal_pronouns = ('I', 'me', 'you', 'he', 'him', 'she', 'her', 'it', 'we', 'us', 'they', 'them')
    pronoun_count = sum(1 for word in tokenized_words if word in personal_pronouns)
    # 12. average word length
    avg_word_length = char_len / word_count
    '''
    Return all the variables gotten.
    '''
    return pos_count, neg_count, polarity_score, subjectivity_score, avg_sen_len, percent_complex_words, fog_index, \
        cmplx_word_count, word_count, \
        avg_syllables, pronoun_count, avg_word_length

''''
Import the input xlsx file, get links and get respective scores.
Then output the resulting dataframe to the root directory.
'''
if __name__=='__main__':
    df = pd.read_excel('./input.xlsx')
    df = df[:5]
    # apply function to the url column
    applied_df = df['URL'].apply(scrape_tokenize)
    # create new dataframe from applied values
    df_vars = pd.DataFrame(applied_df.tolist(),columns=[
        'POSITIVE_SCORE','NEGATIVE_SCORE','POLARITY_SCORE','SUBJECTIVITY_SCORE','AVG SENTENCE_LENGTH','PERCENTAGE_OF_COMPLEX WORDS','FOG_INDEX',
        'COMPLEX_WORD_COUNT','WORD_COUNT',
        'SYLLABLE_PER WORD','PERSONAL_PRONOUNS','AVG WORD_LENGTH',
    ])
    # join resulting dataframe with input dataframe
    df_join = df.join(df_vars)
    df_done = df_join.applymap(lambda x: round(x,2) if isinstance(x, float) else x)
    df_done.to_excel('./result.xlsx', index=False)
