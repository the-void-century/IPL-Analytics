"""
A module to import and work with CSV files
"""
import csv
import matplotlib.pyplot as plt

scores_by_team = {}
batsman_to_run = {}
umpire_to_country = {}
umpire_list = set()
matches_by_team = {}
matches_by_season = {}
winners_by_team = {}
extra_run_by_team = {}
id_to_year = {}
bowlers_runs_conceded = {}
bowlers_balls_played = {}


def teams():
    """This module extracts the data from the csv and transforms it"""
    with open('data/umpires.csv', encoding='utf') as csv_file:
        umpire_reader = csv.DictReader(csv_file)
        for umpires in umpire_reader:
            if umpires["umpire"] != '':
                umpire_to_country[umpires["umpire"]] = umpires[" country"]
    with open('data/matches.csv', encoding='utf') as csv_file:
        match_reader = csv.DictReader(csv_file)
        for matches in match_reader:
            id_to_year[matches["id"]] = int(matches["season"])
            umpire_list.add(matches["umpire1"])
            umpire_list.add(matches["umpire2"])
            if matches["team1"] not in matches_by_team:
                game_by_season = {'2008': 0, '2009': 0, '2010': 0, '2011': 0,
                                  '2012': 0, '2013': 0, '2014': 0, '2015': 0, '2016': 0, '2017': 0}
                game_by_season[matches["season"]] += 1
                matches_by_team[matches["team1"]] = game_by_season
            else:
                if matches["season"] not in matches_by_team[matches["team1"]]:
                    matches_by_team[matches["team1"]][matches["season"]] = 1
                else:
                    matches_by_team[matches["team1"]][matches["season"]] += 1
            if matches["team2"] not in matches_by_team:
                game_by_season = {'2008': 0, '2009': 0, '2010': 0, '2011': 0,
                                  '2012': 0, '2013': 0, '2014': 0, '2015': 0, '2016': 0, '2017': 0}
                game_by_season[matches["season"]] += 1
                matches_by_team[matches["team2"]] = game_by_season
            else:
                if matches["season"] not in matches_by_team[matches["team2"]]:
                    matches_by_team[matches["team2"]][matches["season"]] = 1
                else:
                    matches_by_team[matches["team2"]][matches["season"]] += 1
            if int(matches["season"]) not in matches_by_season:
                matches_by_season[int(matches["season"])] = 1
            else:
                matches_by_season[int(matches["season"])] += 1
            if matches["winner"] not in winners_by_team:
                game_by_season = {'2008': 0, '2009': 0, '2010': 0, '2011': 0,
                                  '2012': 0, '2013': 0, '2014': 0, '2015': 0, '2016': 0, '2017': 0}
                game_by_season[matches["season"]] += 1
                winners_by_team[matches["winner"]] = game_by_season
            else:
                if matches["season"] not in winners_by_team[matches["winner"]]:
                    winners_by_team[matches["winner"]][matches["season"]] = 1
                else:
                    winners_by_team[matches["winner"]][matches["season"]] += 1

    with open('data/deliveries.csv', encoding='utf-8') as csv_file:
        deliveries_reader = csv.DictReader(csv_file)
        for matches in deliveries_reader:
            if matches["batting_team"] not in scores_by_team:
                year_to_runs = {id_to_year[matches["match_id"]]: int(
                    matches["total_runs"])}
                scores_by_team[matches["batting_team"]] = year_to_runs
            else:
                if id_to_year[matches["match_id"]] not in scores_by_team[matches["batting_team"]]:
                    scores_by_team[matches["batting_team"]][id_to_year[matches["match_id"]]] = int(
                        matches["total_runs"])
                else:
                    scores_by_team[matches["batting_team"]][id_to_year[matches["match_id"]]] += int(
                        matches["total_runs"])
            if matches["batting_team"] == "Royal Challengers Bangalore":
                if matches["batsman"] not in batsman_to_run:
                    batsman_to_run[matches["batsman"]] = int(
                        matches["total_runs"])
                else:
                    batsman_to_run[matches["batsman"]
                                   ] += int(matches["total_runs"])
            if id_to_year[matches["match_id"]] == 2016:
                if matches["bowling_team"] not in extra_run_by_team:
                    extra_run_by_team[matches["bowling_team"]] = int(
                        matches["extra_runs"])
                else:
                    extra_run_by_team[matches["bowling_team"]
                                      ] += int(matches["extra_runs"])
            if id_to_year[matches["match_id"]] == 2015:
                if matches["bowler"] not in bowlers_balls_played:
                    bowlers_balls_played[matches["bowler"]] = 1
                else:
                    bowlers_balls_played[matches["bowler"]] += 1
                if matches["bowler"] not in bowlers_runs_conceded:
                    bowlers_runs_conceded[matches["bowler"]] = int(
                        matches["total_runs"])
                else:
                    bowlers_runs_conceded[matches["bowler"]
                                          ] += int(matches["total_runs"])


