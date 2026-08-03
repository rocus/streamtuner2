# encoding: UTF-8
# api: streamtuner2
# title: LiveRadio
# description: Irish/worldwide radio station directory
# url: http://liveradio.ie/
# version: 0.5
# type: channel
# category: radio
# config: -
#    { name: liveradio_tld, value: ie, type: select, select: ie=LiveRadio.ie|uk=LiveRadio.uk, description: Website to fetch from. }
# png:
#    iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAABB0lEQVR4nLWTQUpDMRCGv0lregDBI3gAfW/hRrp8ZOMh5PUMXkFcu7EbTxHd
#    CC4EhfQkQg/QR5txYQqvMdVHwdnMZJj555uQwH+YurpaNZUOqTWl5i5qGIusDxIAZgBGuBhCsiOgrq7WUa+tkReAjepHystQgmn8zt0As40y
#    skYa4HwfSS5w2otd8svtWurqHyvnCZcXAHRRW7v8nANnq6bSPk0ucFQS+M3G2fkduMqLrJF5d3zSTnyYATsXmhO89WLfix8A1NWjvwhek5+m
#    praLGibPC8knFwnEh4U1ct9FvUvoLk0uPbjiCgCPyd+KD0/WyKX4EPcJFLG2/8EaMeLDoE91sH0B3ERWq2CKMoYAAAAASUVORK5CYII=
# priority: default
# extraction-method: regex, dom, action-handler
#
# LiveRadio.ie, based in Ireland, is a radio station directory. It provides
# genre or country browsing (not in this plugin). Already lists over 5550
# stations (more unique selections). Also accepts user submissions.
#
# This channel loads their station logos as favicons. Even allows to utilize
# the live search function.
#
# However, station URLs have to be fetched in a second page request. Such
# the listings are unsuitable for exporting right away. OTOH the website is
# pretty fast; so no delay there or in fetching complete categories.
#

import re
from pq import pq
from config import *
from channels import *
import ahttp
import action


# Categorized directory, secondary URL lookup
class liveradio (ChannelPlugin):

    # control flags
    has_search = True
    listformat = "srv"
    audioformat = "audio/mpeg"
    titles = dict(listeners=False, bitrate=False, playing="Location")
    fixed_size = 30
    img_resize = 32

    # data store    
    categories = ["Top 20"]
    catmap = {"Top 20":"top-20"}
    base = "http://www.liveradio.ie/"
    

    # override meta based on TLD setting (.ie / .uk)
    def init2(self, parent):
        if not "liveradio_tld" in conf:
            conf.liveradio_tld = "ie"
        self.base = "http://www.liveradio.{}/".format(conf.liveradio_tld)
        self.meta["url"] = self.base
        #self.meta["title"] = "LiveRadio.{}".format(conf.liveradio_tld)
        

    # Extract genre links and URL aliases (e.g. "Top 20" maps to "/top-20")
    def update_categories(self):
        html = ahttp.get(self.base + "genres")
        self.categories = ["Top 20"]
        for row in re.findall(r"""<a href="/(stations/genre-[\w-]+)">([^<]+)</a>""", html):
            self.categories.append(unhtml(row[1]))
            self.catmap[unhtml(row[1])] = unhtml(row[0])


    # Fetch entries
    def update_streams(self, cat, search=None):

        # Assemble HTML (collect 1..9 into single blob prior extraction)
        html = ""
        page = 1
        while page < 9:
            page_sfx = "/%s"% page if page > 1 else ""
            if cat:
                add = ahttp.get(self.base + self.catmap[cat] + page_sfx)
            elif search:
                add = ahttp.get(self.base + "stations" + page_sfx, { "text": search, "country_id": "", "genre_id": ""})
            html += add
            if re.search('/\d+">Next</a>', add):
                page += 1
            else:
                break
        html = re.sub("</body>[\s\S]+<body[^>]*>", "", html)
        log.DATA(html)

        # dom or regex                
        if conf.pyquery:
            try:
                return self.pq_extract(html)
            except Exception as e:
                log.ERR(e)
        return self.rx_extract(html)

    # Extract all the things
    #
    # · entries utilize HTML5 microdata classification
    # · title and genre available right away
    # · img url is embedded
    # · keep station ID as `urn:liveradion:12345`
    #
    def rx_extract(self, html):
        r = []
        ls = re.findall("""
           itemtype="https?://schema.org/RadioStation"> .*?
           href="(?:https?://www.liveradio.\w+)?/stations/([\w-]+) .*?
           <img\s+src="/(files/images/[^"]+)"   .*?
           ="country">([^<]+)<  .*?
           itemprop="name"><a[^>]+>([^<]+)</a> .*?
           class="genre">([^<]+)<
        """, html, re.X|re.S)
        for row in ls:
            #log.DATA(row)
            id, img, country, title, genre = row
            r.append(dict(
                homepage = self.base + "stations/" + id,
                url = "urn:liveradio:" + id,
                playing = unhtml(country),
                title = unhtml(title),
                genre = unhtml(genre),
                img = self.base + img
            ))
        return r

    # using DOM extraction and itemtype/itemprop= attributes
    """
       <div class="list_item" itemscope itemtype="http://schema.org/RadioStation">
          <a class="image_outer" href="http://www.liveradio.ie/stations/soulconnexion-radio">
             <span class="image"><img src="/files/images/368787/resized/140x134c/soulconnexion_radio.jpg" alt="Soulconnexion Radio" itemprop="image" /></span>
             <span class="overlay"><!--  --></span>
             <span class="country">United Kingdom</span>
          </a>
       <div class="name" itemprop="name"><a href="http://www.liveradio.ie/stations/soulconnexion-radio">Soulconnexion Radio</a></div>
       <div class="genre">Funk, Soul</div>
    """
    def pq_extract(self, html):
        r = []
        html = pq(html).make_links_absolute(self.base)
        for radio in html.find("*[itemscope][itemtype='http://schema.org/RadioStation'], *[itemscope][itemtype='https://schema.org/RadioStation']"):
            log.DATA(radio)
            radio = pq(radio)
            href = radio.find("*[itemprop='name'] a").attr("href")
            id = re.search("/([\w-]+)$", href).group(1)
            r.append(dict(
                homepage = self.base + "stations/" + id,
                url = "urn:liveradio:" + id,
                playing = radio.find("*.country").text(),
                title = radio.find("*[itemprop='name']").text(),
                genre = radio.find("*.genre").text(),
                img = radio.find("img[itemprop='image']").attr("src")
            ))
        return r
      

    # Update `url` on station data access (incurs a delay for playing or recording)
    #
    # · utilizes action.handler["urn:liveradio"] → urn_resolve hook
    # · where the .update_streams() extraction stores `urn:liveradio:12345` as urls
    # · and this callback extracts the JS invocation URL from liveradio.de station summaries
    #
    def resolve_urn(self, row):
        if row.get("url").startswith("urn:liveradio"):
            id = row["url"].split(":")[2]
            html = ahttp.get(self.base + "stations/" + id)
            ls = re.findall("jPlayer\('setMedia',\s*\{\s*'?\w+'?:\s*'([^']+)'", html, re.M)
            if ls:
                row["url"] = unhtml(ls[0])
            else:
                log.ERR("No stream found on %s" % row["homepage"])
        return row

