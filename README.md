This is a very simple demo of how to interact with the Etsy.com API using Flask and Flask OAuth extension.
To get started, just add a settings.py file containing the API key and secret (see app.py for details) and run the app.

Note that it needs to be publicly accessible for the authorization callbacks to work.

In practice, you'll want to do something smarter with the tokens than keeping them in a session cookie, but this gets you going.

Review the excellent Flask, Flask OAuth and Etsy.com API documentation for more details.
