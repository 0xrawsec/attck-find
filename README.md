Command Line Utility to Search Terms Into MITRE ATT&amp;CK Matrix

# Usage
```
./attck-find.py -h                    
usage: Search for terms in MITRE ATT&CK Matrix [-h] [-p PLATFORM]
                                               [-f {raw,text}] [-a]
                                               terms [terms ...]

positional arguments:
  terms                 Term (regex) to search for

optional arguments:
  -h, --help            show this help message and exit
  -p PLATFORM, --platform PLATFORM
                        Regexp matching platform to search for.
  -f {raw,text}, --format {raw,text}
                        Format output
  -a, --all             Search for techniques containing all the terms
```
