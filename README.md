# Butcher Tools

This repository holds a collection of tools and scripts used during development of *Grand Theft Auto: The Harwood Butcher*, a modification for Grand Theft Auto: Vice City.
All scripts were created for Python 2.x.

## Tools included:

**pathattach** - scripts for managing IPL and IDE path entries

- pathdetach - converts IDE paths to IPL (detached) paths

  USAGE:  
  ```python pathdetach.py [--debug] [--ideinfo] [--mksection] idefile.ide iplfiles.ipl...```  
  `--debug` - include info about original model and ID in output path definitions  
  `--ideinfo` - include extra metadata in flags field of output paths to allow `pathattach` tool to re-attach modified paths properly (use `calcflag.py` to generate these flags)  
  `--mksection` - output `path` and `end` keywords before and after outputting paths


- pathattach - converts IPL (detached) paths back to IDE paths. Input paths **must** contain additional metadata initially output by `pathdetach` in order to be able to properly re-attach paths

  USAGE:  
  `python pathattach.py [--verbose] [--mksection] pathfile.ipl iplfiles.ipl...`  
  `--verbose` - print warnings if paths for a model are processed more than once  
  `--mksection` - output `path` and `end` keywords before and after outputting paths


- calcflag - helper for calculating additional path flags for `pathdetach`