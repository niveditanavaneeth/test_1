import requests
from bs4 import BeautifulSoup 
import os
import json
from datetime import datetime

# import requests, bs4

def dict_null_check( object, key):
    if key in object:
        return 1
    else:
        return 0


main_url = 'https://www.cricbuzz.com/cricket-series/2750/ranji-trophy-2018-19/matches'
main_request = requests.get(main_url)
main_soup = BeautifulSoup(main_request.text, 'lxml')

# print main_soup

url_division = main_soup.find_all(class_="text-hvr-underline")
print "urls_length"
print (len(url_division))
i = 0
url_all = []
for div in url_division:
    if div['href'] :
        url = div['href']
        if "/cricket-scores" in url:
            print (url) 
            url_all.append(url.replace('/cricket-scores','https://www.cricbuzz.com/live-cricket-scorecard'))

# print url_all 
all_matches = []

for i,url_i in enumerate(url_all):
# for url_i in range(1):
    print i
    print url_i    
    # url = 'https://www.cricbuzz.com/live-cricket-scorecard/20884/saur-vs-cg-round-1-elite-group-a-ranji-trophy-2018-19'
    url = url_i

    r = requests.get(url)

    # if r.status_code != 200:
    #     raise DownloadError("oops, could not grab the page", r)

    soup = BeautifulSoup(r.text, 'lxml')
    detailsObject = {}


    match_header = soup.find(class_='cb-nav-hdr cb-font-18 line-ht24').text.split(',') 
    team_list = match_header[0].split('vs')
    teams = {
            'team1' : team_list[0].strip(),
            'team2' : team_list[1].strip()
    }


    index_innings = 1
    # innings_data = []
    Ranji2018 = {}

    for innings_id in range(5):
        # inningsPlayers = inningsid.find_all(class_="cb-col cb-col-100 cb-scrd-itms")    
        # print inningsPlayers
        # index_innings += 1
        innings_id = soup.find(id = "innings_"+str(index_innings))
        if innings_id != None:
            innings_players = innings_id.find_all(class_="cb-col cb-col-100 cb-scrd-itms")
            # print (inningsPlayers)
            batScoreCard = {}
            bowlScoreCard = {}
            extras = {}
            total = {}
            index_bat = 1
            index_bowl = 1

            innings_batting_team = innings_id.find(class_='cb-col cb-col-100 cb-scrd-hdr-rw').text.strip(' ').split(' ') 
            innings_bowling_team = (teams['team1'] if teams['team1'] != innings_batting_team[0] else teams['team2'])

            for div in innings_players:
                tempvar = []
                for div1 in div.find_all('div'):
                    tempvar.append(div1.text)
                # print tempvar
                if len(tempvar) == 7:
                    batScoreCard['player'+ str(index_bat)] = tempvar
                    index_bat +=1
                elif len(tempvar) == 8:
                    bowlScoreCard['player'+ str(index_bowl)] = tempvar
                    index_bowl +=1
                else:
                    if tempvar[0] == "Extras":
                        tempvar[2] = tempvar[2].replace('(',' ')
                        tempvar[2] = tempvar[2].replace(')',' ')
                        x = tempvar[2].split(',')
                        extras = {
                            'wide' : x[2].strip().split(' ')[1] ,
                            'nb' : x[3].strip().split(' ')[1],
                            'lb' : x[1].strip().split(' ')[1],
                            'b' : x[0].strip().split(' ')[1],
                            'p' : x[4].strip().split(' ')[1]
                        }
                    if tempvar[0] == "Total":
                        # print tempvar
                        tempvar[2] = tempvar[2].replace('(',' ')
                        tempvar[2] = tempvar[2].replace(')',' ')
                        x = tempvar[2].split(',') 
                        total = {
                            'runs' : tempvar[1].strip(),
                            'overs': x[1].strip().split(' ')[0],
                            'wickets' : x[0].strip().split(' ')[0]
                        }
        
            fall_of_wicket = innings_id.find(class_='cb-col cb-col-100 cb-col-rt cb-font-13')
            fall_of_wicketlist = []
            if fall_of_wicket != None:
                fall_of_wicketlist = (x.text for x in fall_of_wicket.find_all('span'))
            # fallOfWicket = fallOfWicket.replace('(','') 
            # fallOfWicket = fallOfWicket.replace(')','')

            fall_of_wickets = {}
            index_wicket = 1
            for x in fall_of_wicketlist:
                x = x.split('-', 1)
                # over = x[1].replace(')','').split(',')
                overNo = x[1].replace(')','').split(',')[1].strip()
                calcBall = list(int(x) for x in overNo.split('.'))
                ball = ((calcBall[0] * 6 + calcBall[1]) if len(calcBall) > 1 else calcBall[0]*6 )
                # ball = 'yes' if len(calcBall) > 1 else 'no'
                fall_of_wickets['player' + str(index_wicket)] = {
                    'teamScore' : x[0],
                    'ballNo' : ball
                }
                index_wicket += 1


            inning = {
                    "batTeam": innings_batting_team[0],
                    "batScoreCard": batScoreCard,
                    "FallOfWickets": fall_of_wickets,
                    "bowlTeam": innings_bowling_team,
                    "bowlScoreCard": bowlScoreCard,
                    "extras": extras,
                    "total": total
                }
            # innings_data.append(inning)
            Ranji2018["innings" + str(index_innings)] = inning
            index_innings += 1
        else:
            match_status = soup.find(class_="cb-scrcrd-status").text
            # print (matchStatus)
            # print "ok"
            break
        
    # print batScoreCard
    # print json.dumps(Ranji2018, indent= 2, sort_keys = True)


    #  MATCH DETAILS

    match_details = soup.find(class_="cb-col cb-col-100 cb-font-13") 

    details = {}

    main_detail = {}
    squad_detail = []
    for div in match_details.find_all(class_="cb-mtch-info-itm"):
        details_key = div.find(class_= "cb-col cb-col-27").text
        details_value = div.find(class_= "cb-col cb-col-73").text
        main_detail[details_key.strip().lower()] = details_value.strip()


    for div in match_details.find_all(class_="cb-minfo-tm-nm"): 
        squad_detail.append(div.text.replace('Playing  ','').replace('Bench  ',''))
    # print json.dumps(main_detail , indent=2, sort_keys= True)
    
    toss = {}
    if dict_null_check(main_detail,"toss"):    
        tossdetails = main_detail["toss"].split(' ')
        toss = {'winner' : tossdetails[0].strip() ,'decision' : tossdetails[7].strip()}
    # print toss

    date = {}
    date1 = []
    for i,div in enumerate(match_details.find_all(class_="schedule-date")): 
        # date1 = datetime.utcfromtimestamp(int(div.attrs['timestamp']))
        # date1 = datetime.strptime(div.attrs['timestamp'], ' %d %b %Y')
        date_1 = datetime.fromtimestamp(float(div.attrs['timestamp'])/1000.0).isoformat()
        date1.append(date_1)

    date = {'startDate' : date1[0],
            'endDate': date1[1]}
    # print date
    umpire_list = []
    # if "umpires" in main_detail:
    #     print main_detail["umpires"]
    #     umpirelist = main_detail["umpires"].split(',')
    umpire = {"umpire1": "",
            "umpire2": "",
            "thirdUmpire": ""
        }
    if dict_null_check(main_detail, "umpire"):
        umpire_list = main_detail["umpires"].split(',')
        umpire = {'umpire1': umpire_list[0].strip() if umpire_list[0] else '',
            'umpire2': umpire_list[1].strip() if umpire_list[1] else '',}
    # umpirelist.append(main_detail["match referee"])
    
    if dict_null_check(main_detail, "match referee"):
        umpire = {'thirdUmpire': main_detail["match referee"]}
    # print umpire

    roundNo = ''
    groupName = ''


    squad = {}
    squad['team1'] = { "teamName": squad_detail[0],
                "playing11": squad_detail[1].split(',') ,
                "bench": squad_detail[2].split(',')  if len(squad_detail) == 6 else ''
                } 
    # print details            
    squad['team2'] = { "teamName": squad_detail[3] if len(squad_detail) == 6 else squad_detail[2],
                "playing11": squad_detail[4].split(',') if len(squad_detail) == 6 else squad_detail[3].split(','),
                "bench": squad_detail[5].split(',') if len(squad_detail) == 6 else ''
                } 
    # print squad

    matchInfo = {
            "matchType": "Ranji Test Match",
            "teams": teams,
            "toss": toss,
            "venue": main_detail["venue"],
            "date": date,
            "umpire": umpire,
            "roundNo": match_header[1].strip(),
            "groupName": match_header[2].split('-')[0].strip(),
            "squad": squad
        }

    # print json.dumps(matchInfo, indent=2, sort_keys= True)
    Ranji2018["matchInfo" ] = matchInfo
    all_matches.append(Ranji2018)
    finalObject = { "Ranji2018" : [Ranji2018]}
    file_name = "Ranji2018" + '-' + matchInfo["groupName"].replace(' ', '') + '-' +  matchInfo["roundNo"].replace(' ', '') + '-' + teams["team1"].replace(' ', '') + "vs" + teams["team2"].replace(' ', '') + ".json"
    print file_name
    with open(file_name, 'w') as json_file:
        json.dump(finalObject, json_file, indent=4, sort_keys= True)

