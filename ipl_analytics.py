import csv
import matplotlib.pyplot as plt

scores_by_team={}
batsman_to_run={}
umpire_to_country={}
umpire_list=set()
matches_by_team={}
matches_by_season={}
winners_by_team={}
extra_run_by_team={}
id_to_year={}
bowlers_runs_conceded={}
bowlers_balls_played={}
colors=["black","dimgrey","darkgrey","olive","maroon","salmon","orangered","saddlebrown","burlywood","goldenrod","lawngreen","g","dodgerblue","magenta"]


def teams():
    with open('data/umpires.csv') as csv_file:
        umpire_reader=csv.DictReader(csv_file)
        for umpires in umpire_reader:
            if umpires["umpire"]!='':
                umpire_to_country[umpires["umpire"]]=umpires[" country"]
            
    with open('data/matches.csv') as csv_file:
        match_reader=csv.DictReader(csv_file)
        
        for matches in match_reader:
            id_to_year[matches["id"]]=int(matches["season"])
            umpire_list.add(matches["umpire1"])
            umpire_list.add(matches["umpire2"])
            if matches["team1"] not in matches_by_team:
                game_by_season={matches["season"]:1}
                matches_by_team[matches["team1"]]=game_by_season
            else:
                if matches["season"] not in matches_by_team[matches["team1"]]:
                    matches_by_team[matches["team1"]][matches["season"]]=1
                else:
                    matches_by_team[matches["team1"]][matches["season"]]+=1
            if matches["team2"] not in matches_by_team:
                game_by_season={matches["season"]:1}
                matches_by_team[matches["team2"]]=game_by_season
            else:
                if matches["season"] not in matches_by_team[matches["team2"]]:
                    matches_by_team[matches["team2"]][matches["season"]]=1
                else:
                    matches_by_team[matches["team2"]][matches["season"]]+=1
            if int(matches["season"]) not in matches_by_season:
                matches_by_season[int(matches["season"])]=1
            else:
                matches_by_season[int(matches["season"])]+=1
            if matches["winner"] not in winners_by_team:
                winner_by_season={matches["season"]:1}
                winners_by_team[matches["winner"]]=winner_by_season
            else:
                if matches["season"] not in winners_by_team[matches["winner"]]:
                    winners_by_team[matches["winner"]][matches["season"]]=1
                else:
                    winners_by_team[matches["winner"]][matches["season"]]+=1


            



            
    with open('data/deliveries.csv') as csv_file:
        deliveries_reader=csv.DictReader(csv_file)
        for matches in deliveries_reader:
            if matches["batting_team"] not in scores_by_team:
                year_to_runs={id_to_year[matches["match_id"]]:int(matches["total_runs"])}
                scores_by_team[matches["batting_team"]]=year_to_runs
            else:
                if id_to_year[matches["match_id"]] not in scores_by_team[matches["batting_team"]]:
                    scores_by_team[matches["batting_team"]][id_to_year[matches["match_id"]]]=int(matches["total_runs"])
                else:
                    scores_by_team[matches["batting_team"]][id_to_year[matches["match_id"]]]+=int(matches["total_runs"])
            if matches["batting_team"]=="Royal Challengers Bangalore":
                if matches["batsman"] not in batsman_to_run:
                    batsman_to_run[matches["batsman"]]=int(matches["total_runs"])
                else:
                    batsman_to_run[matches["batsman"]]+=int(matches["total_runs"])
            if id_to_year[matches["match_id"]]==2016:
                if matches["bowling_team"] not in extra_run_by_team:
                    extra_run_by_team[matches["bowling_team"]]=int(matches["extra_runs"])
                else:
                    extra_run_by_team[matches["bowling_team"]]+=int(matches["extra_runs"])
            if id_to_year[matches["match_id"]]==2015:
                if matches["bowler"] not in bowlers_balls_played:
                    bowlers_balls_played[matches["bowler"]]=1
                else:
                    bowlers_balls_played[matches["bowler"]]+=1
                if matches["bowler"] not in bowlers_runs_conceded:
                    bowlers_runs_conceded[matches["bowler"]]=int(matches["total_runs"])
                else:
                    bowlers_runs_conceded[matches["bowler"]]+=int(matches["total_runs"])
            





def plot_total_runs():
    color_count=0
    print(scores_by_team)
    for team in scores_by_team:
        x_axis=list(scores_by_team[team].keys())
        y_axis=list(scores_by_team[team].values())
        x_axis,y_axis=zip(*sorted(zip(x_axis,y_axis)))
        plt.plot(x_axis,y_axis,label=team,color=colors[color_count])
        color_count+=1
    plt.xlabel("Years")
    plt.ylabel("Total Runs")
    plt.title("Total runs scored by Teams over the years")
    plt.legend()
    plt.show()


