# encoding: utf-8
# api: streamtuner2
# title: RadioTray hook
# description: Allows to bookmark stations to RadioTray/NG
# version: 0.9
# type: feature
# category: bookmarks
# depends: deb:python-dbus, deb:streamtuner2, deb:python-xdg
# config:
#   { name: radiotray_map, type: select, value: "group", select: 'root|group|category|asis|channel|play', description: 'Map genres to default RadioTray groups, or just "root".' }
# url: http://radiotray.sourceforge.net/
# priority: extra
# id: streamtuner2-radiotray
# extraction-method: xml
# pack: radiotray.py
# fpm-prefix: /usr/share/streamtuner2/channels/
#
# Adds a context menu "Add in RadioTray.." for bookmarking.
# Should work with old Radiotray and Radiotray-NG. It will
# now probe for RTNG first and prefers to edit its bookmark
# list.
#
# The mapping options:
#   · "root" is just meant for the old Radiotray format.
#   · "group" tries to fit genres onto existing submenus.
#   · "category" maps just the channel category.
#   · "channel" instead creates `Shoutcast - Rock` entries.
#   · "asis" will transfer the literal station genre.
#   · "play" for RT-NG to stream instantly (no bookmarking).
#
# With the old Radiotry this plugin will fall back to just
# playUrl() until the addRadio remote call is added.
# The patch for radiotray/DbusFacade.py would be:
#   +
#   +    @dbus.service.method('net.sourceforge.radiotray')
#   +    def addRadio(self, title, url, group="root"):
#   +        self.dataProvider.addRadio(title, url, group)
#
# Displays existing radiotray stations in ST2 bookmarks (from
# either old bookmarks.xml or RT-NG bookmarks.json). If you're
# using RT-Lite, then symlink its ~/.config dir to `radiotray`.
#
# This plugin may be packaged up separately.
#

from config import *
from channels import *
from uikit import uikit
import re
import dbus
import json
from xdg.BaseDirectory import xdg_data_home, xdg_config_home
from xml.etree import ElementTree


# not a channel plugin, just a category in bookmarks, and a context menu
class radiotray (object):

    # plugin info
    module = 'radiotray'
    meta = plugin_meta()
    # bookmarks cat
    parent = None
    bm = None
    # radiotray config file / bookmarks
    rt_xml = "%s/%s/%s" % (xdg_data_home, "radiotray", "bookmarks.xml")
    rtng_json = "%s/%s/%s" % (xdg_config_home, "radiotray-ng", "bookmarks.json")


    # DBUS connector
    def radiotray(self):
        return dbus.Interface(
            dbus.SessionBus().get_object(
                "net.sourceforge.radiotray",
                "/net/sourceforge/radiotray"
            ),
            "net.sourceforge.radiotray"
        )
    def radiotray_ng(self):
        return dbus.Interface(
            dbus.SessionBus().get_object(
                "com.github.radiotray_ng",
                "/com/github/radiotray_ng"
            ),
            "com.github.radiotray_ng"
        )


    # hook up to main tab
    def __init__(self, parent):

        # keep reference to main window    
        self.parent = parent
        self.bm = parent.channels["bookmarks"]
        conf.add_plugin_defaults(self.meta, self.module)

        # create category
        self.bm.add_category("radiotray", plugin=self);
        self.bm.category_plugins["radiotray"] = self #.update_streams(cat="radiotray")
        self.bm.reload_if_current(self.module)

        # add context menu
        uikit.add_menu([parent.streammenu, parent.streamactions], "Add in RadioTray/NG", self.share, insert=4)
        

    # load RadioTray bookmarks
    def update_streams(self, cat):
        r = []
        # RT-NG
        try:
            for group in json.load(open(self.rtng_json, "r")):
                genre = group["group"]
                for ls in group["stations"]:
                    r.append({
                        "genre": genre,
                        "title": ls["name"],
                        "url": ls["url"]
                    })
        except Exception as e:
            log.ERR("Extracting from radiotray-ng bookmarks.json failed:", e)
        # RT XML
        try:
            for group in ElementTree.parse(self.rt_xml).findall(".//group"):
                for bookmark in group.findall("bookmark"):
                    r.append({
                        "genre": group.attrib["name"],
                        "title": bookmark.attrib["name"],
                        "url": bookmark.attrib["url"],
                        "playing": "",
                    })
        except Exception as e:
            log.ERR("Extracting from radiotray bookmarks.xml failed:", e)
        return r


    # send to 
    def share(self, *w):
        row = self.parent.row()
        if row:
            group = self.map_group(row.get("genre", self.parent.channel().current))
            log.PROC("mapping genre '%s' to RT group '%s'" % (row["genre"], group))

            # Radiotray-NG
            try:
                if conf.radiotray_map == "play":
                    self.radiotray_ng().play_url(row["url"])
                else:
                    self.radiotray_ng().add_radio(row["title"], row["url"], group)
            except Exception as e:
                log.ERR("RTNG DBUS error", e)
                try:
                    cfg = self.radiotray_ng().get_config()
                    self.save_rtng_json(cfg, row, group)
                    self.radiotray_ng().reload_bookmarks()
                    self.parent.status("Exported to Radiotray. You may need to use Preferences > Reload Bookmarks.")
                except Exception as e:
                    log.ERR("radiotray-ng not active", e)

            # RadioTray doesn't have an addRadio method yet, so just fall back to play the stream URL
            try:
                self.radiotray().addRadio(row["title"], row["url"], group)
            except:
                try:
                    self.radiotray().playUrl(row["url"])
                except:
                    log.ERR("radiotry-old not active")
        pass
        
    # manually add to RTNG bookmarks.json
    def save_rtng_json(self, cfg, row, group):
        fn = json.loads(cfg)["bookmarks"]
        j = json.load(open(fn, "r"))
        found = None
        group = {"root": "streamtuner2", "": "streamtuner2"}.get(group, group)
        # find existing group
        for g in j:
            if g["group"] == group:
                found = g
                break
        # else add new group
        if not found:
            found = {
                "group": group,
                "image": None,
                "stations": []
            }
            j.append(found)
        # overwrite bookmarks.json
        if found:
            found["stations"].append({
                "image": None,
                "name": row["title"],
                "url": row["url"]
            })
            json.dump(j, open(fn, "w"), indent=4)

    # match genre to RT groups
    def map_group(self, genre):
        if not genre or not len(genre) or conf.radiotray_map == "root":
            return "root"
        if conf.radiotray_map == "channel":
            return "%s - %s" % (self.parent.current_channel, self.parent.channel().current)
        if conf.radiotray_map == "asis":
            return genre  # if RadioTray itself can map arbitrary genres to its folders
        if conf.radiotray_map == "category":
            genre = self.parent.channel().current
        # else "group" - find first fit for station genre
        map = {
            "Jazz": "jazz|fusion|swing",
            "Latin": "latin|flamenco|tango|salsa|samba",
            "Classic Rock": "classic rock",
            "Classical": "classic|baroque|opera|symphony|piano|violin",
            "Pop / Rock": "top|pop|rock|metal",
            "Oldies": "20s|50s|60s|70s|oldie",
            "Chill": "chill|easy|listening",
            "Country": "country|bluegrass|western",
            "Techno / Electronic": "techno|electro|dance|house|beat|dubstep|progressive|trance",
            "Community": "community|talk|sports|spoken|educational",
        }
        #for str in (genre,title):
        for cat,rx in map.items():
            if re.search(rx, genre, re.I):
                return cat
        return "root"

