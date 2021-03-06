# -*- coding: utf-8 -*-
import click
import logging
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
from pathlib import Path
from dotenv import find_dotenv, load_dotenv


@click.command()
@click.argument('input_filepath', type=click.Path(exists=True))
@click.argument('output_filepath', type=click.Path())
def main(input_filepath, output_filepath):
    """ Runs data processing scripts to turn raw data from (../raw) into
        cleaned data ready to be analyzed (saved in ../processed).
    """
    logger = logging.getLogger(__name__)
    logger.info('making final data set from raw data')

    print(input_filepath)
    process_articles(input_filepath, print_article)


def process_articles(articles_file, f):
    tree = ET.iterparse(articles_file)
    for event, element in tree:
        if element.tag == 'article':
            attrs = element.attrib
            article_id = attrs['id']
            # published = attrs['published-at']
            xml = ET.tostring(element, encoding="utf-8", method="xml").decode()
            article = dict(
                id=article_id,
                xml=xml,
                # published_at=published,
                et=element,
            )
            f(article)
            del article['et']


def print_article(article):
    print(article)


def write_text(article):
    soup = BeautifulSoup(xml)
    print(soup.text) 


def save_to_db(article):
    pass


if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    # not used in this stub but often useful for finding various files
    project_dir = Path(__file__).resolve().parents[2]

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    load_dotenv(find_dotenv())

    main()
