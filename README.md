This is just a simple project to generate an address book for my sons' classes.

HTTP Server setup
=================

    $ python -m SimpleHTTPServer 8080

That's it! Now your http server will start in port 8080.
Now open a browser and type the following address:

    http://127.0.0.1:8080/addressbook.html

Preparing the data
==================
1. export the relevant google contacts' group from GMail using format 'Google CSV'
2. upload exported contacts in Google Drive
3. export the file on Drive to Google Docs
3. download it as CSV file
4. run the following command
    $ python gcontacts_csv2json.py mycontacts.csv cucu.json

Generate the HTML
=================
Note that you have to change addressbook.html to use the json
file generated from the previous section.