finalObject = { "Ranji2018" : [Ranji2018]} 

print json.dumps(finalObject,indent = 2,sort_keys=True)
    
# with open('RanjiStructure.json', 'w') as json_file:
#     json.dump(finalObject, json_file, indent=4, sort_keys= True)




# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    # for div in matchDetails.find_all(class_="cb-col cb-col-27"):
    #     # print ('\n')
    #     # print div.text
    #     details_key.append(div.text)
    # for div in matchDetails.find_all(class_="cb-col cb-col-73"):
    #     # print ('\n')
    #     # print div.text    
    #     details_value.append(div.text)
    # # print details
    # for i in range(len(details_key)):
    #     details[details_key[i]] = details_value[i]
    # teamdetails = details[0].split(',')
    # teams = teamdetails[0].strip().split('vs')
    # matchinfo = {}
    # matchinfo['teams'] = {'team1' : teams[0].strip(), 'team2' : teams[1].strip() }
    # print matchinfo








 # findaa = list(i for i in soup.findAll(class_ = "ng-scope"))
    # find_a = soup.find_all(class_ = "ng-scope")
    # find_aa = soup.find(class_="cb-col cb-col-67 cb-scrd-lft-col html-refresh ng-isolate-scope")
    # find_urll = soup.find(url="/api/html/cricket-scorecard/20881")
    # print "find_a : "
    # print find_a
    # print find_aa
    # print find_urll