def add_two_lists(list1, list2):
    """A function for adding two lists of the same size"""
    for i in enumerate(list1):
        list1[i[0]] += list2[i[0]]
    return list1


def plot_total_runs():
    """Plots total tuns scored by teams over the years in form of a line chart"""
    print(scores_by_team)
    for team in scores_by_team.items():
        x_axis = list(team[1].keys())
        y_axis = list(team[1].values())
        x_axis, y_axis = zip(*sorted(zip(x_axis, y_axis)))
        plt.plot(x_axis, y_axis, label=team[0])
    plt.xlabel("Years")
    plt.ylabel("Total Runs")
    plt.title("Total runs scored by Teams over the years")
    plt.legend()
    plt.show()


def plot_top_batsmen():
    """Plots top 10 batsmen of all time in a bar graph format"""
    # print(batsman_to_run)
    batsmen = list(batsman_to_run.keys())
    runs = list(batsman_to_run.values())
    runs, batsmen = zip(*sorted(zip(runs, batsmen), reverse=True))
    print(list(zip(*sorted((zip(batsmen, runs))))))
    batsmen = list(batsmen[:10])
    runs = list(runs[:10])
    # print(batsmen,runs)
    plt.bar(batsmen, runs, width=0.4)
    plt.xlabel("Batsmen")
    plt.ylabel("Runs")
    plt.title("Top 10 batsmen in RCB over the course of IPL")
    plt.show()


def umpire_by_country():
    """Plots a bar graph showcasing the number of different
      nationalities fo umpires and their frequencies"""
    # print(umpire_list)
    country_count = {}
    for i in umpire_list:
        if i == '':
            continue
        if umpire_to_country[i] == '':
            continue
        print(umpire_to_country[i])
        if umpire_to_country[i] != " India":
            if umpire_to_country[i] not in country_count:
                country_count[umpire_to_country[i]] = 1
            else:
                country_count[umpire_to_country[i]] += 1
    print(country_count)
    x_axis = list(country_count.keys())
    y_axis = list(country_count.values())
    plt.bar(x_axis, y_axis, width=0.4)
    plt.xlabel("Countries")
    plt.ylabel("Number of umpires")
    plt.title("Umpires by country")
    plt.legend()
    plt.show()


def games_by_season():
    """This function prints a stacked bar chart of games every season"""
    team_list = list(matches_by_team.keys())
    # print(matches_by_team)
    baseline = [0]*10
    print(matches_by_team)
    for team in matches_by_team.items():
        seasons = list(team[1].keys())
        match = list(team[1].values())
        seasons, match = zip(*sorted(zip(seasons, match)))
        #print(team, years, match)
        plt.bar(seasons, match, bottom=baseline)
        # print(baseline)
        baseline = add_two_lists(baseline, match)

    plt.ylabel("Matches")
    plt.xlabel("Years")
    plt.legend(team_list)
    plt.title("Stacked bar chart of number of games played, by team , by season")
    plt.show()


