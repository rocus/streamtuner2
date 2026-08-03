# encoding: UTF-8
# api: streamtuner2
# title: SomaFM
# description: Alternative radio, entirely community sponsored and non-advertisey.
# version: 1.0
# type: channel
# category: radio
# url: http://somafm.com/
# config:
#   { name: somafm_bitrate, value: 64, type: select, select: "130=AAC → 128 kbit/s|64=AAC → 64 kbit/s|32=AAC → 32 kbit/s|0=MP3 → 128 kbit/s|56=MP3 → 56 kbit/s|24=MP3 → 24 kbit/s", description: "Most streams are accessible in different bitrates." }
# priority: extra
# extraction-method: static
# png:
#    iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAIAAACQkWg2AAAAA3NCSVQICAjb4U/gAAACpUlEQVQokQXBS28bVRQA4HvOfcwd2xNP7caFtgiqkoglKyhCiFZiUSGxQcACdkis2SGx5lcgumFXhNoNGwpISGUZMKJSGtooStM4teOJXeOZufO4j8P3wZeff7r3z32tRaL7g/7Ikq/qXKEI4BZ5HnzYiJQn
#    50IAxuIkFe9/+NXDP+9JVr++tX3jk2/I29lkV0fd0DY741+z7PC9dz7Ki9XZ8kSrDudKSIBExx3ulVJJL5UcvVkoob0zm8Nzoc0uXnq1Mcuko9NewnkkgvNaMQVCQWirugz4w88/nUyPPrh+M9a9SGAIbVXWPlSmEkIxUeanArnkrLbNepX9vffw2x+/Z2Rni7PP3n0rjuLkxf7R8b+tMVYwaKzIJvuc
#    WkRE1j7dvX/77u0QcKOz8eDxnjk+2L6QDtLfpARXGssKEcVYtQwYcsCuiP74a7zzaB8Yy03DibXWjg+nv/9yz9fsP+NO182ybIRrV5aIA5ONOTw65oJrJQhCX8sYsSH+ZDopns8coyZU3Em8NNrUinMZT56vD+azWAkF1AUAS8vWrwKtnTuYZ97Zui7XdYkXh30GUqDczcPl0ebLg0HlnQZERkikOGFX
#    GuCmbvOynq8KzMoakaNKFMY3r11LtbKOeQYKMCZ4+3xyNWbzower9Vyx0JOI+4/GRWvLgq4Mo1Haq6pcCXBAAtl5bj9+I7313ddfvHkuNpkpKxaskI1Z1rp4NqWtV2ZPT04sAeeFBy4Di8W4rLaeHe+sxJ395aqcXhiN4LXtq6fZGSAQV0gEzMed/mJxmiYi1mIyMz1WV6itZ8G1/TTlqHRZFGVpgrcI
#    GIL3ntq2aRpXGAdEXkgOgMgiKTqdSLz0wqDo8UAEwIjIGF/VNun2iBEAU0pcHkYdBdaT9bA5TP8H6318x/9OSuUAAAAASUVORK5CYII=
#
# SomaFM is a non-commercial radio station project.
#
# Uses a static internal station list. Stream URLs are
# only rewritten depending on bitrate configuration.
#
# Note that only 64bit AAC and 128bit MP3 are guaranteed
# to be available. Most stations offer different bitrates,
# but not all of them!


from config import *
from channels import *
import re
import ahttp