# url = "https://www.cricbuzz.com/live-cricket-scorecard/20900/raj-vs-jk-round-1-elite-group-c-ranji-trophy-2018-19"
# r = requests.get(url)

#     # if r.status_code != 200:
#     #     raise DownloadError("oops, could not grab the page", r)

# soup = BeautifulSoup(r.text, 'lxml')
# detailsObject = {}

#     # findaa = list(i for i in soup.findAll(class_ = "ng-scope"))
#     # find_a = soup.find_all(class_ = "ng-scope")
#     # find_aa = soup.find(class_="cb-col cb-col-67 cb-scrd-lft-col html-refresh ng-isolate-scope")
#     # find_urll = soup.find(url="/api/html/cricket-scorecard/20881")
#     # print "find_a : "
#     # print find_a
#     # print find_aa
#     # print find_urll

# matchHeader = soup.find(class_='cb-nav-hdr cb-font-18 line-ht24').text.split(',') 
# teamList = matchHeader[0].split('vs')
# teams = {
#         'team1' : teamList[0].strip(),
#         'team2' : teamList[1].strip()
# }


# index_innings = 1
# innings_data = []
# Ranji2018 = {}
# for inningsid in range(5):
#     # print inningsid
#     #     print '\n' 
#     # inningsPlayers = inningsid.find_all(class_="cb-col cb-col-100 cb-scrd-itms")    
#     # print inningsPlayers
#     # index_innings += 1
#     inningsid = soup.find(id = "innings_"+str(index_innings))
#     if inningsid != None:
#         # print 'hey'
#         inningsPlayers = inningsid.find_all(class_="cb-col cb-col-100 cb-scrd-itms")
#         inningsBattingTeam = inningsid.find(class_='cb-col cb-col-100 cb-scrd-hdr-rw').text.strip(' ').split(' ') 
#         batScoreCard = {}
#         bowlScoreCard = {}
#         extras = {}
#         total = {}
#         index_bat = 1
#         index_bowl = 1
#         for div in inningsPlayers:
#             tempvar = []
#             for div1 in div.find_all('div'):
#                 tempvar.append(div1.text)
#             # print tempvar
#             if len(tempvar) == 7:
#                 batScoreCard['player'+ str(index_bat)] = tempvar
#                 index_bat +=1
#             elif len(tempvar) == 8:
#                 bowlScoreCard['player'+ str(index_bowl)] = tempvar
#                 index_bowl +=1
#             else:
#                 if tempvar[0] == "Extras":
#                     tempvar[2] = tempvar[2].replace('(',' ')
#                     tempvar[2] = tempvar[2].replace(')',' ')
#                     # print tempvar[2]
#                     x = tempvar[2].split(',')
#                     # print x
#                     extras = {
#                         'wide' : x[2].strip().split(' ')[1] ,
#                         'nb' : x[3].strip().split(' ')[1],
#                         'lb' : x[1].strip().split(' ')[1],
#                         'b' : x[0].strip().split(' ')[1],
#                         'p' : x[4].strip().split(' ')[1]
#                     }
#                 if tempvar[0] == "Total":
#                     # print tempvar
#                     tempvar[2] = tempvar[2].replace('(',' ')
#                     tempvar[2] = tempvar[2].replace(')',' ')
#                     x = tempvar[2].split(',') 
#                     total = {
#                         'runs' : tempvar[1].strip(),
#                         'overs': x[1].strip().split(' ')[0],
#                         'wickets' : x[0].strip().split(' ')[0]
#                     }
    
