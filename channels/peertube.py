# encoding: UTF-8
# api: streamtuner2
# title: Peertube
# description: Video browser for Peertube servers.
# type: channel
# version: 0.2
# priority: extra
# url: https://joinpeertube.org/
# category: video
# config:
#    { name: peertube_srv,  type: select,  value: "peertube.live",  select: "peertube.live|peertube.anarchmusicall.net|hostyour.tv|peertube.co.uk|troo.tubevideo.ploud.fr|video.ploud.fr|peertube.bittube.tv|bittube.video|peertube.video|libretube.net",  description: "Primary instance/server to query", category: server }
# priority: default
# png:
#    iVBORw0KGgoAAAANSUhEUgAAABIAAAASCAMAAABhEH5lAAAABGdBTUEAALGPC/xhBQAAACBjSFJNAAB6JgAAgIQAAPoAAACA6AAAdTAAAOpgAAA6mAAAF3Ccul
#    E8AAABO1BMVEUAAAAhHyAnIiAjICDxaA3uZw0eGx13d3dzc3Nwc3YhHyAhHyAhHyAhHyAhHyAhHyAhHyAhHyAhHyAhHyAhHyAhHyAiHyAgHyA5KB7cYQ//bQwe
#    HiCbShXwaA3xaA3xaA0hHyAhHyAhHyAAACn2ag3xaA3xaA3xaA3xaA3xaA0gHh8hHyDxaA3xaA3xaA3xaA3xaA0sKislIyQfHR4dGxzxaA3xaA3xaA1paWlubm
#    50dHR5eXnxaA3xaA10dHRzc3Nzc3Nzc3Nzc3PxaA3xaA3xaA1zc3Nzc3Nzc3Nzc3M4eKPzaAvxaA3xaA1zc3Nxc3S9bDfxaA3xaA3xaA1zc3ODcmbkaRf/ZwBz
#    c3Nzc3Nyc3RtdHpzc3Nzc3Nzc3Nzc3Nzc3Nzc3Nzc3Nzc3Nzc3MhHyDxaA1zc3MAAABrSqpYAAAAZXRSTlMAAAAAAAAAAAAAA4ROBgK56YIX/EXoGfaNOAd+P8
#    SFF/u7SAQl2/u6RwQC7Sba6oMZA31IBfrAQwODRAXDPQK56oMa5oAcAvu7QwQl/L/nhEDEgRr1kjYE6XwdAfq9RwV9FwOGUtq6k/IAAAABYktHRACIBR1IAAAA
#    CXBIWXMAAA3XAAAN1wFCKJt4AAAAB3RJTUUH5AUPCjUlNSD/NQAAAMJJREFUGNNjYODi5uFlZEABfPwCgkKMjKhCqcL8IigKgUKpqaLcYkzMqEKp4hKSUiwoQg
#    LSMrJy8iwscCEFRSVlFVU1dQ1NiJgWvzbQRlYd3bQ0PX0DsEJDI2MTNgYWkFCaqZk5SMjC0sqaHSqkZmMLErKzd3B04gALObu4gjW62ae7e3h6eev6+MKMBwql
#    p/v5BwQGBcMcARZKDwkNC4c7FSwUERkVzcmAJBQTGxfPgeRtN3uHhERkAQaGpOQUFCUMAJsmJ8NW/rFWAAAAJXRFWHRkYXRlOmNyZWF0ZQAyMDIwLTA1LTE1VD
#    A4OjUzOjM3KzAyOjAw7qvI1wAAACV0RVh0ZGF0ZTptb2RpZnkAMjAyMC0wNS0xNVQwODo1MzozNyswMjowMJ/2cGsAAAAASUVORK5CYII=
# depends: bin:youtube-dl
# extraction-method: json
#
#
# Browser for PeerTube instances (configurable in settings) and
# video categories. Even loads video snapshots as favicons, hencewhy
# the display is slightly stretched in comparison to radio channels.
#
# The chosen main server has some influence over sorting, but usually
# includes entries from peered instances.
#
# Currently there's no player for PeerTube /embed/ links, so the
# video/youtube MIME should be combined with `youtuble-dl` even
# for VLC. Else just use the [Station] homepage for the web view.
#
# Per default fetches 200 entries (not conf.max_streams), because
# it's a little slower on some servers. And the standard sorting
# is publication time (newest videos atop).
#


from config import *
from channels import *

import ahttp
import json
import re



