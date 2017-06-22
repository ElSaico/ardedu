import csv
import io

import flask as fl

app = fl.Flask(__name__)


@app.route('/')
def index():
    return fl.render_template('index.html')


@app.route('/', methods=['POST'])
def process_files():
    files = fl.request.files
    articles = {}

    # The csv module does not like that Flask opens everything in binary mode,
    # so we need this rather roundabout processing
    wos_file = io.StringIO(files['web-of-science'].read().decode('UTF16'),
                           newline=None)
    wos = csv.DictReader(wos_file, delimiter='\t')
    for article in wos:
        if article['DI']:
            article['source'] = 'web-of-science'
            articles[article['DI']] = article

    scopus_file = io.StringIO(files['scopus'].read().decode('UTF8'),
                              newline=None)
    scopus = csv.DictReader(scopus_file, delimiter=';')
    for article in scopus:
        if article['DOI'] and article['DOI'] not in articles:
            article['source'] = 'scopus'
            articles[article['DOI']] = article

    if files['proquest'].content_length > 0:
        pass

    return fl.render_template('index.html')


if __name__ == '__main__':
    app.run()