#         fallOfWicket = inningsid.find(class_='cb-col cb-col-100 cb-col-rt cb-font-13')
#         fallOfWicketList = []
#         if fallOfWicket != None:
#             fallOfWicketList = (x.text for x in fallOfWicket.find_all('span'))
#         # fallOfWicket = fallOfWicket.replace('(','') 
#         # fallOfWicket = fallOfWicket.replace(')','')
#         # print list(fallOfWicketList)

#         FallOfWickets = {}
#         index_wicket = 1
#         for x in fallOfWicketList:
#             x = x.split('-', 1)
#             # over = x[1].replace(')','').split(',')
#             print "fall of wicket loop"
#             print x
#             print (x[1].replace(')','').split(',')[1].strip())
#             overNo = x[1].replace(')','').split(',')[1].strip()
#             calcBall = list(int(x) for x in overNo.split('.'))
#             ball = ((calcBall[0] * 6 + calcBall[1]) if len(calcBall) > 1 else calcBall[0]*6 )
#             # ball = 'yes' if len(calcBall) > 1 else 'no'
#             FallOfWickets['player' + str(index_wicket)] = {
#                 'teamScore' : x[0],
#                 'ballNo' : ball
#             }
#             index_wicket += 1


#         inningsBowlingTeam = (teams['team1'] if teams['team1'] != inningsBattingTeam[0] else teams['team2'])

#         inning = {
#                 "batTeam": inningsBattingTeam[0],
#                 "batScoreCard": batScoreCard,
#                 "FallOfWickets": FallOfWickets,
#                 "bowlTeam": inningsBowlingTeam,
#                 "bowlScoreCard": bowlScoreCard,
#                 "extras": extras,
#                 "total": total
#             }
#         # innings_data.append(inning)
#         Ranji2018["innings" + str(index_innings)] = inning
#     index_innings += 1
# # print batScoreCard
# # print json.dumps(Ranji2018, indent= 2, sort_keys = True)


# #  MATCH DETAILS

# matchDetails = soup.find(class_="cb-col cb-col-100 cb-font-13") 

# details = []
# for div in matchDetails.find_all(class_="cb-col cb-col-73"):
#     # print ('\n')
#     # print div
#     details.append(div.text)
    
# # print details

# # teamdetails = details[0].split(',')
# # teams = teamdetails[0].strip().split('vs')
# # matchinfo = {}
# # matchinfo['teams'] = {'team1' : teams[0].strip(), 'team2' : teams[1].strip() }
# # print matchinfo

