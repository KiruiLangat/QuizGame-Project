from flask import Flask, render_template, request , redirect, url_for
app = Flask(__name__)
import mysql.connector

# Function to establish a connection with the database
def database_connection():
    db_config = {
        "host": "localhost",
        "user": "root",
        "password": "groupnin3",
        "database": "quizgame",
    }
    return mysql.connector.connect(**db_config)

# Function to close the connection with the database
def close_connection(connection, cursor):
    if connection.is_connected():
        cursor.close()
        connection.close()
        print("Connection closed.")

# Route for the homepage
@app.route('/')
def index():
    return render_template('index.html')

# Route for the login page
@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']

        try:
            # Insert username into the database
            connection = database_connection()
            cursor = connection.cursor()

            inserting_query = "INSERT INTO user (Username) VALUES (%s)"
            cursor.execute(inserting_query, (username,))

            # Commit the transaction
            connection.commit()
        except mysql.connector.Error as e:
            print(f"Error: {e}")
            # Rollback the transaction in case of an error
            connection.rollback()
        finally:
            close_connection(connection, cursor)
        return redirect('/topics')
    
    return render_template ('login.html')

# Route for the topics page
@app.route('/topics')
def topics():
    return render_template ('topics.html')

# Route for the gameplay page
@app.route('/gameplay', methods=['GET', 'POST'])
def gameplay():
    if request.method == 'GET':
        selected_topic = request.args.get('topic')
        selected_difficulty = request.args.get('difficulty')

        try:
            connection = database_connection()
            cursor = connection.cursor()

            selected_topic = int(selected_topic)
            selected_difficulty = int(selected_difficulty)

            question_query = "SELECT questionID, question,Options, CorrectAnswer FROM questions WHERE topicID = %s AND difficultyID = %s"
            cursor.execute(question_query, (selected_topic, selected_difficulty))
            questions = cursor.fetchall() #fetch query results

        #commit the transaction
            connection.commit()
        except mysql.connector.Error as e:
                print(f"Error: {e}")
            # Rollback the transaction in case of an error
                connection.rollback()
        finally:
            close_connection(connection, cursor)
        return render_template ('gameplay.html',questions=questions)
    
    elif request.method == 'POST':
        user_answers = request.form.getlist('answers')

        # Calculate the score based on correct answers
        score = 0
        tries = 3

        for question, user_answer in zip(questions, user_answers):
            user_answer = user_answer.upper()
            if user_answer == question[3].upper():
                score += 10
            else:
                tries -= 1
                if tries == 0:
                    # Redirect to score.html when tries reach 0
                    return redirect(url_for('score', score=score))
      
        return render_template('gameplay.html', questions=questions, tries=tries, score=score)    

# Route for the scores page
@app.route('/scores')
def scores():
    score = request.args.get('score')
    tries = request.args.get('tries')
    if tries:
        tries = int(tries)
    else:
        tries = 0  # or some default value
    return render_template('scores.html', score=score, tries=int(tries))

# Run the application
if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5000, debug=True)