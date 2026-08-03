# encoding: UTF-8
# api: streamtuner2
# title: RadioBrowser
# description: Community collection of stations; votes, clicks, homepage links.
# version: 0.5
# type: channel
# url: http://www.radio-browser.info/
# category: radio
# priority: optional
# config:
#   { name: radiobrowser_cat, type: select, value: tags, select="tags|countries|languages", description: Which category types to list. }
#   { name: radiobrowser_srv, type: select, value: all, select:"all|de1|fr1|nl1|old", description: API server to utilize. }
#   { name: radiobrowser_min, type: int, value: 20, description: Minimum stations to list a category/tag. }
# documentation: http://www.radio-browser.info/#ui-tabs-7
# png:
#   iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAABGdBTUEAALGPC/xhBQAAACBjSFJNAAB6JgAAgIQAAPoAAACA6AAAdTAAAOpgAAA6mAAAF3CculE8AAAABmJLR0QA/wD/
#   AP+gvaeTAAAAB3RJTUUH5AUNCjMF8h2w8AAABJBJREFUSMfVlVlsVFUcxn/nzr61004LbWmZKbUC1ioFYgOaEiQEAgEhRiRRVAxxiUTjgwkxxmCMEhdiCC5A0JiIJCSKvpgGZRGoslRp
#   FQot7XQD2tIya9tZ773HB2aaWpooJD74f7r3nHu+73+/7zvnwH9cYrLBCq8v+2gENED6e7r/ESyzTgGsQCwLMH5SAIVAFTAfSAOfAqnbaNoCPA18D/QbJ0xWAC8BQaAZCGQ6up3SgblA
#   BDgwkUAFdgKdmffy2wTPqvA50ArYJhLoWe3GfZyV0AP4AHdGun6gF0gCjPNIB4aAOCAM2dF8txsgN7O4GtgI2IEBYA2wWGq6XVc1FV13CUENQjwESKA/3+2WgBNwcdPkAKAaM+Z6gLqM
#   QUeAWmAD0ABUqMn0GaPLdHBP2xbzuWhxfufwFHmqNe/n1KY6V0q1rsJo9AIdwPYM1nagw9/TPZaiecAO4BJwGPgEOCwl66Wmfbf14lZDMGLc1tCWs2hhSfPUEpNLtiqrB+JfNP4UDw18
#   PfzK4zWKUVmekS0MtGWVyRIcB5YCw8CNjPYLTWZx+LOW9ff7h1LvWYWttCM2HfRero+W4TZTHBtx1tTN8q8tP7borV3LTsY1jbeFoGW8qYZQJEwoEtby3e5AhqAEeE5T5SPrX69UPHeX
#   v9kVubfYlxOjOVjJ+eAMGm9UkRYWcm0JSpx9Hoc9WBvp7hu80Z6YJxTRm2mSUCTMxBTlAR8Day12BVehdYnTmFQKeuu5di5OfmkZ51JzUYROvKcHvaMefX4ER01gmpbSn0cggFXAi0B9
#   hdfHxBQtBt6QujQW+mys3OwVPc1Rvtwb42xvEf2XujHPrkULDRLd/z6apjD0ayPpoio0i10ZPHtFZGJcCHwLqBN3aSFgkRLs+SZiJhctXTnoD24g57GXUc05yGQMtb8Lw7S7KNv0ArOX
#   TCPsvwKFJSimMbiyTFxvkcgPRAUyd0Rz8/tADYNVD+DRChhV7ThXPoswGDBXzsE0o5rqgqPMWpcmkA7iv9DBBYO8uYvgOjAKt54zjcAuIeRIMOzU/UOV2Kwj2BKdeExXMZgMSKEgzDYM
#   DidCGyKhxEjbVYaHk0hVAoSA3VmCMQ9CkTD5brcGnCIR/1EuXN42WrF6gRQuS3HfbkqjP+CbmSasFpHSrajBAFeONhHKXUDKHCAp+qLXT8sd6YC2TSiiHtD9Pd2T3we+o5dRFdXhiLv2
#   5yqW1bPkHrp2fkVesQNlqpdrgTKiLZcx31OL69HNeMu2oNtaD7RqG59xG7sSx73vjGFNehSPOsNYUrbRlCnxblRPd3YoT5C7ZgX9V8NcPHiR8IkTGIvKsS5+EqP1T5LGnvZo2vnhDPYm
#   Tp7Z+jesSf8AoOiXJu77Yw6XZ7Y/bEo7Pyh2XKjxOXaJ9vNPkdC8CM9U0hZFt+YeOmvPO/baitIvG/a1f8T5mlf/HQGAu+kE0zurCRQMlNpkfJ3H3rQ0OlxXqulWqYl0r2pMHlItkW/s
#   qrW/N1ZGcpmHO6t9EpAUnTpiKTnTUDDl9G8ed/NxSwMSEdx+h6D/l/oLDIPO4XsJSDcAAAAldEVYdGRhdGU6Y3JlYXRlADIwMjAtMDUtMTNUMDg6NTE6MTYrMDI6MDBdnX3HAAAAJXRF
#   WHRkYXRlOm1vZGlmeQAyMDIwLTA1LTEzVDA4OjUxOjA1KzAyOjAw0YLfeAAAABl0RVh0U29mdHdhcmUAQWRvYmUgSW1hZ2VSZWFkeXHJZTwAAAAASUVORK5CYII=
# x-icon-src: openclipart:tape.png
# x-service-by: segler_alex
# extraction-method: json
#
#
# Radio-Browser is a community-collected list of internet radios.
# Currently lists ≥25000 streaming stations, and tracks favourited
# entries. Furthermore includes station homepage links!
#
# If you change the categories between tags/countries/languages,
# please apply [Channel]→[Reload Category Tree] afterwards.
#
# Also has an awesome JSON API, has an excellent documentation,
# thus is quite pleasant to support. It's also used by Rhythmbox /
# VLC / Clementine / Kodi / RadioDroid / etc.


