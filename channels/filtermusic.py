# encoding: UTF-8
# api: streamtuner2
# title: filtermusic
# description: Daily refreshed list of electronic+dance music streams.
# version: 0.3
# type: channel
# url: http://filtermusic.net/
# category: radio
# config: -
# png:
#   iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAIAAACQkWg2AAAACXBIWXMAAA7EAAAOxAGVKw4bAAAAB3RJTUUH3wQeBA4mIX2CmQAAABl0RVh0Q29tbWVudABDcmVhdGVkIHdpdGggR0lNUFeBDhcAAAGISURBVCjPnVI9SyNRFD333slMMhrNjBJU0FSLIlovy6IWbmelhRJ/gI2lkMXfIOwv2K38qizstFCs3B+wLFhoIfiR1cggkXzMvHnPIiG6
#   GkE8zYXLPfe8c94F2oAkk7CHHLIIb4AAEIlkcuJmARr8OTxW+pKe9l6PSqN0jOe9hd3014J09tdP96SHSLh8GKirsM1+TvnZ5RN/buO5ItvcUH4BCwC7vex0Vf5stroGMKFu+3omKymdfUTMrs9uDyczAHzfz+VyIpwgu1u8NGccSjbFUyOz/vyOUVVoDZbq3+1gd6lQWMnn85PTEzPR4mdnKjLhrS6uBasArNrZ3t36N29u6/7ge/1038QRECul
#   arWaNrqLvV/lHx2U/pQYbXowUTUuXwJGV0rxQ/H/sKkU/yuqC4dSfdZA0wMAELd+4wUhNFUABro52Spvg54l9y7Cq1g/RiBwAvTkQURs2waBwQARiGE93RKJzW5v/fxIl68bXdd1gyA4Pv6tlLqLbyJEoamX4iI+gEdAknsz9gP1pgAAAABJRU5ErkJggg==
# x-doc:
#   http://code.google.com/p/filtermusic-dot-net/source/browse/
# priority: extra
# extraction-method: regex
#
#
# Filtermusic.net is a radio collection with primarily electronic
# and dance music stations.
#
#  · All entries come with direct server stream URLs.
#  · No homepage listings, and genre details spotty (so omitted).


from config import *
from channels import *
import ahttp
import re


# filtermusic.net
class filtermusic (ChannelPlugin):

    # control attributes
    has_search = False
    listformat = "srv"
    audioformat = "audio/mpeg"
    titles = dict(listeners=False, bitrate=False, playing="Description")
    categories = ["Top Radio Stations", "House / Dance", "Lounge Grooves", "Rock / Metal", "Breaks / Drum'n'Bass", "Various / Independent", "Downtempo / Ambient", "60's / 70's / 80's / 90's", "Hits / Mainstream", "Electronica / Industrial", "Techno / Trance", "HipHop / RnB", "Classical", "Eclectic", "Funk / Soul / Disco", "Reggae / Dub / Dancehall", "International / Ethnic", "Jazz", "Latin / Salsa / Tango"]
    img_resize = 32

    # static
    def update_categories(self):
        pass


    # Refresh station list
    def update_streams(self, cat, search=None):
        return self.from_web(cat)

    # Extract directly from filtermusic.net html
    def from_web(self, cat):
        ucat = re.sub("\W+", "-", cat.lower().replace("'", ""))
        html = ahttp.get("http://filtermusic.net/{}".format(ucat))
        
        rx_station = re.compile("""
               <article [^>]+ about="/([\w\-]+)" .*?
               <img [^>]+ src="(http.+?)" .*?
               data-listen="(.*?)" .*?
               <h3[^>]*>(.+?)</h3> .*?
               <p>(.*?)</p>
            """, re.X|re.S
        )
        ls = re.findall(rx_station, html)
        log.DATA(ls)
        r = [
            dict(
                genre=cat,
                title=unhtml(strip_tags(title)),
                playing=unhtml(strip_tags(descr)),
                img=img,
                homepage="https://filtermusic.net/{}".format(id), id=id, url=url
            )
            for id, img, url, title, descr in ls
        ]
        return r

