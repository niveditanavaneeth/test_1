import requests
from bs4 import BeautifulSoup 
import xlsxwriter
import os

# import requests, bs4
url = 'https://www.espncricinfo.com/series/8050/scorecard/1053479/andhra-vs-himachal-pradesh-group-c-ranji-trophy-2016-17'
r = requests.get(url)
soup = BeautifulSoup(r.text, 'lxml')

results = soup.find(class_="match-header")
tableBatsmanAll = soup.find_all(class_="table batsman")
# print table[0]

#-----------match details----------------

date = results.find(class_ = "desc text-truncate").getText()
print date

# teamlist
teams = results.find_all(class_="team-name")
teamList = []
teamList.append([td.getText() for td in teams])
print teamList

# player of the match
# playerOfMatch = results.find(class_="best-player-name").getText()
# print playerOfMatch
playerOfMatchTeam = results.find_all(class_=["best-player-team-name","best-player-name"])
playerOfMatchDetails = []
playerOfMatchDetails.append([td.getText() for td in playerOfMatchTeam])
 
# creation of workbook
cwd = os.getcwd()
path = cwd + '\\tmp\\batsmendata.xlsx'
workbook = xlsxwriter.Workbook(path)
worksheet = workbook.add_worksheet()
 
print '\n BatsmenData \n' 
for table in tableBatsmanAll:
    print '\n Batsmen : \n'
    rows = table.find_all(class_=["thead-light bg-light"])
    # print rows
    rows_data = table.find_all("tbody");
    # print rows_data

    #  row iteration
    rows = iter(rows)
    rows_data = iter(rows_data)

    headerList = [td.text for td in next(rows).find_all('th') if td.text]
    print headerList 

    w_row = 0
    w_column = 0

    # write operation for header
    for i in headerList:
        worksheet.write(w_row, w_column, headerList[w_column])
        w_column += 1 

    w_row +=1
    w_column = 0 

    # write operation for data rows
    for row in next(rows_data).find_all('tr'): 
        batsmanData = []
        for td1 in row.find_all('td'):
            if td1.text.encode("utf-8") != '':
                batsmanData.append(td1.text.encode("utf-8"))
                x = td1.text.encode("utf-8")
                # write operation
                worksheet.write(w_row, w_column, x.decode('utf-8').strip())

            w_column +=1
        print batsmanData
        w_column = 0
        if len(batsmanData) > 0:
            w_row += 1
        # print w_row , ' row count'

    # fall of wicket
    tfoot = table.find("tfoot")

    
    if(len(tfoot.find_all('tr')) == 2):
        totalScore = list(td.text for td in tfoot.find_all('tr')[0])
        fallOfWicket =  list(td.text.split(',') for td in tfoot.find_all('tr')[1])
    else:
        if (len(tfoot.find_all('tr')) == 3):
            totalScore = list(td.text for td in tfoot.find_all('tr')[0])
            # print totalScore1
            yetToPlay = list(td.text.split(',') for td in tfoot.find_all('tr')[1])
            print yetToPlay
            fallOfWicket =  list(td.text.split(',') for td in tfoot.find_all('tr')[2])
    print totalScore
    print fallOfWicket
    # playerOfMatchDetails.append([td.getText() for td in playerOfMatchTeam])



# #  bowler

print '\n BowlersList '

tableBowlerAll = soup.find_all(class_="table bowler")

for table in tableBowlerAll:
    print '\n bowlers : \n'
    headerList= table.find_all(class_=["thead-light bg-light"])
    headerList = iter(headerList)
    headerBowler = [td.text for td in next(headerList).find_all('th') if td.text]
    print headerBowler

    bowlerStats= table.find_all("tbody");
    bowlerStats = iter(bowlerStats)
    for row in next(bowlerStats).find_all('tr'): 
        bowlerData = []
        for td1 in row.find_all('td'):
            bowlerData.append(td1.text.encode("utf-8"))
        print bowlerData

print '\n MATCH DETAILS \n'
matchDetails = soup.find(class_='w-100 table match-details-table')
bodytag = matchDetails.find('tbody')
for details in bodytag.find_all('tr'):
    matchDetailsList = []
    for td in details.find_all('td'):
        # print td.text
        matchDetailsList.append(td.text)
        # print dataDetails
    print matchDetailsList

workbook.close()




# workbook.save("/tmp/batsmendata.xlsx")
# results = soup.find(id='ResultsContainer')
# # print (results.prettify());
# # job_elems = results.find_all('div', class_='Collapsible')
# job_elems_table = results.find_all('table', class_='table batsman')
# for job_elem in job_elems_table:
#     end='\n'*2
    # print(job_elem, end)

# 'C:/Users/nived/Desktop/scrapping/tmp/batsmendata.xlsx'
