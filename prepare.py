import argparse
import logging
import json
import configparser

config = configparser.ConfigParser()
config.read('config.ini')
logging.basicConfig(format='%(asctime)s | %(levelname)s | %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


def load_json_data(path):
    with open(path) as f:
        json_data = json.load(f)  
    return json_data


def save_json_data(path, data):
    with open(path, 'w') as f:
        json.dump(data, f)


def parse_filter_params(raw_params):
    params = {}
    for param in raw_params:
        try:
            key, value = param.split(':')
        except ValueError:
            logger.warning('Incorrect options format: {}'.format(param))
        else:
            params[key] = set(value.split(','))
    return params   


def get_possible_values(json_data, options=None):
    values = {}
    for i in json_data:
        for k, v in i.items():
            if options and k not in options.keys():
                continue
            if k in values:
                values[k].add(v)
                continue
            values[k] = {v}
    return values


def filter_json(json_data, **kwargs):
    filtered = json_data
    for k, v in kwargs.items():
        filtered = [i for i in filtered if i.get(k) in v]
    return filtered


def main():
    # parse arguments
    parser = argparse.ArgumentParser(description='Filter JSON data by some keys and save to file')
    parser.add_argument('-i', '--input', help="Input file", default=config['DEFAULT']['INPUT'])
    parser.add_argument('-o', '--output', help="Output file", default=config['DEFAULT']['OUTPUT'])
    parser.add_argument('-v', '--values', action="store_true", help="Print all possible values")
    args, raw_params = parser.parse_known_args()

    #load json data
    logger.info('Loading data...')
    json_data = load_json_data(args.input)
    logger.info('Data loaded from {}'.format(args.input))

    # parse filter params
    params = parse_filter_params(raw_params)

    # show possible values
    if args.values:
        logger.info('Counting possible values...')
        print(get_possible_values(json_data, params))
        exit()
    
    # filter json data
    logger.info('Filtering by {}'.format(params))
    filtered_json = filter_json(json_data, **params)
    logger.info('Data filtered')

    # save filtered data if any
    if len(filtered_json) == 0:
        logger.warning('Found no matching objects. Please check filter parameters')
        exit()

    save_json_data(args.output, filtered_json) 
    logger.info('{} items saved to {}'.format(len(filtered_json), args.output)) 


if __name__ == '__main__':
    main()

