#/usr/bin/env python
#
# 1. export the relevant google contacts' group from GMail using format 'Google CSV'
# 2. upload exported contacts in Google Drive
# 3. export the file on Drive to Google Docs
# 3. download it as CSV file
# coding: utf-8
import csv
import re
import io
import json


from optparse import OptionParser

def main():
    usage = "usage: %prog csvcontacts outputfile"
    description = "Dump USER's Google Contacts in file CSVCONTACTS as JSON in file OUTPUT."
    epilog="Use at your own risk!"
    parser = OptionParser(usage=usage,
                          description=description,
                          epilog=epilog)
    (options, args) = parser.parse_args()
    if len(args) != 2:
        parser.error("incorrect number of arguments")
    csvfile  = args[0]
    jsonfile = args[1]
    print args
    dumpAsJson(csvfile, jsonfile)



def getHomePhone(p):
    """Return Home phone."""
    return getPhone(p, 'Home')

def getWorkPhone(p):
    """Return Work phone."""
    return getPhone(p, 'Work')

def getMobilePhone(p):
    """Return Mobile phone."""
    return getPhone(p, 'Mobile')

def getPhone(p, t='Home'):
    """Return Phone number of type 't'."""
    a = ""
    r = re.compile(r"^Phone (\d+) - Type$")
    for k, v in p.iteritems():
        m = r.match(k)
        if m and (v == t):
            a = p[m.group(0).replace("Type", "Value")]
    return a

def getHomeAddress(p):
    """Return Address of type 't'."""
    return getAddress(p, 'Home')

def getAddress(p, t='Home'):
    """Return Address of type 't'."""
    a = {}
    r = re.compile(r"^Address (\d+) - Type$")
    for k, v in p.iteritems():
        m = r.match(k)
        if m and (v == t):
            a = {
                'street':  p[m.group(0).replace("Type", "Street")],
                'zip':     p[m.group(0).replace("Type", "Postal Code")],
                'city':    p[m.group(0).replace("Type", "City")],
                'country': p[m.group(0).replace("Type", "Country")]
                 }
    return a

def getFatherDetails(jcontacts, p):
    """Return Father details."""
    m = getParentDetails(jcontacts, p, t='Father')
    m['Relationship'] = 'Father'
    return m

def getMotherDetails(jcontacts, p):
    """Return Mother details."""
    m = getParentDetails(jcontacts, p, t='Mother')
    m['Relationship'] = 'Mother'
    return m

def getParentDetails(jcontacts, p, t):
    """Return details of p's Parent of type 't', i.e. 'Mother'."""
    a = {}
    r = re.compile(r"^Relation (\d+) - Type$")
    for k, v in p.iteritems():
        m = r.match(k)
        if m and (v == t):
            # look for parent
            f_or_m = findContact(p[m.group(0).replace("Type", "Value")], jcontacts);
            a = {
                'familyname':  f_or_m['Family Name'],
                'givenname':   f_or_m['Given Name'],
                'name':        f_or_m['Name'],
                'workphone':   getWorkPhone(f_or_m),
                'mobilephone': getMobilePhone(f_or_m),
                }
    return a

def findContact(name, contacts):
    """Find parent parente in contacts list."""
    p = [c for c in contacts if c['Name'] == name][0]
    return p




def dumpAsJson(infile, outfile):
    input_data_file  = infile
    output_data_file = outfile

    contacts = csv.reader(open(input_data_file, 'r'), delimiter=',', quotechar='"')
    rows =[]
    for c in contacts:
        rows.append(c)
    keys = rows[0]

    # JSON-like contacts
    jcontacts = [dict(zip(keys, c)) for c in rows[1:]]

    # find entries with a 'Child' relationship
    r = re.compile(r"^Relation (\d+) - Type$")
    names = []
    for c in jcontacts:
        c['Name'] = c['\xef\xbb\xbfName']
        del c['\xef\xbb\xbfName']
        names.append(c['Name'])

    kids = []
    family = []
    for c in jcontacts:
        for k, v in c.iteritems():
            m = r.match(k)
            if m and (c[m.group(0)] == 'Child'):
                if c['Name'] in names:
                    # take the value for matching type
                    # it can be something like:
                    #    'Giovanni Spinielli ::: Francesco Spinielli'
                    s = c[m.group(0).replace("Type", "Value")]
                    # scan the list of children and add only the ones in names
                    children = [w.strip() for w in s.split(':::') if w]
                    for k in children:
                        if k in names:
                            kids.append(k)
    # unique
    kids = set(kids)

    # sort by Surname (assumed to be the last string)
    kids = list(kids)
    kids.sort(key=lambda x: x.split()[-1])

    families = []
    # build the family
    for kid in kids:
        k = [c for c in jcontacts if c['Name'] == kid][0]
        families.append({
            'familyname':  k['Family Name'],
            'givenname':   k['Given Name'],
            'name':        k['Name'],
            'birthday':    k['Birthday'],
            'homeaddress': getHomeAddress(k),
            'homephone':   getHomePhone(k),
            'parents':     [getMotherDetails(jcontacts, k),
                            getFatherDetails(jcontacts, k)]})

    # 'b' needed for unicode
    with io.open(output_data_file, 'wb') as outfile:
        json.dump(families, outfile)


if __name__ == "__main__":
    main()