# tossdetails = details[2].split(' ')
# toss = {}
# toss = {'winner' : tossdetails[0].strip() ,'decision' : tossdetails[7].strip()}
# # print toss

# date = {}
# date1 = []
# for i,div in enumerate(matchDetails.find_all(class_="schedule-date")): 
#     # date1 = datetime.utcfromtimestamp(int(div.attrs['timestamp']))
#     # date1 = datetime.strptime(div.attrs['timestamp'], ' %d %b %Y')
#     date_1 = datetime.fromtimestamp(float(div.attrs['timestamp'])/1000.0).isoformat()
#     date1.append(date_1)

# date = {'startDate' : date1[0],
#         'endDate': date1[1]}
# # print date

# umpirelist = details[5].split(',')
# umpirelist.append(details[6])
# umpire = {}
# umpire = {'umpire1':umpirelist[0].strip(),
#         'umpire2': umpirelist[1].strip(),
#         'thirdUmpire': umpirelist[2].strip()}
# # print umpire

# roundNo = ''
# groupName = ''


# squad = {}
# squad['team1'] = { "teamName": "",
#             "playing11": details[7].split(','),
#             "bench": details[8].split(',')
#             } 
# squad['team2'] = { "teamName": "",
#             "playing11": details[9].split(','),
#             "bench": details[10].split(',')
#             } 
# # print squad

# matchInfo = {
#         "matchType": "Ranji Test Match",
#         "teams": teams,
#         "toss": toss,
#         "venue": details[4],
#         "date": date,
#         "umpire": umpire,
#         "roundNo": matchHeader[1].strip(),
#         "groupName": matchHeader[2].split('-')[0].strip(),
#         "squad": squad
#     }


# Ranji2018["matchInfo" ] = matchInfo

# finalObject = { "Ranji2018" : [Ranji2018]}

# print json.dumps(finalObject,indent = 2,sort_keys=True)

    # with open('RanjiStructure.json', 'w') as json_file:
    #   json.dump(finalObject, json_file, indent=4, sort_keys= True)


# finalObject


# -----------------------------------------------------------------------------------------------------







# innings10id = soup.find(id = "innings_1")
# innings11id = soup.find(id = "innings_2") 
# innings20id = soup.find(id = "innings_3")
# innings21id = soup.find(id = "innings_4")

# innings10Players = innings10id.find_all(class_="cb-col cb-col-100 cb-scrd-itms")
# innings11Players = innings11id.find_all(class_="cb-col cb-col-100 cb-scrd-itms")
# innings20Players = innings20id.find_all(class_="cb-col cb-col-100 cb-scrd-itms")
# innings21Players = innings21id.find_all(class_="cb-col cb-col-100 cb-scrd-itms")

# # print innings10Players

# # teamBat = innings10id.find(class_="cb-col cb-col-100 cb-scrd-hdr-rw")
# # print teamBat.text


# # INNINGS 10

# innings10BattingTeam = innings10id.find(class_='cb-col cb-col-100 cb-scrd-hdr-rw').text.strip(' ').split(' ') 

# batScoreCard = {}
# bowlScoreCard = {}
# extras = {}
# total = {}
# index_bat = 1
# index_bowl = 1
# for div in innings10Players:
#     tempvar = []
#     for div1 in div.find_all('div'):
#         tempvar.append(div1.text)
#     # print tempvar
#     if len(tempvar) == 7:
#         batScoreCard['player'+ str(index_bat)] = tempvar
#         index_bat +=1
#     elif len(tempvar) == 8:
#         bowlScoreCard['player'+ str(index_bowl)] = tempvar
#         index_bowl +=1
#     else:
#         if tempvar[0] == "Extras":
#             tempvar[2] = tempvar[2].replace('(',' ')
#             tempvar[2] = tempvar[2].replace(')',' ')
#             # print tempvar[2]
#             x = tempvar[2].split(',')
#             # print x
#             extras = {
#                 'wide' : x[2].strip().split(' ')[1] ,
#                 'nb' : x[3].strip().split(' ')[1],
#                 'lb' : x[1].strip().split(' ')[1],
#                 'b' : x[0].strip().split(' ')[1],
#                 'p' : x[4].strip().split(' ')[1]
#             }
#         if tempvar[0] == "Total":
#             # print tempvar
#             tempvar[2] = tempvar[2].replace('(',' ')
#             tempvar[2] = tempvar[2].replace(')',' ')
#             x = tempvar[2].split(',') 
#             total = {
#                 'runs' : tempvar[1].strip(),
#                 'overs': x[1].strip().split(' ')[0],
#                 'wickets' : x[0].strip().split(' ')[0]
#             }

