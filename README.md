DownloadMLG
===========

Small script for getting the M3U playlist file of an OWL VOD from MLG.com (The quality is significantly better than Twitch). I have only tested this with Python 3.6

Usage:

python3 DownloadMLG.py <URL> <Resolution>

* URL: The URL of the embedded MLG player from the OWL website

* Resolution: Desired resolution for the VOD. Options are 360, 480, 720 and 1080.

The URL of the embedded MLG player for a particular video can be found by doing the following (on Firefox, at least):

* Go to https://overwatchleague.com/videos

* Inspect the element of the VOD you want to download, doesn't matter if it's the title or the thumbnail

* Select the link in the embed attribute of the link of either the "Card-imageholder" div or the "Card-body"

This is the URL required by the script.