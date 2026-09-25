Streamtuner2 is an audio radio browser that is hardly maintained anymore. I find it a usefull tool to find radio stations all over the world in many languages. It has access to many radiobrowsers (such as Shoutcast, Surfmusic) but some were not working anymore. Some of these browsers work again and are slightly improved. 

My source for this project was the current deb package for Streamtuner2 version 2.2.2 . I changed many of the python files in the deb-package file because of old constructs (Python2) and because some browsers have changed their API or webpage. You can clone  this repository and run streamtuner2 simple by the command: python3 st2.py. You can also copy the "streamtuner2.py" file to for example /usr/bin/. Don't forget to change the invocation script according to the place where your python files are.

You are free to use streamtuner2 as you wish. If you have comments/bugs or suggestions you can post an issue. I must stress that I am not the (new) maintainer of this program: I simply miss the knowledge or experience for that. Said that, I can try to solve problems!


