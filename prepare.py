import argparse
import logging
import json
import configparser

config = configparser.ConfigParser()
config.read('config.ini')
logging.basicConfig(format='%(asctime)s | %(levelname)s | %(message)s', level=logging.INFO)
logger = logging.getLogger()


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
    parser.add_argument('-i', '--input', help="Specify input file")
    parser.add_argument('-o', '--output', help="Specify output file")
    parser.add_argument('-v', '--values', action="store_true", help="Print all possible values")
    args, raw_params = parser.parse_known_args()

    input_path = args.input if args.input else config['DEFAULT']['INPUT']
    output_path = args.output if args.output else config['DEFAULT']['OUTPUT']

    #load json data
    logger.info('Loading data...')
    with open(input_path) as f:
        json_data = json.load(f)  
    logger.info('Data loaded')

    # parse filter params
    params = parse_filter_params(raw_params)

    # show possible values
    if args.values:
        logger.info('Counting possible values...')
        print(get_possible_values(json_data, params))
        exit()
    
    # filter json data
    logger.info('Filtering by {}'.format(params))
    filtered = filter_json(json_data, **params)
    logger.info('Data filtered')

    # save filtered data if any
    if len(filtered) == 0:
        logger.warning('Found no matching objects. Please check filter parameters')
        exit()

    with open(output_path, 'w') as f:
        json.dump(filtered, f)

    logger.info('{} items saved to {}'.format(len(filtered), output_path))  


if __name__ == '__main__':
    main()