# # print batScoreCard

# fallOfWicket = innings10id.find(class_='cb-col cb-col-100 cb-col-rt cb-font-13')
# fallOfWicketList = []
# fallOfWicketList = (x.text for x in fallOfWicket.find_all('span'))
# # fallOfWicket = fallOfWicket.replace('(','') 
# # fallOfWicket = fallOfWicket.replace(')','')
# # print list(fallOfWicketList)

# FallOfWickets = {}
# index_wicket = 1
# for x in fallOfWicketList:
#     x = x.split('-')
#     # over = x[1].replace(')','').split(',')
#     # print x
#     overNo = x[1].replace(')','').split(',')[1].strip()
#     calcBall = list(int(x) for x in overNo.split('.'))
#     ball = ((calcBall[0] * 6 + calcBall[1]) if len(calcBall) > 1 else calcBall[0]*6 )
#     # ball = 'yes' if len(calcBall) > 1 else 'no'
#     FallOfWickets['player' + str(index_wicket)] = {
#         'teamScore' : x[0],
#         'ballNo' : ball
#     }
#     index_wicket += 1


# innings10BowlingTeam = (teams['team1'] if teams['team1'] != innings10BattingTeam[0] else teams['team2'])

# innings10 = {
#         "batTeam": innings10BattingTeam[0],
#         "batScoreCard": batScoreCard,
#         "FallOfWickets": FallOfWickets,
#         "bowlTeam": innings10BowlingTeam,
#         "bowlScoreCard": bowlScoreCard,
#         "extras": extras,
#         "total": total
#     }

# # print '\n INNINGS 1 Bar \n'
# # print innings10

# #  INNINGS 11

# innings11BattingTeam = innings11id.find(class_='cb-col cb-col-100 cb-scrd-hdr-rw').text.strip(' ').split(' ') 

# batScoreCard11 = {}
# bowlScoreCard11 = {}
# extras11 = {}
# total11 = {}
# index_bat = 1
# index_bowl = 1
# for div in innings11Players:
#     tempvar = []
#     for div1 in div.find_all('div'):
#         tempvar.append(div1.text.strip())
#     # print tempvar
#     if len(tempvar) == 7:
#         batScoreCard11['player'+ str(index_bat)] = tempvar
#         index_bat +=1
#     elif len(tempvar) == 8:
#         bowlScoreCard11['player'+ str(index_bowl)] = tempvar
#         index_bowl +=1
#     else:
#         if tempvar[0] == "Extras":
#             tempvar[2] = tempvar[2].replace('(',' ')
#             tempvar[2] = tempvar[2].replace(')',' ')
#             x = tempvar[2].split(',')
#             # print x
#             extras11 = {
#                 'wide' : x[2].strip().split(' ')[1] ,
#                 'nb' : x[3].strip().split(' ')[1],
#                 'lb' : x[1].strip().split(' ')[1],
#                 'b' : x[0].strip().split(' ')[1],
#                 'p' : x[4].strip().split(' ')[1]
#             }
#         if tempvar[0] == "Total":
#             tempvar[2] = tempvar[2].replace('(',' ')
#             tempvar[2] = tempvar[2].replace(')',' ')
#             x = tempvar[2].split(',') 
#             total11 = {
#                 'runs' : tempvar[1].strip(),
#                 'overs': x[1].strip().split(' ')[0],
#                 'wickets' : x[0].strip().split(' ')[0]
#             }

# fallOfWicket = innings11id.find(class_='cb-col cb-col-100 cb-col-rt cb-font-13')
# fallOfWicketList = []
# fallOfWicketList = (x.text for x in fallOfWicket.find_all('span'))
# # fallOfWicket = fallOfWicket.replace('(','') 
# # fallOfWicket = fallOfWicket.replace(')','')
# # print list(fallOfWicketList)

