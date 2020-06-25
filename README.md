# EpiLight

EpiLight is a project which let the students know if a room is available or not

## Installation

To install this project follow the following commands :

    git clone https://github.com/XelaG/EpiLight2020.git;
    pip3 install pandas; pip3 install termcolor; pip3 install pyserial;

After this create your config file by following the next part 😀.

## Creating your config

To create your configuration, use the [example.json](https://github.com/XelaG/EpiLight2020/blob/master/exemple.json) file.


## Usage

./get_intra.py [token] [config_file_path]

    [token]    intra autologin token (https://intra.epitech.eu/[auth-********************/]) only the part between []

    [config_file_path] config file containing the rooms and corresponding IP for the LEDS (follow example.csv format)


