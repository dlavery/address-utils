import re
import jellyfish

PAFattrs = [
    'postcode',
    'postTown',
    'dependentLocality',
    'doubleDependentLocality',
    'thoroughfare',
    'dependentThoroughfare',
    'buildingNumber',
    'buildingName',
    'subBuildingName',
    'POBox',
    'departmentName',
    'organisationName',
    'UDPRN',
    'postcodeType',
    'SUOrganisationIndicator',
    'deliveryPointSuffix'
    ]

def jaccard_index(s1, s2):
    # Calculate the similarity between two single line addresses using the Jaccard coefficient

    # make 3-gram sets
    a = {s1[i] + s1[i+1] + s1[i+2] for i in range(len(s1)-2)}
    b = {s2[i] + s2[i+1] + s2[i+2] for i in range(len(s2)-2)}

    # calculate coefficient
    union = a.union(b)
    intersect = a.intersection(b)

    if len(union) > 0:
        return (len(intersect) / len(union))
    else:
        return 0

def separate_postcode(str):
    # separate postcode from a single line address
    pattn = '([Gg][Ii][Rr] 0[Aa]{2})|((([A-Za-z][0-9]{1,2})|(([A-Za-z][A-Ha-hJ-Yj-y][0-9]{1,2})|(([A-Za-z][0-9][A-Za-z])|([A-Za-z][A-Ha-hJ-Yj-y][0-9]?[A-Za-z])))) [0-9][A-Za-z]{2})'
    matches = re.search(pattn, str)
    if matches:
        postcode = matches.group(0)
        address = re.sub(postcode, '', str)
    else:
        postcode = ''
        address = str
    return (address.strip(), postcode)

def normalise(str):
    # normalise a string - remove all but alphanumerics and a single separating
    # space and convert the result to upper case
    return ' '.join(re.split('\s+', re.sub('[^A-Za-z0-9 ]', '', str).upper())).strip()

def strip_spaces(str):
    # remove all spaces from a string
    return re.sub('\s', '', str)

def remove_stopwords(str):
    # remove stopwords such as 'the', 'and' etc from a string
    stopwords = ['A','ABLE','ABOUT','ACROSS','AFTER','ALL','ALMOST','ALSO','AM','AMONG','AN','AND','ANY','ARE','AS','AT','BE','BECAUSE','BEEN','BUT','BY','CAN','CANNOT','COULD','DEAR','DID','DO','DOES','EITHER','ELSE','EVER','EVERY','FOR','FROM','GET','GOT','HAD','HAS','HAVE','HE','HER','HERS','HIM','HIS','HOW','HOWEVER','I','IF','IN','INTO','IS','IT','ITS','JUST','LEAST','LET','LIKE','LIKELY','MAY','ME','MIGHT','MOST','MUST','MY','NEITHER','NO','NOR','NOT','OF','OFF','OFTEN','ON','ONLY','OR','OTHER','OUR','OWN','RATHER','SAID','SAY','SAYS','SHE','SHOULD','SINCE','SO','SOME','THAN','THAT','THE','THEIR','THEM','THEN','THERE','THESE','THEY','THIS','TIS','TO','TOO','TWAS','US','WANTS','WAS','WE','WERE','WHAT','WHEN','WHERE','WHICH','WHILE','WHO','WHOM','WHY','WILL','WITH','WOULD','YET','YOU','YOUR']
    return ' '.join([x for x in re.split('\s+', str) if x not in stopwords])