# SomaFM radio stations
class somafm (ChannelPlugin):

    # description
    has_search = False
    listformat = "pls"
    audioformat = "audio/aac"
    titles = dict(listeners=False, playing="Description")

    categories = ["listen", "support"]
    builtin = [
        {'genre': 'ambient/electronica', 'listeners': 3210, 'title': 'Groove Salad', 'url': 'http://somafm.com/groovesalad130.pls', 'bitrate': 128, 'homepage': 'http://somafm.com/groovesalad/', 'playing': 'A nicely chilled plate of ambient/downtempo beats and grooves.'},
        {'genre': 'ambient', 'listeners': 962, 'title': 'Drone Zone', 'url': 'http://somafm.com/dronezone130.pls', 'bitrate': 128, 'homepage': 'http://somafm.com/dronezone/', 'playing': 'Served best chilled, safe with most medications. Atmospheric textures with minimal beats.'},
        {'genre': 'electronica', 'listeners': 571, 'title': 'Space Station Soma', 'url': 'http://somafm.com/spacestation130.pls', 'bitrate': 128, 'homepage': 'http://somafm.com/spacestation/', 'playing': 'Tune in, turn on, space out. Spaced-out ambient and mid-tempo electronica.'},
        {'genre': 'alternative/rock', 'listeners': 548, 'title': 'Indie Pop Rocks!', 'url': 'http://somafm.com/indiepop130.pls', 'bitrate': 128, 'homepage': 'http://somafm.com/indiepop/', 'playing': 'New and classic favorite indie pop tracks.'},
        {'genre': 'ambient', 'listeners': 459, 'title': 'Deep Space One', 'url': 'http://somafm.com/deepspaceone130.pls', 'bitrate': 128, 'homepage': 'http://somafm.com/deepspaceone/', 'playing': 'Deep ambient electronic, experimental and space music. For inner and outer space exploration.'},
        {'genre': 'lounge', 'listeners': 445, 'title': 'Secret Agent', 'url': 'http://somafm.com/secretagent130.pls', 'bitrate': 128, 'homepage': 'http://somafm.com/secretagent/', 'playing': 'The soundtrack for your stylish, mysterious, dangerous life. For Spies and PIs too!'},
        {'genre': 'ambient/electronica', 'listeners': 415, 'title': 'Groove Salad Classic', 'url': 'http://somafm.com/gsclassic130.pls', 'bitrate': 128, 'homepage': 'http://somafm.com/gsclassic/', 'playing': 'The classic (early 2000s) version of a nicely chilled plate of ambient/downtempo beats and grooves.'},
        {'genre': 'alternative/electronica', 'listeners': 387, 'title': 'Underground 80s', 'url': 'http://somafm.com/u80s130.pls', 'bitrate': 128, 'homepage': 'http://somafm.com/u80s/', 'playing': 'Early 80s UK Synthpop and a bit of New Wave.'},
        {'genre': 'electronica', 'listeners': 366, 'title': 'Lush', 'url': 'http://somafm.com/lush130.pls', 'bitrate': 128, 'homepage': 'http://somafm.com/lush/', 'playing': 'Sensuous and mellow vocals, mostly female, with an electronic influence.'},
        {'genre': '70s/rock', 'listeners': 355, 'title': 'Left Coast 70s', 'url': 'http://somafm.com/seventies130.pls', 'bitrate': 128, 'homepage': 'http://somafm.com/seventies/', 'playing': 'Mellow album rock from the Seventies. Yacht not required.'},
        {'genre': 'electronica/specials', 'listeners': 246, 'title': 'DEF CON Radio', 'url': 'http://somafm.com/defcon130.pls', 'bitrate': 128, 'homepage': 'http://somafm.com/defcon/', 'playing': 'Music for Hacking. The DEF CON Year-Round Channel.'},
        {'genre': 'alternative/rock', 'listeners': 225, 'title': 'BAGeL Radio', 'url': 'http://somafm.com/bagel130.pls', 'bitrate': 128, 'homepage': 'http://somafm.com/bagel/', 'playing': 'What alternative rock radio should sound like. [explicit]'},
        {'genre': 'folk/alternative', 'listeners': 217, 'title': 'Folk Forward', 'url': 'http://somafm.com/folkfwd130.pls', 'bitrate': 128, 'homepage': 'http://somafm.com/folkfwd/', 'playing': 'Indie Folk, Alt-folk and the occasional folk classics.'},
        {'genre': 'electronica', 'listeners': 190, 'title': 'Beat Blender', 'url': 'http://somafm.com/beatblender130.pls', 'bitrate': 128, 'homepage': 'http://somafm.com/beatblender/', 'playing': 'A late night blend of deep-house and downtempo chill.'},
        {'genre': 'world', 'listeners': 156, 'title': 'Suburbs of Goa', 'url': 'http://somafm.com/suburbsofgoa130.pls', 'bitrate': 128, 'homepage': 'http://somafm.com/suburbsofgoa/', 'playing': 'Desi-influenced Asian world beats and beyond.'},
        {'genre': 'americana', 'listeners': 155, 'title': 'Boot Liquor', 'url': 'http://somafm.com/bootliquor130.pls', 'bitrate': 128, 'homepage': 'http://somafm.com/bootliquor/', 'playing': 'Americana Roots music for Cowhands, Cowpokes and Cowtippers'},
        {'genre': 'celtic/world', 'listeners': 155, 'title': 'ThistleRadio', 'url': 'http://somafm.com/thistle130.pls', 'bitrate': 128, 'homepage': 'http://somafm.com/thistle/', 'playing': 'Exploring music from Celtic roots and branches'},
        {'genre': 'electronica', 'listeners': 145, 'title': 'The Trip', 'url': 'http://somafm.com/thetrip130.pls', 'bitrate': 128, 'homepage': 'http://somafm.com/thetrip/', 'playing': 'Progressive house / trance. Tip top tunes.'},
        {'genre': 'alternative', 'listeners': 142, 'title': 'PopTron', 'url': 'http://somafm.com/poptron130.pls', 'bitrate': 128, 'homepage': 'http://somafm.com/poptron/', 'playing': 'Electropop and indie dance rock with sparkle and pop.'},
        {'genre': 'jazz', 'listeners': 130, 'title': 'Sonic Universe', 'url': 'http://somafm.com/sonicuniverse130.pls', 'bitrate': 128, 'homepage': 'http://somafm.com/sonicuniverse/', 'playing': 'Transcending the world of jazz with eclectic, avant-garde takes on tradition.'},
        {'genre': 'electronica/hiphop', 'listeners': 124, 'title': 'Fluid', 'url': 'http://somafm.com/fluid130.pls', 'bitrate': 128, 'homepage': 'http://somafm.com/fluid/', 'playing': 'Drown in the electronic sound of instrumental hiphop, future soul and liquid trap.'},
        {'genre': 'lounge', 'listeners': 108, 'title': 'Illinois Street Lounge', 'url': 'http://somafm.com/illstreet130.pls', 'bitrate': 128, 'homepage': 'http://somafm.com/illstreet/', 'playing': 'Classic bachelor pad, playful exotica and vintage music of tomorrow.'},
        {'genre': 'reggae', 'listeners': 84, 'title': 'Heavyweight Reggae', 'url': 'http://somafm.com/reggae130.pls', 'bitrate': 128, 'homepage': 'http://somafm.com/reggae/', 'playing': 'NEW! Reggae, Ska, Rocksteady classic and deep tracks.'},
        {'genre': 'electronica', 'listeners': 66, 'title': 'cliqhop idm', 'url': 'http://somafm.com/cliqhop130.pls', 'bitrate': 128, 'homepage': 'http://somafm.com/cliqhop/', 'playing': u"Blips'n'beeps backed mostly w/beats. Intelligent Dance Music."},
        {'genre': 'electronica/alternative', 'listeners': 64, 'title': 'Digitalis', 'url': 'http://somafm.com/digitalis130.pls', 'bitrate': 128, 'homepage': 'http://somafm.com/digitalis/', 'playing': 'Digitally affected analog rock to calm the agitated heart.'},
        {'genre': 'electronica', 'listeners': 64, 'title': 'Dub Step Beyond', 'url': 'http://somafm.com/dubstep130.pls', 'bitrate': 128, 'homepage': 'http://somafm.com/dubstep/', 'playing': 'Dubstep, Dub and Deep Bass. May damage speakers at high volume.'},
        {'genre': 'oldies', 'listeners': 58, 'title': 'Seven Inch Soul', 'url': 'http://somafm.com/7soul130.pls', 'bitrate': 128, 'homepage': 'http://somafm.com/7soul/', 'playing': 'Vintage soul tracks from the original 45 RPM vinyl.'},
        {'genre': 'eclectic', 'listeners': 47, 'title': 'Black Rock FM', 'url': 'http://somafm.com/brfm130.pls', 'bitrate': 128, 'homepage': 'http://somafm.com/brfm/', 'playing': 'From the Playa to the world, for the annual Burning Man festival.'},
        {'genre': 'eclectic', 'listeners': 42, 'title': 'Covers', 'url': 'http://somafm.com/covers130.pls', 'bitrate': 128, 'homepage': 'http://somafm.com/covers/', 'playing': u"Just covers. Songs you know by artists you don't. We've got you covered."},
        {'genre': 'ambient/electronica', 'listeners': 42, 'title': 'Mission Control', 'url': 'http://somafm.com/missioncontrol130.pls', 'bitrate': 128, 'homepage': 'http://somafm.com/missioncontrol/', 'playing': 'Celebrating NASA and Space Explorers everywhere.'},
        {'genre': 'metal', 'listeners': 32, 'title': 'Metal Detector', 'url': 'http://somafm.com/metal130.pls', 'bitrate': 128, 'homepage': 'http://somafm.com/metal/', 'playing': 'From black to doom, prog to sludge, thrash to post, stoner to crossover, punk to industrial.'},
        {'genre': 'ambient/news', 'listeners': 25, 'title': 'SF 10-33', 'url': 'http://somafm.com/sf1033130.pls', 'bitrate': 128, 'homepage': 'http://somafm.com/sf/', 'playing': 'Ambient music mixed with the sounds of San Francisco public safety radio traffic.'},
        {'genre': 'specials', 'listeners': 16, 'title': 'SomaFM Specials', 'url': 'http://somafm.com/specials130.pls', 'bitrate': 128, 'homepage': 'http://somafm.com/specials/', 'playing': 'Special, seasonal and experimental broadcasts'},
        {'genre': 'holiday', 'listeners': 10, 'title': 'Christmas Lounge', 'url': 'http://somafm.com/christmas130.pls', 'bitrate': 128, 'homepage': 'http://somafm.com/christmas/', 'playing': 'Chilled holiday grooves and classic winter lounge tracks. (Kid and Parent safe!)'},
        {'genre': 'holiday', 'listeners': 9, 'title': 'Christmas Rocks!', 'url': 'http://somafm.com/xmasrocks130.pls', 'bitrate': 128, 'homepage': 'http://somafm.com/xmasrocks/', 'playing': 'Have your self an indie/alternative holiday season!'},
        {'genre': 'specials', 'listeners': 9, 'title': 'SomaFM Live', 'url': 'http://somafm.com/live130.pls', 'bitrate': 128, 'homepage': 'http://somafm.com/live/', 'playing': 'Special Live Events and rebroadcasts of past live events'},
        {'genre': 'holiday', 'listeners': 7, 'title': u"Jolly Ol' Soul", 'url': 'http://somafm.com/jollysoul130.pls', 'bitrate': 128, 'homepage': 'http://somafm.com/jollysoul/', 'playing': 'Where we cut right to the soul of the season.'},
        {'genre': 'holiday', 'listeners': 4, 'title': 'Xmas in Frisko', 'url': 'http://somafm.com/xmasinfrisko130.pls', 'bitrate': 128, 'homepage': 'http://somafm.com/xmasinfrisko/', 'playing': u"SomaFM's wacky and eclectic holiday mix. Not for the easily offended."},
        {'genre': 'live/news', 'listeners': 3, 'title': 'SF Police Scanner', 'url': 'http://somafm.com/scanner130.pls', 'bitrate': 128, 'homepage': 'http://somafm.com/scanner/', 'playing': 'San Francisco Public Safety Scanner Feed'}
    ]
    streams = {
    "support": [
        {'genre': 'faq', 'listeners': 6398, 'title': 'Commercial-free, listener supported radio station.', 'url': 'https://youtube.com/v/DAjSPgRPhzw', 'format': 'video/youtube', 'bitrate': 256, 'homepage': 'http://somafm.com/support/', 'playing': 'Unique among music stations, SomaFM depends on community donations to operate. PS: SomaFM Loves You!!'}
    ]}

    # All static
    def update_categories(self):
        pass

    # Just update entries with bitrate setting
    def update_streams(self, cat, search=None):
        if not cat in self.categories:
            return
        elif cat == "listen":
            rows = self.builtin
           # or self._real_parse()
        else:
            rows = self.streams[cat]
        
        # Overwrite bitrate
        bitreal = int(conf.somafm_bitrate) or 128
        biturl = int(conf.somafm_bitrate) or ""
        for i,row in enumerate(rows):
            rows[i]["format"] = "audio/mp3" if bitreal in (128,56,24) else "audio/aac"
            rows[i]["bitrate"] = int(bitreal)
            rows[i]["url"] = re.sub("\d*\.pls$", "%s.pls" % biturl, row["url"])
        
        # Resend stream list
        return rows

    # Disabled at runtime.
    def _real_parse(self):
        html = ahttp.get("http://somafm.com/listen/")
        ls = re.findall(r"""
            Listeners: \s* (\d+) \s*--> \s*
            <!-- .*? \(([\w/]+)\) \s* --> .*?
            <h3>  (.+?)  </h3> \s+
            <p[^>]*> (.+?) </p> .*?
            href="(/\w+\.pls)"
        """, html, re.X|re.S)
        rows = [
           dict(genre=g, title=t, playing=p, url="http://somafm.com"+u, listeners=int(l), bitrate=128, homepage="http://somafm.com"+re.sub("\d*\.pls$", "/", u))
            for l,g,t,p,u in ls
        ]
        log.DATA(rows)
        return rows
        
