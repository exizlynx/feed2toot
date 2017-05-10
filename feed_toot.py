import os
from mastodon import Mastodon
import feedparser

# Settings
instance_url = 'https://mastodon.social'
login_id = '[YourUserName]'
login_password = '[YourPassword]'

history_file = 'toot_log.txt'
clientcred_file = 'pytooter_clientcred.txt'
feed_urls = []
feed_urls.append('[RSS feed url]')

if not os.path.exists(clientcred_file):
    Mastodon.create_app(
        'Feed2Mastodon',
        to_file = clientcred_file,
        api_base_url = instance_url
    )

mastodon = Mastodon(
    client_id = clientcred_file,
    api_base_url = instance_url
)
mastodon.log_in(
    login_id,
    login_password
)

for feed_url in feed_urls:
    feed = feedparser.parse(feed_url)

    for item in reversed(feed.entries):
        link = item.link
        content = item.title + ' ' + item.link
        is_send = True

        if os.path.exists(history_file):
            data = open(history_file, "r+")
            entries = data.readlines()
        else:
            data = open(history_file, "a+")
            entries = []

        for entry in entries:
            if link in entry:
                is_send = False

        if is_send:
            mastodon.toot(content)
            data.write(link + '\n')
            data.flush()

    data.close()