import re
import json
from config import *
from channels import *
from uikit import uikit
import ahttp


# API endpoints:
# https://de1.api.radio-browser.info/#General
#
# ENTRY sets:
#  {
#    "stationuuid":"960e57c5-0601-11e8-ae97-52543be04c81", "name":"SRF 1",
#    "url":"http://stream.srg-ssr.ch/m/drs1/mp3_128", "homepage":"http://ww.srf.ch/radio-srf-1",
#    "favicon":"https://upload.wikimedia.org/wikipedia/commons/thumb/d/d3/Radio_SRF_1.svg/205px-Radio_SRF_1.svg.png",
#    "tags":"srg ssr,public radio",
#    "country":"Switzerland", "countrycode":"CH", "state":"", "language":"german", "votes":0,
#    "lastchangetime":"2019-12-12 18:37:02", "codec":"MP3", "bitrate":128, "hls":0, "lastcheckok":1,
#    "lastlocalchecktime":"2020-01-08 23:18:38", "clickcount":0,
#  }
#
class radiobrowser (ChannelPlugin):

    # control flags
    has_search = True
    listformat = "pls"
    titles = dict(listeners="Votes", bitrate="Bitrate", playing="Country")
    api_old = "http://www.radio-browser.info/webservice/json/"
    api_url = "http://{}.api.radio-browser.info/json/"  # de1, nl1, all (from conf.radiobrowser_srv)
    categories = ["topvote", "topclick", "60s", "70s", "80s", "90s", "adult contemporary", "alternative", "ambient", "catholic", "chillout", "christian", "classic hits", "classic rock", "classical", "college radio", "commercial", "community radio", "country", "dance", "electronic", "folk", "hiphop", "hits", "house", "indie", "information", "jazz", "local music", "local news", "lounge", "metal", "music", "news", "noticias", "npr", "oldies", "pop", "public radio", "religion", "rock", "soul", "sport", "talk", "techno", "top 40", "university radio", "variety", "world music"]
    pricat = ("topvote", "topclick")
    catmap = { "tags": "bytag", "countries": "bycountry", "languages": "bylanguage" }
    tagmap = { "tags": "tag", "countries": "country", "languages": "language" }

    # hook menu
    def init2(self, parent):
        if parent:
            uikit.add_menu([parent.streammenu, parent.streamactions], "Share in Radio-Browser", self.submit, insert=5)
            parent.hooks["play"].append(self.click)

    # votes, and tags, no countries or languages
    def update_categories(self):
        params = {"order":"name", "reverse":"false", "hidebroken":"true"} 
        self.categories = list(self.pricat) + [grp["name"] for grp in filter(
            lambda grp: grp["stationcount"] >= conf.radiobrowser_min,
            self.api(conf.radiobrowser_cat, params)
        )]
            

    # Direct mapping
    def update_streams(self, cat, search=None):

        # title search
        if search:
            data = self.api(
                "stations/search",
                {"search": search, "limit": conf.max_streams}
            )
        # topclick, topvote
        elif cat in self.pricat:
            self.status(0.3)
            data = self.api(
                "stations/{}/{}".format(cat, conf.max_streams),
                {"limit": conf.max_streams}
            )
        # empty category
        #elif cat in ("tags", "countries", "languages"):
        #    return [
        #         dict(genre="-", title="Placeholder category", url="offline:")
        #    ]
        # search by tag, country, or language
        else:
            data = self.api(
                "stations/search",
                {
                    self.tagmap[conf.radiobrowser_cat]: cat,
                    "hidebroken": "true",
                    "order": "click",
                    "limit": conf.max_streams
                }
            )
            #data = self.api("stations/" + self.catmap[conf.radiobrowser_cat] + "/" + cat)

        if len(data) >= 5000:
            data = data[0:5000]
        self.status(0.75)

        r = []
        for e in data:
            r.append(dict(
                genre = e["tags"],
                url = e["url"],
                format = mime_fmt(e["codec"]),
                title = e["name"],
                homepage = ahttp.fix_url(e["homepage"]),
                playing = e["country"],
                listeners = int(e["votes"]),
                bitrate = int(e["bitrate"]),
                favicon = e["favicon"]
            ))
        return r


    # fetch multiple pages
    def api(self, method, params={}, post=False, **kwargs):
        # api/srv switcheroo
        if not "radiobrowser_srv" in conf:
            conf.radiobrowser_srv = "all"
        if conf.radiobrowser_srv == "old":
            srv = self.api_old
        else:
            srv = self.api_url.format(conf.radiobrowser_srv)
        # request + json decode
        j = ahttp.get(srv + method, params, post=post, **kwargs)
        try:
            return json.loads(j, strict=False)   # some entries contain invalid character encodings
        except:
            return []


    # callback for general stream play event
    def click(self, row, channel):
        if not channel == self:
            return
        # fetch uuid, then register click
        uuid = self.api("stations/byurl", {"url": row.get("url")}, quieter=1)
        if uuid:
            if isinstance(uuid, list): # just vote on the first entry
                uuid = uuid[0]
            log.CLICK(self.api("url/{}".format(uuid["stationuuid"], quieter=1)))


    # Add radio station to RBI
    def submit(self, *w):
        cn = self.parent.channel()
        row = cn.row()
        # convert row from channel
        data = dict(
            name = row["title"],
            url = row["url"],
            homepage = row["homepage"],
            #favicon = self.parent.favicon.html_link_icon(row["url"]), # no longer available as module
            tags = row["genre"].replace(" ", ","),
        )
        # map extra fields
        for _from,_val,_to in [("playing","location","country")]:
            #country	Austria	The name of the country where the radio station is located
            #state	Vienna	The name of the part of the country where the station is located
            #language	English	The main language which is used in spoken text parts of the radio station.
            if _from in cn.titles and cn.titles[_from].lower() == _val:
                data[_to] = _from
        # API submit
        j = self.api("add", data, post=1)
        log.SUBMIT_RBI(j)
        if j and "ok" in j and j["ok"] == "true" and "id" in j:
            self.parent.status("Submitted successfully to Radio-Browser.info, new station id #%s." % j["id"], timeout=15)

