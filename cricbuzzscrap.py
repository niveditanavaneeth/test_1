import requests
from bs4 import BeautifulSoup 
import os
import json
from datetime import datetime

# import requests, bs4

url = 'https://www.cricbuzz.com/live-cricket-scorecard/20881/brd-vs-guj-round-1-elite-group-a-ranji-trophy-2018-19'
r = requests.get(url)

# if r.status_code != 200:
#     raise DownloadError("oops, could not grab the page", r)

soup = BeautifulSoup(r.text, 'lxml')
detailsObject = {}


innings10id = soup.find(id = "innings_1")
innings11id = soup.find(id = "innings_2") 
innings20id = soup.find(id = "innings_3")
innings21id = soup.find(id = "innings_4")

innings10Players = innings10id.find_all(class_="cb-col cb-col-100 cb-scrd-itms")
innings11Players = innings11id.find_all(class_="cb-col cb-col-100 cb-scrd-itms")
innings20Players = innings20id.find_all(class_="cb-col cb-col-100 cb-scrd-itms")
innings21Players = innings21id.find_all(class_="cb-col cb-col-100 cb-scrd-itms")

# print innings10Players

# teamBat = innings10id.find(class_="cb-col cb-col-100 cb-scrd-hdr-rw")
# print teamBat.text

matchHeader = soup.find(class_='cb-nav-hdr cb-font-18 line-ht24').text.split(',') 
teamList = matchHeader[0].split('vs')
teams = {
        'team1' : teamList[0].strip(),
        'team2' : teamList[1].strip()
}

# INNINGS 10

innings10BattingTeam = innings10id.find(class_='cb-col cb-col-100 cb-scrd-hdr-rw').text.strip(' ').split(' ') 

batScoreCard = {}
bowlScoreCard = {}
extras = {}
total = {}
index_bat = 1
index_bowl = 1
for div in innings10Players:
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
            # print tempvar[2]
            x = tempvar[2].split(',')
            # print x
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

fallOfWicket = innings10id.find(class_='cb-col cb-col-100 cb-col-rt cb-font-13')
fallOfWicketList = []
fallOfWicketList = (x.text for x in fallOfWicket.find_all('span'))
# fallOfWicket = fallOfWicket.replace('(','') 
# fallOfWicket = fallOfWicket.replace(')','')
# print list(fallOfWicketList)

FallOfWickets = {}
index_wicket = 1
for x in fallOfWicketList:
    x = x.split('-')
    # over = x[1].replace(')','').split(',')
    # print x
    overNo = x[1].replace(')','').split(',')[1].strip()
    calcBall = list(int(x) for x in overNo.split('.'))
    ball = ((calcBall[0] * 6 + calcBall[1]) if len(calcBall) > 1 else calcBall[0]*6 )
    # ball = 'yes' if len(calcBall) > 1 else 'no'
    FallOfWickets['player' + str(index_wicket)] = {
        'teamScore' : x[0],
        'ballNo' : ball
    }
    index_wicket += 1


innings10BowlingTeam = (teams['team1'] if teams['team1'] != innings10BattingTeam[0] else teams['team2'])

innings10 = {
        "batTeam": innings10BattingTeam[0],
        "batScoreCard": batScoreCard,
        "FallOfWickets": FallOfWickets,
        "bowlTeam": innings10BowlingTeam,
        "bowlScoreCard": bowlScoreCard,
        "extras": extras,
        "total": total
    }

print '\n INNINGS 1 Bar \n'
print innings10

#  INNINGS 11

innings11BattingTeam = innings11id.find(class_='cb-col cb-col-100 cb-scrd-hdr-rw').text.strip(' ').split(' ') 

