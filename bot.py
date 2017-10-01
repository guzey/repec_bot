import tweepy
from variable_stuff import *
import requests, bs4
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw

#
# abstract --> image; adapted from https://gist.github.com/destan/5540702
#

def text2png(text, fullpath, leftpadding = 6, upperpadding=6, rightpadding = 3, width = 500):

    font = ImageFont.truetype("font.ttf", 20)
    text = text.replace('\r\n', '')#.replace('\n', ' ' + '\uFFFD' + ' ')

    lines = []
    line = ""

    for word in text.split():
        if font.getsize( line + ' ' + word )[0] <= (width - rightpadding - leftpadding):
            line += ' ' + word
        else: #start a new line
            lines.append( line[1:] ) #slice the white space in the begining of the line
            line = ' ' + word

    if len(line) != 0:
        lines.append( line[1:] ) #add the last line

    line_height = font.getsize(text)[1]
    img_height = line_height * len(lines) + 12

    img = Image.new("RGB", (width, img_height), "#FFF")
    draw = ImageDraw.Draw(img)

    for line in lines:
        draw.text( (leftpadding, upperpadding), line, "#000", font=font)
        upperpadding += line_height

    img.save(fullpath)


def main():

    # twitter auth info
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    # repec page with last papers; jel=d82 is mechanism design code
    web_page = requests.get('https://econpapers.repec.org/scripts/search.pf?sort=date;jel=' + jel_codes + '&iframes=no')
    web_page_text = bs4.BeautifulSoup(web_page.text, "html.parser")

    # get tweets to be able to check if paper was tweeted already
    tweets = api.user_timeline(id=user_id, count=1)

    # get parts of web_page with each paper (they're in a list)
    parsed_lists = web_page_text.find_all('li')

    # check each paper if it was tweeted already till reach the last one that was tweeted
    papers_titles = [None] * 20
    papers_links = [None] * 20

    for paper in range(0, 20):
        # extract title from webpage (they're in bold)
        papers_titles[paper] = parsed_lists[paper].find_next('a').getText()
        # cut long titles to fit in a tweet
        if len(papers_titles[paper]) > 116:
            papers_titles[paper] = papers_titles[paper][0:115] + "…"
        papers_links[paper] = "https://econpapers.repec.org" + parsed_lists[paper].find_next('a')['href']

        if tweets:
            # if length of paper's title is less than length of tweet,
            # then could be the right tweet, since link adds to length
            # can't compare directly because then could get out of range for tweet
            # + only check last tweet
            # -2 appears because twitter adds "…" symbol sometimes and we need to cut it off to make comparison ok
            if len(papers_titles[paper]) < len(tweets[0].text):
                if papers_titles[paper][0:-2] == tweets[0].text[0:int(len(papers_titles[paper])) - 2]:
                    # get the number of last paper tweeted
                    last_tweeted_paper = paper
                    break
        else:
            last_tweeted_paper = 19

    for paper in reversed(range(0,last_tweeted_paper)):

        paper_page = requests.get(papers_links[paper])
        paper_page.encoding = paper_page.apparent_encoding
        paper_page_text = bs4.BeautifulSoup(paper_page.text, "html.parser")
        if paper_page_text.find(text="Abstract:"):
            abstract = paper_page_text.find(text="Abstract:").next_element
            text2png(abstract, 'abstract.png')
            api.update_with_media("abstract.png", papers_titles[paper] + " " + papers_links[paper])
        else:
            api.update_status(papers_titles[paper] + " " + papers_links[paper])

if __name__ == "__main__":
    main()
