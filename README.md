Profiles
========

[Volatility](https://github.com/volatilityfoundation/volatility) profiles for Linux and Mac OS X

Each of these profiles is implemented as a zip file. You can enable them individually with your Volatility installation by copying Linux profiles to `volatility/plugins/overlays/linux` and Mac profiles to `volatility/plugins/overlays/mac`. 

## Important notes

- Only enable the profiles you plan to use. If you copy all zip files into the aforementioned directories, Volatility will be extremely slow to load. 
- [Volatility 3](https://github.com/volatilityfoundation/volatility3/) does not use profiles, but instead uses [`Symbol Tables`](https://volatility3.readthedocs.io/en/latest/basics.html#symbol-tables). 
- These profiles may not be fully tested (or tested at all). Use at your own risk. If you encounter problems, please report them through the issue tracker: https://github.com/volatilityfoundation/profiles/issues. 