batScoreCard11 = {}
bowlScoreCard11 = {}
extras11 = {}
total11 = {}
index_bat = 1
index_bowl = 1
for div in innings11Players:
    tempvar = []
    for div1 in div.find_all('div'):
        tempvar.append(div1.text.strip())
    # print tempvar
    if len(tempvar) == 7:
        batScoreCard11['player'+ str(index_bat)] = tempvar
        index_bat +=1
    elif len(tempvar) == 8:
        bowlScoreCard11['player'+ str(index_bowl)] = tempvar
        index_bowl +=1
    else:
        if tempvar[0] == "Extras":
            tempvar[2] = tempvar[2].replace('(',' ')
            tempvar[2] = tempvar[2].replace(')',' ')
            x = tempvar[2].split(',')
            # print x
            extras11 = {
                'wide' : x[2].strip().split(' ')[1] ,
                'nb' : x[3].strip().split(' ')[1],
                'lb' : x[1].strip().split(' ')[1],
                'b' : x[0].strip().split(' ')[1],
                'p' : x[4].strip().split(' ')[1]
            }
        if tempvar[0] == "Total":
            tempvar[2] = tempvar[2].replace('(',' ')
            tempvar[2] = tempvar[2].replace(')',' ')
            x = tempvar[2].split(',') 
            total11 = {
                'runs' : tempvar[1].strip(),
                'overs': x[1].strip().split(' ')[0],
                'wickets' : x[0].strip().split(' ')[0]
            }

fallOfWicket = innings11id.find(class_='cb-col cb-col-100 cb-col-rt cb-font-13')
fallOfWicketList = []
fallOfWicketList = (x.text for x in fallOfWicket.find_all('span'))
# fallOfWicket = fallOfWicket.replace('(','') 
# fallOfWicket = fallOfWicket.replace(')','')
# print list(fallOfWicketList)

FallOfWickets11 = {}
index_wicket = 1
for x in fallOfWicketList:
    x = x.split('-')
    # print x
    overNo = x[1].replace(')','').split(',')[1].strip()
    calcBall = list(int(x) for x in overNo.split('.'))
    ball = ((calcBall[0] * 6 + calcBall[1]) if len(calcBall) > 1 else calcBall[0]*6 )
    # ball = 'yes' if len(calcBall) > 1 else 'no'
    FallOfWickets11['player' + str(index_wicket)] = {
        'teamScore' : x[0],
        'ballNo' : ball
    }
    index_wicket += 1


innings11BowlingTeam = (teams['team1'] if teams['team1'] != innings11BattingTeam[0] else teams['team2'])

innings11 = {
        "batTeam": innings11BattingTeam[0],
        "batScoreCard": batScoreCard11,
        "FallOfWickets": FallOfWickets11,
        "bowlTeam": innings11BowlingTeam,
        "bowlScoreCard": bowlScoreCard11,
        "extras": extras11,
        "total": total11
    }

print '\n INNINGS 1 Guj \n'
print innings11

# for div in innings11Players:
    # print div.text

#  INNINGS 20

innings20BattingTeam = innings20id.find(class_='cb-col cb-col-100 cb-scrd-hdr-rw').text.strip(' ').split(' ') 

batScoreCard20 = {}
bowlScoreCard20 = {}
extras20 = {}
total20 = {}
index_bat = 1
index_bowl = 1
for div in innings20Players:
    tempvar = []
    for div1 in div.find_all('div'):
        tempvar.append(div1.text.strip())
    # print tempvar
    if len(tempvar) == 7:
        batScoreCard20['player'+ str(index_bat)] = tempvar
        index_bat +=1
    elif len(tempvar) == 8:
        bowlScoreCard20['player'+ str(index_bowl)] = tempvar
        index_bowl +=1
    else:
        if tempvar[0] == "Extras":
            tempvar[2] = tempvar[2].replace('(',' ')
            tempvar[2] = tempvar[2].replace(')',' ')
            x = tempvar[2].split(',')
            # print x
            extras20 = {
                'wide' : x[2].strip().split(' ')[1] ,
                'nb' : x[3].strip().split(' ')[1],
                'lb' : x[1].strip().split(' ')[1],
                'b' : x[0].strip().split(' ')[1],
                'p' : x[4].strip().split(' ')[1]
            }
        if tempvar[0] == "Total":
            tempvar[2] = tempvar[2].replace('(',' ')
            tempvar[2] = tempvar[2].replace(')',' ')
            x = tempvar[2].split(',') 
            total20 = {
                'runs' : tempvar[1].strip(),
                'overs': x[1].strip().split(' ')[0],
                'wickets' : x[0].strip().split(' ')[0]
            }

