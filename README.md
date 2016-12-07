This is a template for a bot that tweets latest papers to appear on RePEc for a given JEL code(s).

# Setup

## twitter

1. Clone the repo by entering the following in your console

        git clone https://github.com/guzey/repec_bot

2. Go to http://twitter.com/ and create an account for your bot. Go to http://apps.twitter.com/ and create a new app. For the "Website" field just enter your personal site or htpp://somethingrandom.com if you don't have one.

3. Go to Keys and Access Tokens and copy Consumer Key and Consumer Secret to variable_stuff.py. Scroll down and press "Create my access token", then copy Access Token and Access Token Secret to variable_stuff.py (make sure there are no rogue spaces anywhere!).

4. On line 1, enter a JEL code you like ([here](https://www.aeaweb.org/econlit/jelCodes.php?view=jel)'s the list). If you want to enter several codes, separate them by "+". On line 2, enter your Owner ID from twitter's Keys and Access Tokens page and close variable_stuff.py.

5. In console enter

        git add .
        git commit -m "enter login data"

We're done with twitter for now. You can run bot.py on your machine to make sure the bot works. However, we want it to run automatically, so proceed to Heroku setup (note: you'll need to enter your credit card data into Heroku account for this).

Note that twitter's keys you entered in variable_stuff.py gives full control over the twitter account. So if you intend on publishing this code, make sure add variable_stuff to .gitignore
 
## Heroku

1. Create and activate a [Heroku](https://www.heroku.com/) account. Press "Create New App" button and follow the directions. Scroll down to "Deploy using Heroku Git" section and follow the directions there i.e. download and install Heroku CLI and enter the following commands in the console:


        heroku login
        heroku git:remote -a YOURAPPSNAME
        git push heroku master


2. Now we need to create a scheduler that would run the bot for us automatically (you'll need to enter a credit card for this to work):


        heroku addons:create scheduler:standard
        heroku addons:open scheduler


3. Press "Add new job", enter "worker" (without the quote marks) into the text field, set frequency to every 10 minutes, and click save.

That's it! Now your bot will automatically check for new papers every 10 minutes and post them to the linked twitter account!