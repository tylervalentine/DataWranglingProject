from dotenv import load_dotenv
import mysql.connector, os, csv
import webscrapeHallOfFame, webscrapeCareerLeaders, webscrapeTopIndividualPerf, webscrapePlayerCareerStats
from datetime import datetime


def connect_to_SQL():
    load_dotenv()
    conn = mysql.connector.connect(user=os.getenv("USERNAME"), password=os.getenv("PASSWORD"),
                                   host='127.0.0.1')
    cursor = conn.cursor()
    return cursor, conn


def createBaseballDB(cursor, db_name):
    cursor.execute('DROP DATABASE IF EXISTS ' + db_name)
    cursor.execute('CREATE DATABASE ' + db_name)
    cursor.execute('USE ' + db_name)


def createTable(cursor, fields, table_name):
    cursor.execute('DROP TABLE IF EXISTS {}'.format(table_name))
    columns = ','.join(['{} {}'.format(key, fields[key]) for key in fields.keys()])
    cursor.execute('CREATE TABLE {} ({})'.format(table_name, columns))


def loadPlayerNamesTable(cursor, player_names_dict, table_name):
    for player in player_names_dict:
        cursor.execute('INSERT INTO {} VALUES ("{}","{}")'.format(table_name, player_names_dict[player], player))


def loadHOFTable(cursor, hall_of_fame_dict, table_name):
    for player in hall_of_fame_dict:
        cursor.execute('INSERT INTO {} VALUES ("{}", "{}")'.format(table_name, player, hall_of_fame_dict[player]))


def loadPlayerBiosTable(cursor, bios_dict, table_name):
    for player in bios_dict:
        debut_date, final_game, bats, throws = bios_dict[player]
        cursor.execute(
            'INSERT INTO {} VALUES ("{}", "{}", "{}", "{}","{}")'.format(table_name, player,
                                                                         debut_date, final_game, bats, throws))


def loadCareerStatsTables(cursor, career_stats, table_name):
    for player in career_stats:
        stats_string = ','.join(career_stats[player])
        sql = f'INSERT INTO {table_name} VALUES ("{player}",' + stats_string + ')'  # string slicing to remove extra comma and append a parenthesis to the sql command
        cursor.execute(sql)


def createDBFields():
    name_fields = {
        'PlayerID': 'VARCHAR(100)',
        'PlayerName': 'VARCHAR(100)'
    }
    player_bio_fields = {
        'PlayerID': 'VARCHAR(100)',
        'debutDate': 'DATE',
        'finalGameDate': 'DATE',
        'bats': 'CHAR(1)',
        'throws': 'CHAR(1)'

    }
    hall_of_fame_fields = {
        'PlayerID': 'VARCHAR(25)',
        'YearOfInduction': 'Year'
    }
    all_time_batting = {
        'PlayerID': 'VARCHAR(25)',
        'AtBats': 'FLOAT',
        'BFW': 'FLOAT',
        'Batting_Avg': 'FLOAT',
        'CaughtStealing': 'FLOAT',
        'Doubles': 'FLOAT',
        'Games': 'FLOAT',
        'GroundedIntoDoublePlays': 'FLOAT',
        'HitByPitch': 'INT',
        'Hits': 'Float',
        'Homeruns': 'INT',
        'Intentional_Walks': 'INT',
        'OnBasePercentage': 'FLOAT',
        'Plate_Apps': 'INT',
        'RBIs': 'INT',
        'Runs': 'INT',
        'SacrificeFlies': 'INT',
        'SacrificeHits': 'INT',
        'SluggingPercent': 'FLOAT',
        'StolenBases': ' INT',
        'Strikeouts': 'INT',
        'Triples': 'INT',
        'Walks': 'INT'

    }
    all_time_pitching = {
        'PlayerID': 'VARCHAR(25)',
        'Balks': 'FLOAT',
        'CompleteGames': 'FLOAT',
        'ERA': 'FLOAT',
        'Earned_Runs': 'INT',
        'GamesFinished': 'INT',
        'GamesPitched': 'INT',
        'GamesStarted': 'INT',
        'HitByPitch': 'INT',
        'Hits': 'INT',
        'Homeruns': 'INT',
        'InningsPitched': 'INT',
        'IntentionalWalks': 'FLOAT',
        'Losses': 'INT',
        'PW': 'INT',
        'Runs': 'INT',
        'Saves': 'INT',
        'Shutouts': 'INT',
        'Strikeouts': 'INT',
        'Walks': ' INT',
        'WildPitches': 'INT',
        'Wins': 'INT'
    }

    career_batting_stats = {
        # Career Batting Table Columns
        'PlayerID': 'VARCHAR(100)',
        'Games': 'INT',
        'AtBats': 'INT',
        'Runs': 'INT',
        'Hits': 'INT',
        'Doubles': 'INT',
        'Triples': 'INT',
        'Homeruns': 'INT',
        'RBI': 'INT',
        'Walks': 'INT',
        'IntentionalWalks': 'INT',
        'Strikeouts': 'INT',
        'HitByPitch': 'INT',
        'Sacrifice_Hits': 'INT',
        'Sacrifice_Flies': 'INT',
        'XI': 'INT',
        'ROE': 'INT',
        'GroundedIntoDoublePlays': 'INT',
        'StolenBases': 'INT',
        'CaughtStealing': 'INT',
        'BattingAVG': 'FLOAT',
        'On_BasePercent': 'FLOAT',
        'SluggingPercent': 'FLOAT',
        'BFW': 'FLOAT'
    }

    career_pitching_stats = {
        # Career Pitching Table Columns
        'PlayerID': 'VARCHAR(100)',
        'Games': 'INT',
        'GamesStarted': 'INT',
        'CompleteGames': 'INT',
        'Shutouts': 'INT',
        'GamesFinished': 'INT',
        'Saves': 'INT',
        'InningsPitched': 'INT',
        'Hits': 'INT',
        'BFP': 'INT',
        'Homeruns': 'INT',
        'Runs': 'INT',
        'EarnedRuns': 'INT',
        'Walks': 'INT',
        'IntentionalWalks': 'INT',
        'Strikeouts': 'INT',
        'SacrificeHits': 'INT',
        'SacrificeFlies': 'INT',
        'WildPitches': 'INT',
        'HitByPitch': 'INT',
        'Balks': 'INT',
        'Doubles': 'INT',
        'Triples': 'INT',
        'GroundedIntoDoublePlays': 'INT',
        'ROE': 'INT',
        'Wins': 'INT',
        'Losses': 'INT',
        'ERA': 'FLOAT',
        'RunSupport': 'FLOAT',
        'PW': 'FLOAT'
    }

    return name_fields, player_bio_fields, hall_of_fame_fields, all_time_batting, all_time_pitching, career_batting_stats, career_pitching_stats