fallOfWicket = innings20id.find(class_='cb-col cb-col-100 cb-col-rt cb-font-13')
fallOfWicketList = []
fallOfWicketList = (x.text for x in fallOfWicket.find_all('span'))
# fallOfWicket = fallOfWicket.replace('(','') 
# fallOfWicket = fallOfWicket.replace(')','')
# print list(fallOfWicketList)

FallOfWickets20 = {}
index_wicket = 1
for x in fallOfWicketList:
    x = x.split('-')
    # print x
    overNo = x[1].replace(')','').split(',')[1].strip()
    calcBall = list(int(x) for x in overNo.split('.'))
    ball = ((calcBall[0] * 6 + calcBall[1]) if len(calcBall) > 1 else calcBall[0]*6 )
    # ball = 'yes' if len(calcBall) > 1 else 'no'
    FallOfWickets20['player' + str(index_wicket)] = {
        'teamScore' : x[0],
        'ballNo' : ball
    }
    index_wicket += 1


innings20BowlingTeam = (teams['team1'] if teams['team1'] != innings20BattingTeam[0] else teams['team2'])

innings20 = {
        "batTeam": innings20BattingTeam[0],
        "batScoreCard": batScoreCard20,
        "FallOfWickets": FallOfWickets20,
        "bowlTeam": innings20BowlingTeam,
        "bowlScoreCard": bowlScoreCard20,
        "extras": extras20,
        "total": total20
    }

print '\n INNINGS 2 Brd \n'
print innings20

# for div in innings20Players:
    # print div.text


#  INNINGS 20

innings21BattingTeam = innings21id.find(class_='cb-col cb-col-100 cb-scrd-hdr-rw').text.strip(' ').split(' ') 

batScoreCard21 = {}
bowlScoreCard21 = {}
extras21 = {}
total21 = {}
index_bat = 1
index_bowl = 1
for div in innings21Players:
    tempvar = []
    for div1 in div.find_all('div'):
        tempvar.append(div1.text.strip())
    # print tempvar
    if len(tempvar) == 7:
        batScoreCard21['player'+ str(index_bat)] = tempvar
        index_bat +=1
    elif len(tempvar) == 8:
        bowlScoreCard21['player'+ str(index_bowl)] = tempvar
        index_bowl +=1
    else:
        if tempvar[0] == "Extras":
            tempvar[2] = tempvar[2].replace('(',' ')
            tempvar[2] = tempvar[2].replace(')',' ')
            x = tempvar[2].split(',')
            # print x
            extras21 = {
                'wide' : x[2].strip().split(' ')[1] ,
                'nb' : x[3].strip().split(' ')[1],
                'lb' : x[1].strip().split(' ')[1],
                'b' : x[0].strip().split(' ')[1],
                'p' : x[4].strip().split(' ')[1]
            }
        if tempvar[0] == "Total":
            tempvar[2] = tempvar[2].replace('(',' ')
            tempvar[2] = tempvar[2].replace(')',' ')
            x = tempvar[2].split(',') 
            total21 = {
                'runs' : tempvar[1].strip(),
                'overs': x[1].strip().split(' ')[0],
                'wickets' : x[0].strip().split(' ')[0]
            }