def expand_abbreviations(str):
    # expand common thoroughfare type abbreviations, e.g. 'RD' becomes 'ROAD'
    abbreviations = {
        'ALY':'ALLEY',
        'ARC':'ARCADE',
        'AV':'AVENUE',
        'AVE':'AVENUE',
        'AVEN':'AVENUE',
        'AVENU':'AVENUE',
        'AVN':'AVENUE',
        'AVNUE':'AVENUE',
        'BNK':'BANK',
        'BCH':'BEACH',
        'BOT':'BOTTOM',
        'BOTTM':'BOTTOM',
        'BTM':'BOTTOM',
        'BLVD':'BOULEVARD',
        'BOUL':'BOULEVARD',
        'BOULV':'BOULEVARD',
        'BRDGE':'BRIDGE',
        'BRG':'BRIDGE',
        'BLDG': 'BUILDING',
        'CAUSEWA':'CAUSEWAY',
        'CSWY':'CAUSEWAY',
        'CIRC':'CIRCUS',
        'CL':'CLOSE',
        'COR':'CORNER',
        'CT':'COURT',
        'CV':'COVE',
        'CRES':'CRESCENT',
        'CRSENT':'CRESCENT',
        'CRSNT':'CRESCENT',
        'XING':'CROSSING',
        'DL':'DALE',
        'DR':'DRIVE',
        'DRIV':'DRIVE',
        'DRV':'DRIVE',
        'EST':'ESTATE',
        'GDNS':'GARDENS',
        'GRDNS':'GARDENS',
        'GROV':'GROVE',
        'GRV':'GROVE',
        'HVN':'HAVEN',
        'HL':'HILL',
        'JCT':'JUNCTION',
        'JCTN':'JUNCTION',
        'LN':'LANE',
        'LCK':'LOCK',
        'LDG':'LODGE',
        'LDGE':'LODGE',
        'LODG':'LODGE',
        'MNR':'MANOR',
        'MD':'MEAD',
        'MWS':'MEWS',
        'MNT':'MOUNT',
        'PKWY':'PARKWAY',
        'PL':'PLACE',
        'RDG':'RIDGE',
        'RI':'RISE',
        'RD':'ROAD',
        'RW':'ROW',
        'SQ':'SQUARE',
        'SQR':'SQUARE',
        'SQRE':'SQUARE',
        'SQU':'SQUARE',
        'STA':'STATION',
        'STN':'STATION',
        'ST':'STREET',
        'STR':'STREET',
        'STRT':'STREET',
        'TCE':'TERRACE',
        'VL':'VALE',
        'VW':'VIEW',
        'VILL':'VILLAGE',
        'VILLG':'VILLAGE',
        'VLG':'VILLAGE',
        'WY':'WAY',
        'WH':'WHARF',
        'WHA':'WHARF',
        'WHF':'WHARF'
    }
    words = re.split('\s+', str)
    newwords = []
    for w in words:
        if w in abbreviations:
            newwords.append(abbreviations[w])
        else:
            newwords.append(w)
    return ' '.join(newwords)

def single_line(addr):
    # create a single line address from a list of address lines
    return ' '.join(addr)

def paf_to_lines(address):
    # convert PAF format address to a list of address lines
    lines = []
    if 'organisationName' in address:
        lines.append(address['organisationName'])
        lines.append('\n')
    if 'subBuildingName' in address:
        lines.append(address['subBuildingName'])
        lines.append(' ')
    if 'buildingName' in address:
        lines.append(address['buildingName'])
        lines.append('\n')
    if 'buildingNumber' in address:
        lines.append(address['buildingNumber'])
        lines.append(' ')
    if 'dependentThoroughfare' in address:
        lines.append(address['dependentThoroughfare'])
        lines.append('\n')
    if 'thoroughfare' in address:
        lines.append(address['thoroughfare'])
        lines.append('\n')
    if 'doubleDependentLocality' in address:
        lines.append(address['doubleDependentLocality'])
        lines.append('\n')
    if 'dependentLocality' in address:
        lines.append(address['dependentLocality'])
        lines.append('\n')
    if 'postTown' in address:
        lines.append(address['postTown'])
        lines.append('\n')
    if 'postcode' in address:
        lines.append(address['postcode'])
        lines.append('\n')
    line = ''.join(lines)
    lines = line.split('\n')
    return lines[0:-1]

def phonetic(addressline):
    # create a metaphone representation of an address or partial address
    words = re.split('\s+', addressline)
    phonetics = []
    for word in words:
        if re.match('\d', word):
            phonetics.append(word)
        else:
            phonetics.append(jellyfish.metaphone(word))
    return ''.join(phonetics)

def match_address():
    pass