def loadBaseballData():
    """
    This function calls all of our webscraping python files which loads various sources from retrosheet into CSVs for database loading
    """
    webscrapeHallOfFame.main()
    webscrapeTopIndividualPerf.main()
    webscrapeCareerLeaders.main()


def webscrapeCareerStatsForEachPlayer(playerNameDictionary):
    """
    Opens batting/pitching files for adding career statistics
    This function calls our separate webscrape file which goes to each individual players url and scrapes either their pitching record, fielding record or both
    Any errors in formatting such as players missing fields or players that did not have certain stats were skipped over in the webscraping process
    We made sure not to abuse the webscraping of retrosheet by making sure only making calls out to the server 7 times per minute.

    I ran this particular function on my raspberry pi and it took roughly 23 hours total to webscrape all of the necessary data

    """
    # TODO Create Rate Limiting for Webscraping
    batting_file = open('playerinformation/batting_stats.csv', 'a')
    pitching_file = open('playerinformation/pitching_stats.csv', 'a')
    player_dict_len = len(playerNameDictionary.keys())
    current_index = 0
    player_list = list(playerNameDictionary.keys())
    for player in player_list:
        try:
            webscrapePlayerCareerStats.webscrapeCareerStats(player, playerNameDictionary, batting_file,
                                                            pitching_file)
            current_index += 1
            print('Current Completion Level: {}/{}'.format(current_index, player_dict_len))
        except ValueError:
            continue


def getDataDirectories(folder_name):
    directories = []
    for root, dirs, files in os.walk(folder_name):
        for file in files:
            if file.endswith('.csv'):
                directories.append(os.path.join(root, file))
    return directories


def convertDate(date):
    format_string = "%m/%d/%Y"
    try:
        d = datetime.strptime(date, format_string)
    except ValueError:
        # if there is no date we return 0000-01-01 to denote no date
        return '0000-01-01'
    output_date = "%Y-%m-%d"
    return d.strftime(output_date)


def getPlayerNamesDictionary(filename):
    playerNameDictionary = {}
    with open(filename) as file:
        file.readline()
        player_info = csv.reader(file)
        for line in player_info:
            line = [element.strip('"') for element in line]
            playerID, playerName = line[0], line[3] + ' ' + line[1]
            playerNameDictionary[playerName] = playerID

    return playerNameDictionary


def getPlayerBiosDictionary(filename):
    playerBioDictionary = {}
    with open(filename) as file:
        headers = [header.strip() for header in file.readline().split(',')]
        bats_index = headers.index('BATS')
        throws_index = headers.index('THROWS')
        debut_date_index = headers.index('PLAY DEBUT')
        final_game_index = headers.index('PLAY LASTGAME')
        player_info = csv.reader(file)
        for line in player_info:
            line = [element.strip('"') for element in line]
            playerID, debut_date, final_game, bats, throws = line[0], line[debut_date_index], line[final_game_index], \
                                                             line[bats_index], line[throws_index],
            debut_date, final_game = convertDate(debut_date), convertDate(final_game)
            playerBioDictionary[playerID] = [debut_date, final_game, bats, throws]
    return playerBioDictionary