# Peertube
#
# /video queries are public, so we don't even need OAuth for most
# of the instances.
# The API and resultsets are also quite simple to work with.
# Apart from the /embed/ url not being useful for direct playback.
#
# API
#
#  · https://peer.tube/api/v1/oauth-clients/local
#     {"client_id":"3ouzl1…","client_secret":"oLFjYTCjw…"}
#
#  · https://peer.tube/api/v1/videos/categories
#     {"1":"Music","2":"Films","3":"Vehicles","4":"Art","5":"Sports",…}
#
#  · https://peer.tube/api/v1/videos?categoryOneOf=1
#     data[
#      {
#         "publishedAt" : "2020-05-10T07:01:18.843Z",
#         "embedPath" : "/videos/embed/b60bae06-82bf-4925-b1ef-b8fc6903ae28",
#         "originallyPublishedAt" : "2014-03-31T07:00:42.000Z",
#         "nsfw" : false,
#         "language" : {
#            "id" : "te",
#            "label" : "Telugu"
#         },
#         "createdAt" : "2020-05-10T07:01:18.843Z",
#         "privacy" : {
#            "label" : "Public",
#            "id" : 1
#         },
#         "id" : 184339,
#         "views" : 1,
#         "duration" : 349,
#         "thumbnailPath" : "/static/thumbnails/b60bae06-82bf-4925-b1ef-b8fc6903ae28.jpg",
#         "description" : "Lyrics : Lakshmi Valli Devi Bijibilla\nMusic : Kanakesh Rathod\nPublisher : Bijibilla Rama Rao ",
#         "dislikes" : 0,
#         "uuid" : "b60bae06-82bf-4925-b1ef-b8fc6903ae28",
#         "likes" : 0,
#         "category" : {
#            "label" : "Music",
#            "id" : 1
#         },
#         "updatedAt" : "2020-05-10T08:02:35.008Z",
#         "licence" : {
#            "id" : 7,
#            "label" : "Public Domain Dedication"
#         },
#         "channel" : {
#            "avatar" : null,
#            "url" : "https://peertube.slat.org/video-channels/sudhanva_sankirtanam",
#            "displayName" : "Sudhanva Sankirtanam",
#            "id" : 16607,
#            "name" : "sudhanva_sankirtanam",
#            "host" : "peertube.slat.org"
#         },
#         "isLocal" : false,
#         "name" : "Alayam Devaalayam-Kanakesh Rathod",
#         "account" : {
#            "id" : 25475,
#            "name" : "bijibilla_rama_rao",
#            "host" : "peertube.slat.org",
#            "displayName" : "Bijibilla Rama Rao",
#            "url" : "https://peertube.slat.org/accounts/bijibilla_rama_rao",
#            "avatar" : null
#         },
#         "previewPath" : "/static/previews/b60bae06-82bf-4925-b1ef-b8fc6903ae28.jpg"
#      },
#
#  · peertube.mygaia.org/videos/embed/f1208e4f-425f-473b-9449-bc168798d604
#
# INTERNA
#
# The /embed/ section of the url can sometimes be substituted with:
#  · /videos/watch/UUID
#  · /static/streaming-playlists/hls/UUID/master.m3u8
#  · /static/webseed/UUID.mp4
# Though that's sometimes blocked / or not consistently supported on all instances.
# Which is why resolve_urn does an extra /api/v1/videos/uuid lookup.
#
class peertube (ChannelPlugin):

    # control attributes
    listformat = "href"
    has_search = True
    audioformat = "video/youtube"
    titles = dict( genre="Channel", title="Title", playing="Description", bitrate=False, listeners=False )
    srv = conf.peertube_srv
    image_resize = 48
    fixed_size = [48,32]

    categories = [] 
    catmap = { "Music": "1" }


    # just a static list for now
    def update_categories(self):
        cats = self.api("videos/categories")    # { "1": "Music" }
        self.catmap = dict((k,int(v)) for v,k in cats.items())   # { "Music": 1 }
        self.categories = sorted(self.catmap, key=self.catmap.get)   # sort by value


    # retrieve and parse
    def update_streams(self, cat, search=None):
        if search:
            method = "search/videos"
            params = {
                "search": search,
                "count": 100,
                "sort": "-match",
                "nsfw": "false"
            }
        elif not cat in self.catmap:
            return []
        elif cat:
            method = "videos"
            params = {
                "categoryOneOf": self.catmap[cat],
                "count": 100,
                "sort": "-publishedAt",
                "nsfw": "false"
            }

        # fetch + map
        self.status(0.9)
        #log.DATA(video)
        return [
            self.map_data(video) for video in self.api(method, params)
        ]

    # peertube entry to streamtunter2 dict
    def map_data(self, v):
        #log.DATA(v)
        url = "http://" + v["channel"]["host"]
        return dict(
            uuid = v["uuid"],
            genre = v["category"]["label"],
            title = v["name"],
            playing = re.sub("\s+", " ", v["description"]) if v.get("description") else "",
            url = "urn:peertube:{}".format(v["uuid"]),
            homepage = url + v["embedPath"].replace("/embed/", "/watch/"),
            #homepage = v["channel"]["url"],
            format = self.audioformat,
            img = url + v["thumbnailPath"]
        )


    # fetch one or multiple pages from API
    def api(self, method, params={}, debug=False, count=200, **kw):
        r = []
        for i in range(0, 5):
            self.status(i / 6.0)
            add = json.loads(
                ahttp.get("http://{}/api/v1/{}".format(conf.peertube_srv, method), params, **kw)
            )
            if not add.get("data"):
                return add
            else:
                r += add["data"]
                params["start"] = 100 * (i+1);
            if len(r) >= count:
                break
        return r


    # from uuid to downloadUrl
    def resolve_urn(self, row):
        video = self.api("videos/" + row["uuid"])
        #log.DATA(video)
        search = (
            ("streamingPlaylists", "playlistUrl", "audio/mpeg-url"),
            ("files", "fileDownloadUrl", "video/mpeg"),
            ("files", "fileUrl", "video/mpeg")
        )
        for section, entry, format in search:
            for row in video.get(section, []):
                if row.get(entry):
                    row["url"] = row[entry]
                    row["format"] = format
                    return row
        # else use /watch/ url
        row["url"] = row["homepage"]
        return row

