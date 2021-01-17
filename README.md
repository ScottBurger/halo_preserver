# halo_preserver
More info at https://svburger.com

Python scripting to gently scrape halo.bungie.net and save a user's recorded game data for Halo 2 and Halo 3

Halo.bungie.net was a great resource for checking your halo-related stats in the xbox 360 era. Years ago I'd always flock to https://halo.bungie.net/stats/halo3/careerstats.aspx?player=AI52487963 and check my stats because I was obsessed and had nothing better to do. Because it's planned to shut the halo data off in Feb 2021, this script will help preserve the raw html data to allow a user to mine the offline data afterwards.

There are 4 functions here:

`halo2_get_files("GAMERTAG")`
This loops over all the pages of game data for a given gamertag, produces a list of the game ids, then for each game id downloads the raw html file associated to it. That will allow data hoarders like me in the future to mine it for fun stats.

`halo3_get_files("AI52487963")`
This does the same thing, but for Halo 3's matchmaking and custom game lists only.

`halo3_get_campaign_files("AI52487963")`
This does the same thing, but specifically for Halo 3 campaign files, because the URL structure is slightly different.

`halo3_main_stats_page("AI52487963")`
Finally this function will dump the raw html of the main stats page for a gamertag, since it's a decent aggregation page.


