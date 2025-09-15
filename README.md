# ASUS BIOS Flashback Name Extractor

A command-line utility to extract the correct filename required for the **ASUS USB BIOS Flashback** feature from an official BIOS `.CAP` file.

## The Problem

Certain ASUS motherboards with the USB BIOS Flashback feature require the BIOS `.CAP` file to be renamed to a specific, shortened model name before it can be flashed without a CPU or RAM. For example, `Pro-WS-W790E-SAGE-SE-ASUS-1801.CAP` might need to be renamed to `PWW790SG.CAP`.

This required name is embedded within the BIOS file itself. This script automates the process of finding and extracting that name, eliminating guesswork and preventing failed flashes due to incorrect filenames.

## Requirements

- Python 3.x

## Usage

Run the script from your terminal and provide the path to the BIOS `.CAP` file as an argument.

```sh
python bios_extractor.py <path_to_your_bios_file.CAP>
```

The script will print the correct filename to the console if successful.


```sh
$ python bios_extractor.py Pro-WS-W790E-SAGE-SE-ASUS-1801.CAP
PWW790SG.CAP
```

You would then rename the file Pro-WS-W790E-SAGE-SE-ASUS-1801.CAP to PWW790SG.CAP and copy it to your USB drive.

