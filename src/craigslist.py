import argparse
import logging
import requests

logging.basicConfig(level='INFO')
logger = logging.getLogger(__name__)

from bs4 import BeautifulSoup
from constants import (
    CL_BASE,
    CL_CITIES,
    CL_BASE_SEARCH,
    CL_BASE_TAIL
)

from utils.url_util import cl_product


def construct_url(metro, product):
    """
    Construct a craigslist compliant URL for a given metro and product
    :param metro:
    :param product:
    :return:
    """
    serialize_product = cl_product(product)
    out_url = f'https://{metro}.{CL_BASE}{CL_BASE_SEARCH}{serialize_product}&{CL_BASE_TAIL}'

    return out_url


def get_soup(request_url):
    """
    Using Url constructed, get top level html from craigslist.org
    :param request_url:
    :return:
    """
    req = requests.get(request_url)
    req_content = req.content

    soup = BeautifulSoup(req_content, 'html.parser')

    return soup


def run(args_dict):
    """
    Pseudo handler for craigslist scraping from given args
    :param args_dict:
    :return:
    """
    metroarea = args_dict['metroarea']
    product = args_dict['product']
    fout = construct_url(metroarea, product)

    # Get URL constructed
    logger.info(f'Url constructed: {fout}')

    cl_soup = get_soup(fout)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Find prices for product based on metropolitan area'
    )
    parser.add_argument(
        '-m', '--metroarea',
        required=True,
        type=str,
        help='Metropolitan area to search caigslist.org for'
    )
    parser.add_argument(
        '-p', '--product',
        required=True,
        type=str,
        help='Product to find prices for'
    )

    args_dict = vars(parser.parse_args())

    if args_dict['metroarea'] not in CL_CITIES:
        logger.error(' Metropolitan Area not available')

    run(args_dict)