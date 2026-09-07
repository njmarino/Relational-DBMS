import mysql.connector

#placeholder values
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="password",
    database="MLB"
)

print("Connected to the database...")

while True:
    print("\nMenu:")
    print("1. View all players")
    print("2. View all games")
    print("3. Get a player's game performance")
    print("4. Get a player's season batting average")
    print("5. Get team's division standings")
    print("6. Exit")
    
    choice = input("Enter your choice: ")
    
    #print all players
    if choice == "1":
        mycursor = db.cursor()
        mycursor.execute("SELECT firstName, lastName, playerID FROM PLAYER")
        result = mycursor.fetchall()
        print("\nList of all players:")
        for row in result:
            print(f"{row[0]} {row[1]} - ID: {row[2]}")

    #list games
    elif choice == "2":
        mycursor = db.cursor()
        mycursor.execute(f"SELECT * FROM GAME")
        result = mycursor.fetchall()
        print("\nList of all games:")
        for row in result:
            print(f"Game ID: {row[0]}, Date: {row[1]}, Home Team: {row[2]}, Away Team: {row[3]}, Home Score: {row[4]}, Away Score: {row[5]}")

    #Get player's game performance
    elif choice == "3":
        first_name = input("Enter player's first name: ")
        last_name = input("Enter player's last name: ")
        game_date = input("Enter game date (YYYY-MM-DD): ")
        mycursor = db.cursor()
        mycursor.execute(f"SELECT P.firstName, P.lastName, G.datePlayed, GS.hits, GS.homeruns, GS.battingAvg FROM PLAYER AS P, GAME AS G, GAME_STATS AS GS WHERE P.firstName = '{first_name}' AND P.lastName = '{last_name}' AND P.playerID = GS.playerID AND G.datePlayed = '{game_date}' AND GS.gameID = G.gameID")
        result = mycursor.fetchall()
        if result:
            print(f"\n{first_name} {last_name} played on {game_date}:")
            print(f"Hits: {result[0][3]}, Homeruns: {result[0][4]}, Batting Average: {result[0][5]}")
        else:
            print(f"\nNo game found for {first_name} {last_name} on {game_date}.")

    #Get player's season batting average
    elif choice == "4":
        first_name = input("Enter player's first name: ")
        last_name = input("Enter player's last name: ")
        season_year = input("Enter season year (YYYY): ")
        mycursor = db.cursor()
        mycursor.execute(f"SELECT AVG(GS.battingAvg) FROM PLAYER AS P, GAME_STATS AS GS, GAME AS G WHERE P.firstName = '{first_name}' AND P.lastName = '{last_name}' AND P.playerID = GS.playerID AND G.datePlayed BETWEEN '{season_year}-04-01' AND '{season_year}-10-31' AND GS.gameID = G.gameID")
        result = mycursor.fetchall()
        if result:
            print(f"\n{first_name} {last_name}'s batting average for the {season_year} season: {(result[0][0]):.3f}")
        else:
            print(f"\nNo data found for {first_name} {last_name} in the {season_year} season.")

    elif choice == "5":
        season_year = input("Enter season year (YYYY): ")
        team_name = input("Enter team name: ")
        mycursor = db.cursor()
        mycursor.execute(f"SELECT DISTINCT T.division, S.teamName, S.wins, S.losses FROM TEAM AS T, SEASON AS S WHERE T.division = (SELECT division FROM TEAM WHERE teamName = '{team_name}') AND S.seasonYear = '{season_year}' ORDER BY S.wins DESC")
        result = mycursor.fetchall()
        if result:
            print(f"\n{team_name} standings within the {result[0][0]} for the {season_year} season:")
            for row in result:
                print(f"Team: {row[1]}, Wins: {row[2]}, Losses: {row[3]}")
        else:
            print(f"\nNo data found for {team_name} or year.")

    #exit
    elif choice == "6":
        print("Exiting the program...")
        break