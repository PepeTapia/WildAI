import pandas as pd
import os

temp_red = [['0', '0', '0', '1170'], ['0', '0', '0', '1081'], ['0', '0', '0', '1220'], ['0', '0', '0', '1155'], ['0', '0', '0', '932']]
stats_header = ["time", "team","towers", "team_gold", "team_kills""top_kill", "top_death", "top_assist", "top_gold",
                "jungle_kill", "jungle_death", "jungle_assist", "jungle_gold",
                "mid_kill","mid_death", "mid_assist", "mid_gold",
                "bot_kill", "bot_death", "bot_assist", "bot_gold",
                "supp_kill", "supp_death", "supp_assist","supp_gold",]
stats_dict = {
            'time': None,
            'team': None,
            'towers': None,
            'team_gold': None,
            'team_kills': None,
            'top_kill': None,
            'top_death': None,
            'top_assist': None,
            'top_gold': None,
            'jungle_kill': None, 
            'jungle_death': None,
            'jungle_assist': None,
            'jungle_gold': None,
            'mid_kill': None,
            'mid_death': None,
            'mid_assist': None,
            'mid_gold': None,
            'bot_kill': None,
            'bot_death': None,
            'bot_assist': None,
            'bot_gold': None,
            'supp_kill': None,
            'supp_death': None,
            'supp_assist': None,
            'supp_gold': None
            }
#print(stats_dict)
time = 5
team = "Red"
towers = 1
team_gold = 32000
team_kills = 5

# temp_list = []
# temp_list.append(time)
# temp_list.append(team)
# for i in temp_red:
#     for x in i:
#         temp_list.append(x)
# temp_list.append(towers)
# temp_list.append(team_gold)
# temp_list.append(team_kills)
stats_dict['time'] = time
stats_dict['team'] = "red"
stats_dict['towers'] = towers
stats_dict['team_gold'] = team_gold
stats_dict['team_kills'] = team_kills
red_list = [x for xs in temp_red for x in xs]
#print(red_list)
if stats_dict.get('supp_assist') == None:
    print('it has none')
# for x, y in enumerate(stats_dict.items()):
#     print(x)
#     #print(y)
#     #print(iter-1)
#     stats_dict[y[x]] = red_list[x]



print(stats_dict)
#final_dict = {}
#for x, stat in enumerate(stats_header):
    #final_dict[stat] = temp_list[x]
#df = pd.DataFrame(final_dict,index=[time])
#print(df)
#game_num = 1
#base = os.getcwd()
#title = input("""Enter folder title. Format should be similar to 'Team A vs Team B Series (Play-in/Group/Knockout)  """)
#os.makedirs(f'WildAI\Datasets\{title}',exist_ok=True)
#output_csv = os.path.join(base, f'WildAI\Datasets\{title}\Game{game_num}.csv')
#df.to_csv(output_csv,mode='a',index=False,header=False)
#print(os.getcwd())
#print(df)

#def game_start_csv(blue_team, red_team, game_number):
    