# encoding: utf-8
# title: Version/update check on startup
# description: Checks fossil repository for newer version
# version: 1.1
# depends: streamtuner2 >= 2.2.0
# priority: default
# type: feature
# category: ui
#
# Probes http://fossil.include-once.org/streamtuner2/cat/releases.json
# for newer version. Activates only on ~20% of startups, only adds a statusbar
# notification after 5 seconds, no nag screen.


import json
import ahttp
import random
import threading
from config import plugin_meta
from channels import FeaturePlugin

# Update notification
class version_check(FeaturePlugin):

    # Hook timer
    def init2(self, parent):
        if random.randint(0,5):
            return
        threading.Timer(5, self.check).start()

    # Request release.json, notify in status bar
    def check(self, *x, **y):
        try:
            j = ahttp.get("http://fossil.include-once.org/streamtuner2/cat/releases.json", timeout=5, quieter=1)
            j = json.loads(j)
            max = j["releases"][0]["version"] # alread ordered newest-first
            m = plugin_meta(module="st2", extra_base=["config"])
            ver = m["version"]
            if ver < max:
                self.status(text="A newer streamtuner2 version (→%s) is available." % str(ver), timeout=7, icon="gtk-dialog-info")
        except:
            None