import mysql.connector

def play_game():
    #Start: Connect to database
    db_config = {
        "host": "localhost",
        "user": "root",
        "password": "groupnin3",
        "database": "quizgame",
    }

    try:
        # Establishing a connection
        connection = mysql.connector.connect(**db_config)

        if connection.is_connected():
            print("Connected to MySQL server!")

            # Begining of database query connection
            cursor = connection.cursor()

            # step 1: Get user input
            username = input("Enter your Username: ")
            print("\nWELCOME", username)
            #query to store username
            Inserting_query = ("INSERT INTO user (username) VALUES (%s)")
            cursor.execute(Inserting_query, (username,))

            #Step 3: Select topic Name from topics
            topic_query = "SELECT topicID, topicName FROM topics"
            cursor.execute(topic_query)
            topics = cursor.fetchall() #fetch topics from the database

            print("\nPick a topic:")
            for topicname in topics:
                print(f"{topicname[0]}. {topicname[1]}")

            
            # Error Handling to make sure the user enters the numbers specified for topics
            while True:
                try:
                    selected_topic = int(input("\nEnter the topic number: "))
                    if 1 <= selected_topic <= len(topics):
                        break
                    else:
                        print("Invalid input. Please enter a numeric value within the specified range.")
                except ValueError:
                    print("Invalid input. Please enter a numeric value for the topic.")
                    print("\n")

            #Step 4: To select difficulty level
            difficulty_query = "SELECT difficultyID, level FROM difficulty"
            cursor.execute(difficulty_query)
            difficulty = cursor.fetchall()

            print("\nPick a difficulty level:")
            for level in difficulty:
                print(f"{level[0]}. {level[1]}")

            # Error Handling to make sure the user enters the numbers specified for difficulty
            while True:
                try:
                    selected_difficulty = int(input("Enter the difficulty number: "))
                    if 1 <= selected_difficulty <= len(difficulty):
                        break
                    else:
                        print("Invalid input. Please enter a numeric value within the specified range.")
                except ValueError:
                    print("Invalid input. Please enter a numeric value for the difficulty.")
                    print("\n")

            #Step 5: Fetch and display questions for the selected difficulty and topic
            question_query = "SELECT questionID, question,Options, CorrectAnswer FROM questions WHERE topicID = %s AND difficultyID = %s"
            cursor.execute(question_query, (selected_topic, selected_difficulty))
            questions = cursor.fetchall()

            print("\nLET THE GAMES BEGIN\n")
            score = 0
            tries_left = 3

            for question in questions:
                print(question[1])  # prints the question
                Options = question[2].split(" ")  # splits the option string into a list
                for Option in Options:
                    print(Option)
                       
                #Error handling for choice answers
                while True:
                    user_answer = input("Your Answer is: ").upper()

                    if user_answer in {'A','B','C','D'}:
                        break
                    else:
                        print("Invalid Choice. Please enter the valid options (A B C D)!")

                
                if user_answer.upper() == question[3].upper():  # converts both answers to uppercase
                    print("Correct!\n")
                    score += 10
                else:
                    print("Incorrect")
                    tries_left -= 1
                    print(f"{tries_left} chance(s) left. \n")

                    if tries_left == 0:
                        print("Game Over!",username.upper())
                        break

            # Check if the user wants to restart
            restart_game = input("Do you want to restart the game? (yes/no): ").lower()
            if restart_game == "yes":
                play_game()  # Call the function to restart the game
            else:
                print("\nYour score is: ", score, "\n")

            connection.commit()
            # Close the cursor and connection when done
            cursor.close()

    except mysql.connector.Error as e:
        print(f"Error: {e}")

    finally:
        if connection.is_connected():
            connection.close()
            print("Connection closed.")

# Call the function to start the game
play_game()
