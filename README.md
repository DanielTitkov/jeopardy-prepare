# json-prepare

Loads data from JSON files, filters it by multiple keys and saves to file. You can get demo data from here: [Reddit Jeopardy data](https://www.reddit.com/r/datasets/comments/1uyd0t/200000_jeopardy_questions_in_a_json_file/). 

## Getting started

### Prerequisites

Works with Python 3.5.x and higher. Does not require any additional libraries.
![Little kitty](https://media.giphy.com/media/3oKIPnAiaMCws8nOsE/giphy.gif)

### Installing

Just copy repo to your computer.

```
git clone https://github.com/DanielTitkov/json-prepare.git
```

## Using json-prepare

```
usage: python prepare.py [-h] [-i INPUT] [-o OUTPUT] [-v]

Filter JSON data by some keys and save to file

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        Specify input file
  -o OUTPUT, --output OUTPUT
                        Specify output file
  -v, --values          Print all possible values
  <filter_params>       Filter keys in specific format: <key>:<value1>,<value2> <key2>:<value>
```
Path to the your file with JSON data to process as well as output path can be also specified in config.ini file.
To filter JSON data by some keys, run program as shown bellow. Keys that are not present in the data will be ignored.
```
python prepare.py category:HISTORY
```
This will give you items from your JSON data with the key "category" equals to "HISTORY".
You can also specify multiple keys and several values separated by comma (*with no whitespace!*)
```
python prepare.py category:HISTORY,"COMPLETE THE BIBLE QUOTE" show_number:4680
```
This will give you items with the category "HISTORY" **OR** "COMPLETE THE BIBLE QUOTE" **AND** show number 4680.
Please note, that values consisting of several words must be provided within double qoutes. 
If the string itself contains double qoutes, you can escape them with backslash.
```
python prepare.py category:"\"C\" SERPENTS","I'M BORED"
```
#### Checking possible values
If you wonder what values you can use to filter your json data, you may run json-prepare with **-v** flag. In won't save any data, but will print out all possible values for all keys in your data (be warned, output may be overwhelming). 
If you use **-v** with filter options like **category:HISTORY**, values will be printed out only for the specified key, e.g. category. Mind you, filter option must be provided in proper format anyway, or they will be ignored.

## License

This project is licensed under the Unlicense - see the [LICENSE.md](LICENSE.md) file for details