def matches_every_year():
    """This function plots the bar graph of the number
      of matches played every year over the history of IPL"""
    seasons = list(matches_by_season.keys())
    match = list(matches_by_season.values())
    seasons, match = zip(*sorted(zip(seasons, match)))
    #print(years, match)
    plt.bar(seasons, match)
    plt.title("Matches played by year over the history of IPL")
    plt.xlabel("Years")
    plt.ylabel("Matches")
    plt.show()


def winner_by_season():
    """This function plots the stacked bar of winners by team by every season"""
    baseline = [0]*10
    team_list = list(winners_by_team.keys())
    for team in winners_by_team.items():
        seasons = list(team[1].keys())
        match = list(team[1].values())
        seasons, match = zip(*sorted(zip(seasons, match)))
        plt.bar(seasons, match, bottom=baseline)
        baseline = add_two_lists(baseline, match)
    plt.title("Stacked bar plot of winners by season by team")
    plt.legend(team_list)
    plt.xlabel("Years")
    plt.ylabel("Matches")
    plt.show()


def extra_runs_conceded():
    """This function plots a bar chart of extra runs conceded by every team in 2016"""
    # print(id_to_year)
    teams_in_2016 = list(extra_run_by_team.keys())
    runs = list(extra_run_by_team.values())
    # print(extra_run_by_team)
    plt.bar(teams_in_2016, runs, width=0.3)
    plt.title("Extra runs conceded per team in 2016")
    plt.xlabel("Teams")
    plt.ylabel("Extra Runs")
    plt.show()


def top_economical_bowler():
    """Plots top 10 economical bowlers in 2015"""
    bowler_economy_rate = {}
    for bowler in bowlers_balls_played.items():
        bowler_economy_rate[bowler[0]] = (
            (bowlers_runs_conceded[bowler[0]]/bowlers_balls_played[bowler[0]])*6)
    bowler_list = list(bowler_economy_rate.keys())
    bowler_economy = list(bowler_economy_rate.values())
    bowler_list, bowler_economy = zip(
        *sorted(zip(bowler_list, bowler_economy)))
    bowler_list = bowler_list[:10]
    bowler_economy = bowler_economy[:10]
    plt.bar(bowler_list, bowler_economy)
    plt.title("Top 10 bowlers by economy in 2015")
    plt.xlabel("Bowlers")
    plt.ylabel("Economy")
    plt.show()


def main():
    """main function"""
    teams()
    while True:
        print("Please Enter the corresponding number to select an option: ")
        print("1. Plot a chart of total runs scored by each teams over the history of IPL")
        print("2. Plot the total runs scored by top 10 batsmen",
              "playing for Royal Challengers Bangalore")
        print("3. Plot a chart of umpires by country (Ignoring",
              "Indian umpires since they would dominate the charts)")
        print("4. Plot a stacked bar chart of number of games played: by team and by season")
        print("5. Plot of a bar chart of number of",
              "matches played per year for all the years in IPL.")
        print("6. Plot a stacked bar chart of number of matches won per team per year in IPL.")
        print("7. Plot a bar chart of Extra runs conceded per team in the year 2016")
        print("8. Plot a bar chart of top 10 economical bowlers in the year 2015")
        print("Press any other number to exit")
        choice = int(input())
        if choice == 1:
            plot_total_runs()
        elif choice == 2:
            plot_top_batsmen()
        elif choice == 3:
            umpire_by_country()
        elif choice == 4:
            games_by_season()
        elif choice == 5:
            matches_every_year()
        elif choice == 6:
            winner_by_season()
        elif choice == 7:
            extra_runs_conceded()
        elif choice == 8:
            top_economical_bowler()
        else:
            break


if __name__ == "__main__":
    main()