fallOfWicket = innings21id.find(class_='cb-col cb-col-100 cb-col-rt cb-font-13')
fallOfWicketList = []
fallOfWicketList = (x.text for x in fallOfWicket.find_all('span'))
# fallOfWicket = fallOfWicket.replace('(','') 
# fallOfWicket = fallOfWicket.replace(')','')
# print list(fallOfWicketList)

FallOfWickets21 = {}
index_wicket = 1
for x in fallOfWicketList:
    x = x.split('-')
    # print x
    overNo = x[1].replace(')','').split(',')[1].strip()
    calcBall = list(int(x) for x in overNo.split('.'))
    ball = ((calcBall[0] * 6 + calcBall[1]) if len(calcBall) > 1 else calcBall[0]*6 )
    # ball = 'yes' if len(calcBall) > 1 else 'no'
    FallOfWickets21['player' + str(index_wicket)] = {
        'teamScore' : x[0],
        'ballNo' : ball
    }
    index_wicket += 1


innings21BowlingTeam = (teams['team1'] if teams['team1'] != innings21BattingTeam[0] else teams['team2'])

innings21 = {
        "batTeam": innings21BattingTeam[0],
        "batScoreCard": batScoreCard21,
        "FallOfWickets": FallOfWickets21,
        "bowlTeam": innings21BowlingTeam,
        "bowlScoreCard": bowlScoreCard21,
        "extras": extras21,
        "total": total21
    }

print '\n INNINGS 2 Guj \n'
print innings21

# for div in innings21Players:
    # print div.text



#  MATCH DETAILS

matchDetails = soup.find(class_="cb-col cb-col-100 cb-font-13") 

details = []
for div in matchDetails.find_all(class_="cb-col cb-col-73"):
    # print ('\n')
    # print div
    details.append(div.text)
    
# print details

# teamdetails = details[0].split(',')
# teams = teamdetails[0].strip().split('vs')
# matchinfo = {}
# matchinfo['teams'] = {'team1' : teams[0].strip(), 'team2' : teams[1].strip() }
# print matchinfo

tossdetails = details[2].split(' ')
toss = {}
toss = {'winner' : tossdetails[0].strip() ,'decision' : tossdetails[7].strip()}
# print toss

date = {}
date1 = []
for i,div in enumerate(matchDetails.find_all(class_="schedule-date")): 
    # date1 = datetime.utcfromtimestamp(int(div.attrs['timestamp']))
    # date1 = datetime.strptime(div.attrs['timestamp'], ' %d %b %Y')
    date_1 = datetime.fromtimestamp(float(div.attrs['timestamp'])/1000.0).isoformat()
    date1.append(date_1)

date = {'startDate' : date1[0],
          'endDate': date1[1]}
# print date

umpirelist = details[5].split(',')
umpirelist.append(details[6])
umpire = {}
umpire = {'umpire1':umpirelist[0].strip(),
          'umpire2': umpirelist[1].strip(),
          'thirdUmpire': umpirelist[2].strip()}
# print umpire

roundNo = ''
groupName = ''


squad = {}
squad['team1'] = { "teamName": "",
            "playing11": details[7].split(','),
            "bench": details[8].split(',')
             } 
squad['team2'] = { "teamName": "",
            "playing11": details[9].split(','),
            "bench": details[10].split(',')
             } 
# print squad

matchInfo = {
        "matchType": "Ranji Test Match",
        "teams": teams,
        "toss": toss,
        "venue": details[4],
        "date": date,
        "umpire": umpire,
        "roundNo": matchHeader[1].strip(),
        "groupName": matchHeader[2].split('-')[0].strip(),
        "squad": squad
    }

finalObject = {
    "Ranji2018": 
  [{
      "matchInfo" : matchInfo,
      "innings10" : innings10,
      "innings11" : innings11,
      "innings20" : innings20,
      "innings21" : innings21
  }]
}

with open('RanjiStructure.json', 'w') as json_file:
  json.dump(finalObject, json_file, indent=4, sort_keys= True)

# print '\n MATCH INFO \n'
# print matchInfo