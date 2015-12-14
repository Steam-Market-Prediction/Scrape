# Scrape

Scrape.py is supposed to be used to scrape item history data using items.txt. All of the data is stored in the Market List folder.

item_schema_parse.py is supposed to be used to read the vdf file list provided by valve. The vdf file provided by valve includes information that is not useful in this parse, so item_schema_parse.py will get rid of all the extra information except the item name. This allows the generation of items.txt for Scrape.py to use.
