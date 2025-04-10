#importing necessary modules
import requests
from bs4 import BeautifulSoup
import csv

#defining the working url
url = "https://www.scrapethissite.com/pages/forms/?page_num={}"
#filename to save our data 
filename = "teams.csv"


with open(filename, "w", newline="", encoding='utf-8') as file:
    writer = csv.writer(file)
    
    writer.writerow(["Team_name","year","Wins","Losses","OT Losses","Wins","Goals_for_gf","Goals_agains_gf", "+ / -"])

    headers = {'User-Agent':'Chrome'}
    
    page = 1

    while True:
        response = requests.get(url.format(page), headers=headers)
        soup = BeautifulSoup(response.text, "lxml")

        if page == 25:
            print(f"Finished all the pages:")
            break
        
        teams = soup.find_all("tr", class_="team")

        for team in teams:
            team_name = team.find("td", class_="name").text.strip() if team.find("td", class_="name") else "N/A"
            year = team.find("td", class_="year").text.strip() if team.find("td", class_="year") else "N/A"
            wins = team.find("td", class_="wins").text.strip() if team.find("td", class_="wins") else "N/A"
            losses = team.find("td", class_="losses").text.strip() if team.find("td", class_="losses") else "N/A"
            ot_losses = team.find("td", class_="ot-losses").text.strip() if team.find("td", class_="ot-losses") else "N/A"
            win_ = team.find("td", class_="pct text-success").text.strip() if team.find("td", class_="pct text-success") else team.find("td", class_="pct text-danger").text.strip() 
            gf = team.find("td", class_="gf").text.strip() if team.find("td", class_="gf") else "N/A"
            ga = team.find("td", class_="ga").text.strip() if team.find("td", class_="ga") else "N/A"
            last = team.find("td", class_="diff text-success").text.strip() if team.find("td", class_="diff text-success") else team.find("td", class_="diff text-danger").text.strip()

            writer.writerow([team_name,year,wins,losses,ot_losses,win_,gf,ga,last])
            
        print(f"Finished scrapping page: {page}")
        page += 1


        

        
        