def plot_top_batsmen():
    x_axis=list(batsman_to_run.keys())
    y_axis=list(batsman_to_run.values())
    x_axis,y_axis=zip(*sorted(zip(x_axis,y_axis),reverse=True))
    x_axis=x_axis[:10]
    y_axis=y_axis[:10]
    plt.bar(x_axis,y_axis,width=0.4)
    plt.xlabel("Batsmen")
    plt.ylabel("Runs")
    plt.title("Top 10 batsmen in RCB over the course of IPL")
    plt.legend()
    plt.show()

def umpire_by_country():
    print(umpire_list)
    country_count={}
    for i in umpire_list:
        if i=='':
            continue
        if umpire_to_country[i]=="India":
            continue
        if umpire_to_country[i] not in country_count:
            country_count[umpire_to_country[i]]=1
        else:
            country_count[umpire_to_country[i]]+=1
    x_axis=list(country_count.keys())
    y_axis=list(country_count.values())
    plt.bar(x_axis,y_axis,width=0.4)
    plt.xlabel("Countries")
    plt.ylabel("Number of umpires")
    plt.title("Umpires by country")
    plt.legend()
    plt.show()


def games_by_season():
    color_count=0
    team_list=list(matches_by_team.keys())
    #print(matches_by_team)
    for team in matches_by_team:
        years=list(matches_by_team[team].keys())
        match=list(matches_by_team[team].values())
        print(team,years,match)
        years,match=zip(*sorted(zip(years,match)))
        plt.bar(years,match,color=colors[color_count])
        color_count+=1
    plt.ylabel("Matches")
    plt.xlabel("Years")
    plt.legend(team_list)
    plt.title("Stacked bar chart of number of games played, by team , by season")
    plt.show()

def matches_every_year():
    years=list(matches_by_season.keys())
    match=list(matches_by_season.values())
    years,match=zip(*sorted(zip(years,match)))
    print(years,match)
    plt.bar(years,match)
    plt.title("Matches played by year over the history of IPL")
    plt.xlabel("Years")
    plt.ylabel("Matches")
    plt.show()

def winner_by_season():
    color_count=0
    team_list=list(winners_by_team.keys())
    for team in winners_by_team:
        years=list(winners_by_team[team].keys())
        match=list(winners_by_team[team].values())
        years,match=zip(*sorted(zip(years,match)))
        plt.bar(years,match)
        color_count+=1
    plt.title("Stacked bar plot of winners by season by team")
    plt.legend(team_list)
    plt.xlabel("Years")
    plt.ylabel("Matches")
    plt.show()

def extra_runs_conceded():
    #print(id_to_year)
    teams=list(extra_run_by_team.keys())
    runs=list(extra_run_by_team.values())
    #print(extra_run_by_team)
    plt.bar(teams,runs,width=0.3)
    plt.title("Extra runs conceded per team in 2016")
    plt.xlabel("Teams")
    plt.ylabel("Extra Runs")
    plt.show()

def top_economical_bowler():
    bowler_economy_rate={}
    for bowler in bowlers_balls_played:
        bowler_economy_rate[bowler]=((bowlers_runs_conceded[bowler]/bowlers_balls_played[bowler])*6)
    bowler_list=list(bowler_economy_rate.keys())
    bowler_economy=list(bowler_economy_rate.values())
    bowler_list,bowler_economy=zip(*sorted(zip(bowler_list,bowler_economy)))
    bowler_list=bowler_list[:10]
    bowler_economy=bowler_economy[:10]
    plt.bar(bowler_list,bowler_economy)
    plt.title("Top 10 bowlers by economy in 2015")
    plt.xlabel("Bowlers")
    plt.ylabel("Economy")
    plt.show()


def main():
    teams()
    while True:
        print("Please Enter the corresponding number to select an option: ")
        print("1. Plot a chart of total runs scored by each teams over the history of IPL")
        print("2. Plot the total runs scored by top 10 batsmen playing for Royal Challengers Bangalore")
        print("3. Plot a chart of umpires by country (Ignoring indian umpires since they would dominate the charts)")
        print("4. Plot a stacked bar chart of number of games played: by team and by season")
        print("5. Plot of a bar chart of number of matches played per year for all the years in IPL.")
        print("6. Plot a stacked bar chart of number of matches won per team per year in IPL.")
        print("7. Plot a bar chart of Extra runs conceded per team in the year 2016")
        print("8. Plot a bar chart of top 10 economical bowlers in the year 2015")
        print("Press any other number to exit")
        choice=int(input())
        if choice==1:
            plot_total_runs()
        elif choice==2:
            plot_top_batsmen()
        elif choice==3:
            umpire_by_country()
        elif choice==4:
            games_by_season()
        elif choice==5:
            matches_every_year()
        elif choice==6:
            winner_by_season()
        elif choice==7:
            extra_runs_conceded()
        elif choice==8:
            top_economical_bowler()
        else:
            break

if __name__ == "__main__":
    main()