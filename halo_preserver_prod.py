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
import pandas as pd


heatmap_data = {'name': ['assembly','avalanche','blackout','citadel','cold_storage','construct','epitaph','foundry','ghost_town','guardian','heretic','high_ground','isolation','last_resort','longshore','narrows','orbital','rats_nest','sandbox','sandtrap','snowbound','standoff','the_pit','valhalla','kills_all','kills_assault_rifle','kills_ball','kills_banshee','kills_battle_rifle','kills_beam_rifle','kills_bomb','kills_brute_shot','kills_carbine','kills_chopper','kills_environment','kills_elephant_turret','kills_energy_sword','kills_falling','kills_firebomb_grenade','kills_flag','kills_flamethrower','kills_fragmentation_grenade','kills_fuel_rod_gun','kills_ghost','kills_gravity_hammer','kills_guardians','kills_hornet','kills_mauler','kills_melee','kills_missile_pod','kills_Mongoose','kills_Needler','kills_Pistol','kills_Plasma_Grenade','kills_Plasma_Rifle','kills_Plasma_Pistol','kills_Plasma_Turret','kills_Prowler','kills_Rocket_Launcher','kills_Scorpion_-_Driver','kills_Scorpion_-_Gunner','kills_Sentinel_Beam','kills_Shotgun','kills_SMG','kills_Sniper_Rifle','kills_Spartan_Laser','kills_Spike_Grenade','kills_Spike_Rifle','kills_Tripmine','kills_Turret_Gun','kills_Warthog_-_Driver','kills_Warthog_-_Gunner','kills_Warthog_-_Gunner_Gauss','kills_Wraith_-_Driver','kills_Wraith_-_Gunner','deaths_all','deaths_assault_rifle','deaths_ball','deaths_banshee','deaths_battle_rifle','deaths_beam_rifle','deaths_bomb','deaths_brute_shot','deaths_carbine','deaths_chopper','deaths_environment','deaths_elephant_turret','deaths_energy_sword','deaths_falling','deaths_firebomb_grenade','deaths_flag','deaths_flamethrower','deaths_fragmentation_grenade','deaths_fuel_rod_gun','deaths_ghost','deaths_gravity_hammer','deaths_guardians','deaths_hornet','deaths_mauler','deaths_melee','deaths_missile_pod','deaths_Mongoose','deaths_Needler','deaths_Pistol','deaths_Plasma_Grenade','deaths_Plasma_Rifle','deaths_Plasma_Pistol','deaths_Plasma_Turret','deaths_Prowler','deaths_Rocket_Launcher','deaths_Scorpion_-_Driver','deaths_Scorpion_-_Gunner','deaths_Sentinel_Beam','deaths_Shotgun','deaths_SMG','deaths_Sniper_Rifle','deaths_Spartan_Laser','deaths_Spike_Grenade','deaths_Spike_Rifle','deaths_Tripmine','deaths_Turret_Gun','deaths_Warthog_-_Driver','deaths_Warthog_-_Gunner','deaths_Warthog_-_Gunner_Gauss','deaths_Wraith_-_Driver','deaths_Wraith_-_Gunner'],
                
            'id': ['490','470','520','740','600','300','350','480','590','320','720','310','330','30','440','380','500','580','730','400','360','410','390','340','127','16','34','39','11','15','32','22','12','52','2','60','25','1','30','31','23','27','18','730','26','0','53','8','3','19','41','7','5','28','10','6','38','55','20','42','43','56','13','9','14','21','29','17','59','35','46','47','48','49','50','255','144','162','167','139','143','160','150','140','180','130','188','153','129','158','159','151','155','146','858','154','128','181','136','131','147','169','135','133','156','138','134','166','183','148','170','171','184','141','137','142','149','157','145','187','163','174','175','176','177','178'],
           
            'type': ['map','map','map','map','map','map','map','map','map','map','map','map','map','map','map','map','map','map','map','map','map','map','map','map','kill','kill','kill','kill','kill','kill','kill','kill','kill','kill','kill','kill','kill','kill','kill','kill','kill','kill','kill','kill','kill','kill','kill','kill','kill','kill','kill','kill','kill','kill','kill','kill','kill','kill','kill','kill','kill','kill','kill','kill','kill','kill','kill','kill','kill','kill','kill','kill','kill','kill','kill','death','death','death','death','death','death','death','death','death','death','death','death','death','death','death','death','death','death','death','death','death','death','death','death','death','death','death','death','death','death','death','death','death','death','death','death','death','death','death','death','death','death','death','death','death','death','death','death','death','death','death'] }

heatmap_df = pd.DataFrame.from_dict(heatmap_data)


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
    
