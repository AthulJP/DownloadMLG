"""
Copyright (c) 2018, Athul Perumpillichira
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer.
2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

The views and conclusions contained in the software and documentation are those
of the authors and should not be interpreted as representing official policies,
either expressed or implied, of the DownloadMLG project.
"""

import argparse
import requests
from html5_parser import parse
import json

ArgParser = argparse.ArgumentParser(description="Return the URL for the M3U file " +
                                    "containing the playlist for any OWL VOD")
ArgParser.add_argument("URL", help="The URL containing the link to the embeddable MLG player")
ArgParser.add_argument("Resolution", help="Desired video resolution. Options are 360, 480, 720 and 1080")
Arguments = ArgParser.parse_args()

#Get the HTML of the embedded MLG player
PlayerEmbedRequest = requests.get(Arguments.URL)
PlayerEmbedHTML = PlayerEmbedRequest.text
PlayerEmbedRoot = parse(PlayerEmbedHTML)

#Get the contents of the script tag containing the media items
ScriptTag = PlayerEmbedRoot.xpath("./body//script")[0]
JSONText = ScriptTag.text

#Get the URL of the resolution list from the script
BraceIndex = JSONText.index("{", JSONText.index("mediaItem"))
SemicolonIndex = JSONText.index(";", JSONText.index("}]};"))
JSONText = JSONText[BraceIndex:SemicolonIndex]
MediaItem = json.loads(JSONText)
ResListURL = MediaItem["streams"][0]["streamUrl"]
ResListURL = "https:" + ResListURL

#Get the resolution list
ResListRequest = requests.get(ResListURL)
ResList = ResListRequest.text

#Get the transport stream playlist URL from the resolution list
TSListName = ""
LineIndex = 0
for i in range(4):
    LineIndex = ResList.index("#EXT-X-STREAM-INF", LineIndex+1)
    ResIndex = ResList.index("x", LineIndex)
    CommaIndex = ResList.index(",", ResIndex)
    ResString = ResList[ResIndex+1:CommaIndex]

    if ResString == Arguments.Resolution:
        URIIndex = ResList.index("\n", CommaIndex)
        EndIndex = ResList.index("\n", URIIndex+1)
        TSListName = ResList[URIIndex+1:EndIndex]
        break

IdentifierIndex = ResListURL.index(TSListName[:10])
URLPrefix = ResListURL[:IdentifierIndex]
TSListURL = URLPrefix+TSListName

#Put this in VLC or M3U8X to get the VOD
print(TSListURL)
