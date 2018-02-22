# address-utils
Utilities for matching unformatted addresses with PAF UDPRN.

These utilities require data available from the UK Royal Mail at https://www.poweredbypaf.com/using-our-address-data/use-the-data-yourself/; the addressloader will load this data into a local MongoDB as specified in the addressutils.cfg file.

Also useful is the PAF programmers' guide: https://www.poweredbypaf.com/wp-content/uploads/2017/07/Latest-Programmers_guide_Edition-7-Version-6.pdf.

And the addressing guide: https://www.royalmail.com/sites/default/files/GuideForClearAddressing_October_2012_0.pdf.

Stopwords are based upon this list: https://www.textfixer.com/tutorials/common-english-words.txt.

Street abbreviations are based on this list: https://pe.usps.com/text/pub28/28apc_002.htm.

Documentation on the setup of MongoDB can be found here.
