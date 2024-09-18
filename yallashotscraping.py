import requests
from bs4 import BeautifulSoup
import csv

date = input("Please Enter a Date in the following format MM/DD/YYYY: ")
page = requests.get(f"https://www.yallakora.com/match-center/?date={date}#")

def main(page):
    src = page.content
    soup = BeautifulSoup(src, "lxml")
    matches_details = []

    championships = soup.find_all("div", class_="matchCard")

    def get_match_info(championship):
        championship_title = championship.find_all("h2")[0].text.strip()
        all_matches = championship.find_all("div", class_="ul")[0].find_all("div", recursive=False)
        number_of_matches = len(all_matches)

        for i in range(number_of_matches):
            # get teams names
            team_a = all_matches[i].find("div", class_="teamA").text.strip()
            team_b = all_matches[i].find("div", class_="teamB").text.strip()

            # get score
            match_result = all_matches[i].find("div", class_='MResult').find_all('span', class_='score')
            # Add non-breaking space before and after hyphen to prevent Excel from converting to date
            score = f"{match_result[0].text.strip()}\u00A0-\u00A0{match_result[1].text.strip()}"

            # get match time
            match_time = all_matches[i].find("div", class_='MResult').find('span', class_='time').text.strip()

            # add match info to matches_details
            matches_details.append({'نوع البطوله': championship_title,
                                    'الفريق الاول': team_a,
                                    'الفريق التاني': team_b,
                                    'النتيجه': score,
                                    'موعد المباراه': match_time})

    for i in range(len(championships)):
        get_match_info(championships[i])

    keys = matches_details[0].keys()

    with open('yalla.csv', 'w', newline='', encoding='utf-8-sig') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(matches_details)
        print("done")

main(page)
