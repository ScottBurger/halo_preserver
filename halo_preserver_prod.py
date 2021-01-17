# -*- coding: utf-8 -*-
"""
https://svburger.com/2021/01/16/halo-data-evolved/

This script will gently scrape halo.bungie.net for a given gamertag's halo 2 or halo 3 data.

The idea here is to grab the data associated with a user before the site's complete removal
of the data on Feb 9 2021. Once the raw html is downloaded, the local data can then be mined
to develop statistical measurements.
"""


import requests
import re
import time
import os.path


def halo2_game_ids(gamertag):
   """
   hard download of all pages of games
   maybe alter this to not store on hdd?
   """ 
   
   max_url = 'https://halo.bungie.net/stats/playerstatshalo2.aspx?player={}'.format(gamertag)
   max_data = requests.get(max_url)
   max_data_text = max_data.text
   result = re.search('\\\\"PageCount\\\\":(.*),\\\\"EditMode\\\\":', max_data_text)
   max_pages = int(result.group(1))
    
   
   game_ids_list = []
   
   for i in range(1,max_pages+1):
      
       print("getting halo2 game id data for {} page {}/{}".format(gamertag,i,max_pages))

        #request page data
       url = 'https://halo.bungie.net/stats/playerstatshalo2.aspx?player={}&ctl00_mainContent_bnetpgl_recentgamesChangePage={}'.format(gamertag,i)
       page_data = requests.get(url)
       page_data_text = page_data.text
      
        #extract game ids from page
       game_ids = re.findall('gameid=(.*)&amp',page_data_text)
       game_ids_list = game_ids_list + game_ids
       
       time.sleep(2) # to not overload HBN with response calls
    
       print("done!")

   return game_ids_list



def halo2_game_id_download(game_id, gamertag):
    """
    for each game id, hard download all the game data

    hard download because it's going away soon and its
    easier to experiment offline than to hit HBN with
    response calls every time
    """

    game = 'https://halo.bungie.net/Stats/GameStatsHalo2.aspx?gameid={}&player={}'.format(game_id, gamertag)
    game_data = requests.get(game)
    game_text = game_data.text
    
    save_path = ''
    name_of_file = '{}_halo2_game_{}.txt'.format(gamertag,game_id)
    complete_name = os.path.join(save_path, name_of_file)
    
    file = open(complete_name, "w")
    file.write(game_text)
    file.close
    
    time.sleep(2)
         
    
    
    
    
    
def halo3_game_ids(gamertag):
   """
   returns list of all custom and matchmaking, and campaign game ids
   """
   
   custom_url = 'https://halo.bungie.net/stats/playerstatshalo3.aspx?player={}&cus=1'.format(gamertag)
   custom_data = requests.get(custom_url)
   custom_data_text = custom_data.text
   custom_result = re.search('\\\\"PageCount\\\\":(.*),\\\\"EditMode\\\\":', custom_data_text)
   custom_pages = int(custom_result.group(1))

   mm_url = 'https://halo.bungie.net/stats/playerstatshalo3.aspx?player={}'.format(gamertag)
   mm_data = requests.get(mm_url)
   mm_data_text = mm_data.text
   mm_result = re.search('\\\\"PageCount\\\\":(.*),\\\\"EditMode\\\\":', mm_data_text)
   mm_pages = int(mm_result.group(1))
    
   h3_custom_game_ids = []
   h3_mm_game_ids = []

   
   ###
   ### customs
   ###
   for i in range(1,custom_pages+1):
      
       #i = 3
       print("getting halo3 custom game id data for {} page {}/{}".format(gamertag,i,custom_pages))

        #request page data
       url = 'https://halo.bungie.net/stats/playerstatshalo3.aspx?player={}&cus=1&ctl00_mainContent_bnetpgl_recentgamesChangePage={}'.format(gamertag,i)
       page_data = requests.get(url)
       page_data_text = page_data.text
      
        #extract game ids from page
       game_ids = re.findall('gameid=(.*)&amp',page_data_text)
       h3_custom_game_ids = h3_custom_game_ids + game_ids
       
       time.sleep(2) # to not overload HBN with response calls
    
       print("done!")
       
   ###
   ### matchmaking
   ###
      
   for i in range(1,mm_pages+1):
     
      print("getting halo3 matchmaking game id data for {} page {}/{}".format(gamertag,i,mm_pages))

       #request page data
      url = 'https://halo.bungie.net/stats/playerstatshalo3.aspx?player={}&ctl00_mainContent_bnetpgl_recentgamesChangePage={}'.format(gamertag,i)
      page_data = requests.get(url)
      page_data_text = page_data.text
     
       #extract game ids from page
      game_ids = re.findall('gameid=(.*)&amp',page_data_text)
      h3_mm_game_ids = h3_mm_game_ids + game_ids
      
      time.sleep(2) # to not overload HBN with response calls
   
      print("done!")
      
   return h3_custom_game_ids + h3_mm_game_ids 
    
    
    
    