def getHallOfFamePlayersDictionary(filename, playerNameDictionary):
    hall_of_fame_dictionary = {}
    with open(filename) as file:
        file.readline()
        hall_of_fame_info = csv.reader(file)
        for line in hall_of_fame_info:
            player_name, year_inducted = line[0], line[1]
            if player_name in playerNameDictionary:
                player_id = playerNameDictionary[player_name]
                hall_of_fame_dictionary[player_id] = year_inducted
    return hall_of_fame_dictionary


def loadAllTimeLeaders(filedirectories, playerDictionary, player_position, cursor):

    for filename in filedirectories:
        with open(filename) as file:
            headers = file.readline()
            headers = headers.replace("\n", "")
            categories = headers.split(",")
            categories[0] = categories[0].replace(" ", "")
            player_name_header = categories[0]
            category = categories[1]
            if category == "G":
                category_list = categories[1]
            else:
                category_list = categories[1:]

            fields = "playerID VARCHAR(255), " + player_name_header + " VARCHAR(255)"
            for value in category_list:
                value = value.replace("/", "Per")
                value = value.replace("%", "Percentage")
                fields = fields + ", " + value + " FLOAT"
            table_name = player_position + category
            cursor.execute('DROP TABLE IF EXISTS {}'.format(table_name))
            cursor.execute('CREATE TABLE {} ({})'.format(table_name, fields))
            all_time_stats = csv.reader(file)
            for line in all_time_stats:
                name = line[0]
                if name in playerDictionary:
                    value_command = 'INSERT INTO {} VALUES ("{}", "{}"'.format(table_name, playerDictionary[name], name)
                for values in line[1:]:
                    if category == "G":
                        value_command += ', "{}"'.format(values)
                        break
                    value_command += ', "{}"'.format(values)
                value_command += ')'
                cursor.execute(value_command)


def getCareerStatsForPlayersDictionary(filename):
    career_stats_dict = {}
    with open(filename) as file:
        file.readline()
        career_stats = csv.reader(file)
        for line in career_stats:
            career_stats_dict[line[0]] = line[1:]
    return career_stats_dict


def main():
    # loadBaseballData()

    cursor, conn = connect_to_SQL()
    createBaseballDB(cursor, "baseballStats_db")
    name_fields, player_bio_fields, hall_of_fame_fields, all_time_batting_fields, all_time_pitching_fields, \
    career_batting_stats_fields, career_pitching_stats_fields = createDBFields()

    # Player Names Table
    createTable(cursor, name_fields, 'PlayerNames')
    player_names_dict = getPlayerNamesDictionary('playerinformation/playerBios.csv')
    loadPlayerNamesTable(cursor, player_names_dict, 'PlayerNames')

    # Player Bios Table
    createTable(cursor, player_bio_fields, 'PlayerBios')
    player_bio_dict = getPlayerBiosDictionary('playerinformation/playerBios.csv')
    loadPlayerBiosTable(cursor, player_bio_dict, 'PlayerBios')

    # Hall Of Fame Table
    createTable(cursor, hall_of_fame_fields, 'HallOfFame')
    hall_of_fame_dict = getHallOfFamePlayersDictionary('awards/The Hall of Fame.csv', player_names_dict)
    loadHOFTable(cursor, hall_of_fame_dict, 'HallOfFame')

    # All Time Batting Leaders Table
    createTable(cursor, all_time_batting_fields, 'AllTimeBatting')
    all_time_batting_dirs = sorted(getDataDirectories('battingstats/careerleaders/'))
    batting_string = "Batting"
    loadAllTimeLeaders(all_time_batting_dirs, player_names_dict, batting_string, cursor)

    # All Time Pitching Leaders Table
    all_time_pitching_dirs = sorted(getDataDirectories('pitchingstats/careerleaders/'))
    createTable(cursor, all_time_pitching_fields, 'AllTimePitching')
    pitching_string = "Pitching"
    loadAllTimeLeaders(all_time_pitching_dirs, player_names_dict, pitching_string, cursor)

    # Career Batting Stats for All Players Table
    # webscrapeCareerStatsForEachPlayer(player_names_dict)
    createTable(cursor, career_batting_stats_fields, 'CareerBattingStats')
    career_batting_stats = getCareerStatsForPlayersDictionary('playerinformation/batting_stats.csv')
    loadCareerStatsTables(cursor, career_batting_stats, 'CareerBattingStats')

    # Career Pitching Stats for All Players Table
    createTable(cursor, career_pitching_stats_fields, 'CareerPitchingStats')
    career_pitching_stats = getCareerStatsForPlayersDictionary('playerinformation/pitching_stats.csv')
    loadCareerStatsTables(cursor, career_pitching_stats, 'CareerPitchingStats')
    conn.commit()


if __name__ == '__main__':
    main()
