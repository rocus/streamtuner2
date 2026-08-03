# encoding: utf-8
# api: streamtuner2
# title: Links to directory services
# description: Static list of various music directory websites.
# type: group
# category: web
# version: 0.4
# priority: standard
# config: -
#
# Simply adds a "links" entry in bookmarks tab, where known services
# are listed with homepage links. Registered plugins automatically
# end up on top of that list.
#


from config import *
from channels import *
import ahttp
import copy, json, re



# hooks into main.bookmarks
class links (FeaturePlugin):

    # list
    streams = [    ]
    default = [
        ("stream", "RadioTower", "http://www.radiotower.com/"),
        ("stream", "8tracks", "http://8tracks.com/"),
        ("stream", "Jango", "http://www.jango.com/"),
        ("stream", "last.fm", "http://www.last.fm/"),
        ("stream", "StreamFinder", "http://www.streamfinder.com/"),
        ("stream", "Rhapsody (US-only)", "http://www.rhapsody.com/"),
        ("stream", "Pirateradio Network", "http://www.pirateradionetwork.com/"),
        ("stream", "radio-locator", "http://www.radio-locator.com/"),
        ("stream", "Radio Station World", "http://radiostationworld.com/"),
        ("stream", "iHeart", "http://www.iheartradio.com/"),
        ("download", "Live Music Archive(.org)", "https://archive.org/details/etree"),
        ("download", "FMA, free music archive", "http://freemusicarchive.org/"),
        ("download", "Audiofarm", "http://audiofarm.org/"),
        ("stream", "SoundCloud", "https://soundcloud.com/"),
        ("download", "ccMixter", "http://dig.ccmixter.org/"),
        ("stream", "Hype Machine", "http://hypem.com/"),
        ("download", "Amazon Free MP3s", "http://www.amazon.com/b/ref=dm_hp_bb_atw?node=7933257011"),
        ("download", "ccTrax", "http://www.cctrax.com/"),
        ("list", "WP: Streaming music services", "http://en.wikipedia.org/wiki/Comparison_of_on-demand_streaming_music_services"),
        ("list", "WP: Music databases", "http://en.wikipedia.org/wiki/List_of_online_music_databases"),
        ("commercial", "Google Play Music", "https://play.google.com/about/music/"),
        ("commercial", "Deezer", "http://www.deezer.com/features/music.html"),
    ]
    

    
    # prepare gui
    def init2(self, parent):
        if not parent:
            return
        self.bookmarks = parent.bookmarks

        # prepare target category
        if not self.bookmarks.streams.get(self.module):
            self.bookmarks.streams[self.module] = self.streams
        self.bookmarks.add_category(self.module, self)


    def update_streams(self, cat="links"):
        #log.PROC("links.update_streams")
        del self.streams[:]
    
        # Collect links from channel plugins
        for name,channel in self.parent.channels.items():
            try:
                self.streams.append({
                    "favourite": 1,
                    "genre": "channel",
                    "title": channel.meta.get("title", channel.module),
                    "homepage": channel.meta.get("url", ""),
                    "format": "text/html",
                })
            except Exception as e:
                log.ERR("links: adding entry failed:", e)
        
        # Add wiki or built-in link list
        try:
            self.from_wiki()
        except Exception as e:
            log.ERR("Failure to retrieve /wiki/links\n", e)
        for genre, title, homepage in self.default:
            self.streams.append(dict(genre=genre, title=title, homepage=homepage, type="text/html"))

        # add to bookmarks
        return self.streams


    # retrieve links from repository wiki page (via JSON API /json/wiki/get/…)
    def from_wiki(self):
        src = ahttp.get("https://fossil.include-once.org/streamtuner2/json/wiki/get/links", timeout=2.0)
        if not src:
            return
        wiki = json.loads(src)
        if not wiki or not wiki.get("payload"):
            return
        wiki = wiki["payload"]["content"]
        pairs = re.findall("(?:(\w+)\s*\|\s*)?\[([\w\s(&,;!:#+\-)]+)\]\((http[^)\s]+)\)", wiki)
        if not pairs:
            return
        self.default = [(cat if cat else "site", title, url) for cat,title,url in pairs]