# FallOfWickets11 = {}
# index_wicket = 1
# for x in fallOfWicketList:
#     x = x.split('-')
#     # print x
#     overNo = x[1].replace(')','').split(',')[1].strip()
#     calcBall = list(int(x) for x in overNo.split('.'))
#     ball = ((calcBall[0] * 6 + calcBall[1]) if len(calcBall) > 1 else calcBall[0]*6 )
#     # ball = 'yes' if len(calcBall) > 1 else 'no'
#     FallOfWickets11['player' + str(index_wicket)] = {
#         'teamScore' : x[0],
#         'ballNo' : ball
#     }
#     index_wicket += 1


# innings11BowlingTeam = (teams['team1'] if teams['team1'] != innings11BattingTeam[0] else teams['team2'])

# innings11 = {
#         "batTeam": innings11BattingTeam[0],
#         "batScoreCard": batScoreCard11,
#         "FallOfWickets": FallOfWickets11,
#         "bowlTeam": innings11BowlingTeam,
#         "bowlScoreCard": bowlScoreCard11,
#         "extras": extras11,
#         "total": total11
#     }

# # print '\n INNINGS 1 Guj \n'
# # print innings11

# # for div in innings11Players:
#     # print div.text

# #  INNINGS 20

# innings20BattingTeam = innings20id.find(class_='cb-col cb-col-100 cb-scrd-hdr-rw').text.strip(' ').split(' ') 

# batScoreCard20 = {}
# bowlScoreCard20 = {}
# extras20 = {}
# total20 = {}
# index_bat = 1
# index_bowl = 1
# for div in innings20Players:
#     tempvar = []
#     for div1 in div.find_all('div'):
#         tempvar.append(div1.text.strip())
#     # print tempvar
#     if len(tempvar) == 7:
#         batScoreCard20['player'+ str(index_bat)] = tempvar
#         index_bat +=1
#     elif len(tempvar) == 8:
#         bowlScoreCard20['player'+ str(index_bowl)] = tempvar
#         index_bowl +=1
#     else:
#         if tempvar[0] == "Extras":
#             tempvar[2] = tempvar[2].replace('(',' ')
#             tempvar[2] = tempvar[2].replace(')',' ')
#             x = tempvar[2].split(',')
#             # print x
#             extras20 = {
#                 'wide' : x[2].strip().split(' ')[1] ,
#                 'nb' : x[3].strip().split(' ')[1],
#                 'lb' : x[1].strip().split(' ')[1],
#                 'b' : x[0].strip().split(' ')[1],
#                 'p' : x[4].strip().split(' ')[1]
#             }
#         if tempvar[0] == "Total":
#             tempvar[2] = tempvar[2].replace('(',' ')
#             tempvar[2] = tempvar[2].replace(')',' ')
#             x = tempvar[2].split(',') 
#             total20 = {
#                 'runs' : tempvar[1].strip(),
#                 'overs': x[1].strip().split(' ')[0],
#                 'wickets' : x[0].strip().split(' ')[0]
#             }

# fallOfWicket = innings20id.find(class_='cb-col cb-col-100 cb-col-rt cb-font-13')
# fallOfWicketList = []
# fallOfWicketList = (x.text for x in fallOfWicket.find_all('span'))
# # fallOfWicket = fallOfWicket.replace('(','') 
# # fallOfWicket = fallOfWicket.replace(')','')
# # print list(fallOfWicketList)

# FallOfWickets20 = {}
# index_wicket = 1
# for x in fallOfWicketList:
#     x = x.split('-')
#     # print x
#     overNo = x[1].replace(')','').split(',')[1].strip()
#     calcBall = list(int(x) for x in overNo.split('.'))
#     ball = ((calcBall[0] * 6 + calcBall[1]) if len(calcBall) > 1 else calcBall[0]*6 )
#     # ball = 'yes' if len(calcBall) > 1 else 'no'
#     FallOfWickets20['player' + str(index_wicket)] = {
#         'teamScore' : x[0],
#         'ballNo' : ball
#     }
#     index_wicket += 1


# innings20BowlingTeam = (teams['team1'] if teams['team1'] != innings20BattingTeam[0] else teams['team2'])