def halo3_campaign_ids(gamertag):
   """
   returns list of campaign game ids
   """
   

   camp_url = 'https://halo.bungie.net/stats/playercampaignstatshalo3.aspx?player={}'.format(gamertag)
   camp_data = requests.get(camp_url)
   camp_data_text = camp_data.text
   camp_result = re.search('\\\\"PageCount\\\\":(.*),\\\\"EditMode\\\\":', camp_data_text)
   camp_pages = int(camp_result.group(1))

   h3_camp_game_ids = []
         
   ###
   ### campaign
   ###
      
   for i in range(1,camp_pages+1):
     
      i = 1
      print("getting halo3 campaign game id data for {} page {}/{}".format(gamertag,i,camp_pages))

       #request page data
      url = 'https://halo.bungie.net/stats/playercampaignstatshalo3.aspx?player={}&ctl00_mainContent_bnetpgl_recentgamesChangePage={}'.format(gamertag,i)
      page_data = requests.get(url)
      page_data_text = page_data.text
     
       #extract game ids from page
      game_ids = re.findall('gameid=(.*)&amp',page_data_text)
      h3_camp_game_ids = h3_camp_game_ids + game_ids
      
      time.sleep(2) # to not overload HBN with response calls
   
      print("done!")
      
      

   return h3_camp_game_ids
    
    
    
    
    
    
    
    
    
def halo3_game_id_download(game_id, gamertag):
    """
    for each game id, hard download all the game data

    hard download because it's going away soon and its
    easier to experiment offline than to hit HBN with
    response calls every time
    """

    game = 'https://halo.bungie.net/Stats/GameStatsHalo3.aspx?gameid={}&player={}'.format(game_id, gamertag)
    game_data = requests.get(game)
    game_text = game_data.text
    
    save_path = ''
    name_of_file = '{}_halo3_game_{}.txt'.format(gamertag,game_id)
    complete_name = os.path.join(save_path, name_of_file)
    
    file = open(complete_name, "w")
    file.write(game_text)
    file.close
    
    time.sleep(2)
    
    
def halo3_campaign_id_download(game_id, gamertag):
    """
    separate function for campaign ids
    since the url path is different
    """

    game = 'https://halo.bungie.net/Stats/GameStatsCampaignHalo3.aspx?gameid={}&player={}'.format(game_id, gamertag)
    game_data = requests.get(game)
    game_text = game_data.text
    
    save_path = ''
    name_of_file = '{}_halo3_campaign_{}.txt'.format(gamertag,game_id)
    complete_name = os.path.join(save_path, name_of_file)
    
    file = open(complete_name, "w")
    file.write(game_text)
    file.close
    
    time.sleep(2)
    
    
    
    
    
def halo3_main_stats_page(gamertag):
    """
    download of the main halo 3 stats page
    """
    
    url = 'https://halo.bungie.net/stats/halo3/careerstats.aspx?player={}'.format(gamertag)
    url_data = requests.get(url)
    url_text = url_data.text
    
    save_path = ''
    name_of_file = '{}_halo3_profile_stats.txt'.format(gamertag)
    complete_name = os.path.join(save_path, name_of_file)
    
    file = open(complete_name, "w")
    file.write(url_text)
    file.close
    
    time.sleep(2)
    
    
    
    
    
def halo2_get_files(gamertag):
    halo2_game_ids_list = halo2_game_ids(gamertag) 
    j=1
    for i in halo2_game_ids_list:
        print("processing game id {}, {}/{} total games".format(i, j,len(halo2_game_ids_list)))
        halo2_game_id_download(i, gamertag)
        j=j+1
    
def halo3_get_files(gamertag):
    halo3_game_ids_list = halo3_game_ids(gamertag)
    j=1
    for i in halo3_game_ids_list:
        halo3_game_id_download(i, gamertag)
        print("processing game id {}, {}/{} total games".format(i, j,len(halo3_game_ids_list)))
        j=j+1
        
def halo3_get_campaign_files(gamertag):
    halo3_campaign_ids_list = halo3_campaign_ids(gamertag)
    j=1
    for i in halo3_campaign_ids_list:
        halo3_campaign_id_download(i, gamertag)
        print("processing campaign id {}, {}/{} total games".format(i, j,len(halo3_campaign_ids_list)))
        j=j+1
    
    
    
# halo2_get_files("AI52487963")
# halo3_get_files("AI52487963")
# halo3_get_campaign_files("AI52487963")
# halo3_main_stats_page("AI52487963")
    
    


###
### analytics coming soon!
###
    

"""
for each game's data, assemble the Carnage Report dataframe

timestamp, map, gametype, playlist, gamertag, rank?, place, score, kills, assists, deaths, etc
"""