def halo3_get_heatmap_images(gamertag, inf=10, kills=True, individual_weapons=False, map_to_get='all'):
    #gamertag = 'AI52487963'
    #inf = 10
    #kills=True        
    #individual_weapons=True
    
    if map_to_get=='all':
        map_data = heatmap_df[heatmap_df['type']=='map']
    else:
        map_data = heatmap_df[heatmap_df['name']==map_to_get]
        
   
    if kills==True and individual_weapons==False: # kills, all weapons
        type_data = heatmap_df[heatmap_df['name']=='kills_all']
    elif kills==True and individual_weapons==True: # kills, individual weapons
        type_data = heatmap_df[heatmap_df['type']=='kill']
    elif kills==False and individual_weapons==False: # deaths, all weapons
        type_data = heatmap_df[heatmap_df['name']=='deaths_all']
    elif kills==False and individual_weapons==True: # deaths, individual weapons
        type_data = heatmap_df[heatmap_df['type']=='death']

    
    for i in range(0,map_data.shape[0]):
        for j in range(0,type_data.shape[0]):
                        
            map_id = map_data['id'].iloc[i]
            map_name = map_data['name'].iloc[i]
            
            type_id = type_data['id'].iloc[j]
            type_name = type_data['name'].iloc[j]
    
            response = requests.get("https://halo.bungie.net/stats/Halo3/HeatMap.ashx?player={}&map={}&wep={}&inf={}".format(gamertag,map_id,type_id,inf))
    
            save_path = ''
            name_of_file = '{}_halo3_heatmap_{}_{}_{}.png'.format(gamertag,map_name,type_name,inf)
            print("saving {}".format(name_of_file))
            complete_name = os.path.join(save_path, name_of_file)
            file = open(complete_name,"wb")
            file.write(response.content)
            file.close()
    
            time.sleep(2)
    
    
    
    
   
def reach_write(url, filename):
    response = requests.get(url)
    save_path = ''
    name_of_file = filename
    print("saving {}".format(filename))
    complete_name = os.path.join(save_path, name_of_file)
    file = open(complete_name,"wb")
    file.write(response.content)
    file.close
    
    time.sleep(2)
            
def reach_career_stats(gamertag):
    """
    gets the main stats pages for each permutation of stat type and drilldown.
    note: playlist and enemies only have 2-3 drilldowns, so their downloaded
    data might be empty or otherwise useless. in the interest of dev time im
    keeping those permuatations in here...
    """
    
    career_stats_list = ['default', 'playlists', 'maps', 'medals', 'weapons', 'enemies']
    drilldown = ['invasion', 'arena', 'competitive', 'campaign', 'firefight', 'custom']
    
    for i in career_stats_list:
        for j in range(1,7):
            url = "https://halo.bungie.net/stats/reach/careerstats/{}.aspx?player={}&vc={}".format(i,gamertag,j)
            filename = '{}_reach_career_stats_{}_{}.txt'.format(gamertag, i, drilldown[j-1])
            reach_write(url, filename)
         
            
            
           
        
            
def reach_overview(gamertag):
    """
    gets overview and commendations
    """
    overview_url = 'https://halo.bungie.net/Stats/Reach/default.aspx?player={}'.format(gamertag)
    overview_filename = '{}_reach_service_record_overview.txt'.format(gamertag)
    reach_write(overview_url, overview_filename)
    
    comm_url = 'https://halo.bungie.net/Stats/Reach/Commendations.aspx?player={}'.format(gamertag)
    comm_filename = '{}_reach_service_record_commendations.txt'.format(gamertag)
    reach_write(comm_url,comm_filename)
    
    
        
    
def reach_game_ids(gamertag):
    """
    iterates through game history RSS 
    and generates list of unique game ids
    """
    
    #25 game ids per page
    # href="/stats/reach/gamestats.aspx?gameid=775177128&amp;player=Naded"></a>
    # https://halo.bungie.net/Stats/Reach/GameStats.aspx?gameid=873296322&player=Naded
    
    gamertag = 'naded'
    game_ids_list = []
    
    num_before = 0
    num_after = 1
    
    i=0
    while num_before != num_after:
        # i = 25
        
        # gamertag= 'naded'
        
        print("getting reach game id data for {} page {}".format(gamertag,i))
        num_before = len(game_ids_list)
        url = 'https://halo.bungie.net/stats/reach/rssgamehistory.ashx?vc=0&player={}&page={}'.format(gamertag,i)
    
        page_data = requests.get(url)
        page_data_text = page_data.text
        game_ids = re.findall('gameid=(.*)&amp',page_data_text)
        game_ids_fix = list(set([i[0:9] for i in game_ids]))
        
        game_ids_list = list(set(game_ids_list + game_ids_fix))
        num_after = len(game_ids_list)
        time.sleep(2)
        i = i+1
        print("done! {} total game ids collected so far".format(num_after))
        
    return game_ids_list
    
    

def reach_game_id_download(game_id,gamertag):
    
    reach_url = 'https://halo.bungie.net/Stats/Reach/GameStats.aspx?gameid={}&player={}'.format(game_id,gamertag)
    filename = '{}_reach_game_{}.txt'.format(gamertag,game_id)
    reach_write(reach_url,filename)
    time.sleep(2)
    
    

def reach_get_files(gamertag):
    reach_game_ids_list = reach_game_ids(gamertag)
    
    j=1
    for i in reach_game_ids_list:
        print("processing reach game id {}, {}/{} total games".format(i,j,len(reach_game_ids_list)))
        reach_game_id_download(i,gamertag)
        j=j+1
    
    
  
    
       
    
    
 
# halo2_get_files("AI52487963")
# halo3_get_files("AI52487963")
# halo3_get_campaign_files("AI52487963")
# halo3_main_stats_page("AI52487963")
# halo3_get_heatmap_images("AI52489763") # all kills, all maps
# halo3_get_heatmap_images("AI52487963", inf=1, kills=False, individual_weapons=True,map_to_get="the_pit")
# reach_career_stats("AI52487963")
# reach_overview("AI52487963")
# reach_get_files("AI52487963")
    


###
### analytics coming soon!
###
    

"""
for each game's data, assemble the Carnage Report dataframe

timestamp, map, gametype, playlist, gamertag, rank?, place, score, kills, assists, deaths, etc
"""


