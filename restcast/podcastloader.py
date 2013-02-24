import feedparser
from time import mktime
from datetime import datetime
from restcast.models import Episode, Podcast

def load_episodes_for_podcast(podcast):
    feed = feedparser.parse(podcast.link)
    new_episodes = []
    for entry in feed.entries:
        link = entry.links[0]['href']
        matching_episode = list(podcast.episode_set.filter(link=link))
        if not matching_episode:
            episode = Episode(
                podcast=podcast,
                subtitle=entry.subtitle,
                title=entry.title,
                author=entry.author,
                updated=datetime.fromtimestamp(mktime(entry.updated_parsed)),
                summary=entry.summary,
                link=link
                )
            episode.save()
            new_episodes.append(episode)
    return new_episodes
            


def create_podcast_form_feed_link(link):
    itunes_podcast_xml = feedparser.parse(link)
    podcast_feed = itunes_podcast_xml.feed

    podcast = Podcast(
        last_updated = datetime.fromtimestamp(mktime(itunes_podcast_xml.updated_parsed)),
        version = itunes_podcast_xml.version,
        itunes_namespace = itunes_podcast_xml.namespaces['itunes'],
        publisher = podcast_feed.publisher,
        subtitle = podcast_feed.subtitle,
        link = link,
        title = podcast_feed.title,
        rights = podcast_feed.rights,
        author = podcast_feed.author, 
        email = podcast_feed.authors[0]['email'],
        summary = podcast_feed.summary
        )

    podcast.save()
    return podcast
    
