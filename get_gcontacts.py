#!/usr/env python
#
# retrieve google contacts of user, usr (with password, pwd)
# and belonging to the group, grp
#
# Author: Enrico Spinielli

import gdata.contacts.client
from optparse import OptionParser

def main():
    usage = "usage: %prog user pwd groupname"
    description = "Print USER's Google Contacts in GROUPNAME. (Use PWD as password.)"
    epilog="Use at your own risk!"
    parser = OptionParser(usage=usage,
                          description=description,
                          epilog=epilog)
    (options, args) = parser.parse_args()
    if len(args) != 3:
        parser.error("incorrect number of arguments")
    usr = args[0]
    pwd = args[1]
    grp = args[2]
    retrieveGContacts(usr, pwd, grp)

def retriveGContactsGroupID(client, group):
    feed = client.GetGroups()
    for entry in feed.entry:
        if entry.title.text.encode('utf-8') == group:
            g = entry.id.text
            break
    return g

def retrieveGContacts(user, password, group):
    """print out all USER's Google Contacts in GROUP."""
    gd_client = gdata.contacts.client.ContactsClient()
    gd_client.client_login(user, password, "myscript")


    query = gdata.contacts.client.ContactsQuery()
    query.max_results = 200
    #   query.alt = 'json'
    query.group = retriveGContactsGroupID(gd_client, group)
    feed = gd_client.get_contacts(q = query)
    contacts = []
    for contact in feed.entry:
        #contact.name.full_name
        #print contact
        contacts.append(contact)
    return contacts

if __name__ == "__main__":
    main()