# innings20 = {
#         "batTeam": innings20BattingTeam[0],
#         "batScoreCard": batScoreCard20,
#         "FallOfWickets": FallOfWickets20,
#         "bowlTeam": innings20BowlingTeam,
#         "bowlScoreCard": bowlScoreCard20,
#         "extras": extras20,
#         "total": total20
#     }

# # print '\n INNINGS 2 Brd \n'
# # print innings20

# # for div in innings20Players:
#     # print div.text


# #  INNINGS 20

# innings21BattingTeam = innings21id.find(class_='cb-col cb-col-100 cb-scrd-hdr-rw').text.strip(' ').split(' ') 

# batScoreCard21 = {}
# bowlScoreCard21 = {}
# extras21 = {}
# total21 = {}
# index_bat = 1
# index_bowl = 1
# for div in innings21Players:
#     tempvar = []
#     for div1 in div.find_all('div'):
#         tempvar.append(div1.text.strip())
#     # print tempvar
#     if len(tempvar) == 7:
#         batScoreCard21['player'+ str(index_bat)] = tempvar
#         index_bat +=1
#     elif len(tempvar) == 8:
#         bowlScoreCard21['player'+ str(index_bowl)] = tempvar
#         index_bowl +=1
#     else:
#         if tempvar[0] == "Extras":
#             tempvar[2] = tempvar[2].replace('(',' ')
#             tempvar[2] = tempvar[2].replace(')',' ')
#             x = tempvar[2].split(',')
#             # print x
#             extras21 = {
#                 'wide' : x[2].strip().split(' ')[1] ,
#                 'nb' : x[3].strip().split(' ')[1],
#                 'lb' : x[1].strip().split(' ')[1],
#                 'b' : x[0].strip().split(' ')[1],
#                 'p' : x[4].strip().split(' ')[1]
#             }
#         if tempvar[0] == "Total":
#             tempvar[2] = tempvar[2].replace('(',' ')
#             tempvar[2] = tempvar[2].replace(')',' ')
#             x = tempvar[2].split(',') 
#             total21 = {
#                 'runs' : tempvar[1].strip(),
#                 'overs': x[1].strip().split(' ')[0],
#                 'wickets' : x[0].strip().split(' ')[0]
#             }

# fallOfWicket = innings21id.find(class_='cb-col cb-col-100 cb-col-rt cb-font-13')
# fallOfWicketList = []
# fallOfWicketList = (x.text for x in fallOfWicket.find_all('span'))
# # fallOfWicket = fallOfWicket.replace('(','') 
# # fallOfWicket = fallOfWicket.replace(')','')
# # print list(fallOfWicketList)

# FallOfWickets21 = {}
# index_wicket = 1
# for x in fallOfWicketList:
#     x = x.split('-')
#     # print x
#     overNo = x[1].replace(')','').split(',')[1].strip()
#     calcBall = list(int(x) for x in overNo.split('.'))
#     ball = ((calcBall[0] * 6 + calcBall[1]) if len(calcBall) > 1 else calcBall[0]*6 )
#     # ball = 'yes' if len(calcBall) > 1 else 'no'
#     FallOfWickets21['player' + str(index_wicket)] = {
#         'teamScore' : x[0],
#         'ballNo' : ball
#     }
#     index_wicket += 1


# innings21BowlingTeam = (teams['team1'] if teams['team1'] != innings21BattingTeam[0] else teams['team2'])

# innings21 = {
#         "batTeam": innings21BattingTeam[0],
#         "batScoreCard": batScoreCard21,
#         "FallOfWickets": FallOfWickets21,
#         "bowlTeam": innings21BowlingTeam,
#         "bowlScoreCard": bowlScoreCard21,
#         "extras": extras21,
#         "total": total21
#     }

# # print '\n INNINGS 2 Guj \n'
# # print innings21

# # for div in innings21Players:
#     # print div.text




# finalObject = {
#     "Ranji2018": 
#   [{
#       "matchInfo" : matchInfo,
#       "innings10" : innings10,
#       "innings11" : innings11,
#       "innings20" : innings20,
#       "innings21" : innings21
#   }]
# }









# print '\n MATCH INFO \n'
# print matchInfo