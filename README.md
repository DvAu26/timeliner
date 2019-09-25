# Timeliner

PoC to have an automatic timeliner from hdd files and windows memory dump

Support just DOS/MBR magic type and the volatility memory dump capabilities.

## Install

Tested with Ubuntu 18.04 LTS updated and upgraded with 4Go and 2 procs

You have to install volatility from the official github and try it !

That will be updating to take all supported files by log2timeline

You just have to create 3 directories and update this constants (file_test.py):

IN
OUT
END
MEM
NOK

IN -> Put your own dd file
OUT -> you will have your plaso files and csv files (hdd and memory)
END -> Moving the file at the end of the thread.
MEM -> Moving the file at the end of the memory thread.
NOK -> Moving the unsupported files

## Using

   python3 file_test.py


## Next step

- Voltility extractor with 2 directories (dump and csv)
- Better dispatcher (rechercheur.py) class
- elif (timemem.py)
- and others ;) 
