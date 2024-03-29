import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db


#get the current directory of the Python file 
current_directory = os.path.dirname(__file__)

#key's relative path (this should work on different computers)
json_file_path = os.path.join(current_directory, "second-chance-64b66-firebase-adminsdk-etkn4-2927af9e64.json")

#service account key
cred = credentials.Certificate(json_file_path)
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://second-chance-64b66-default-rtdb.firebaseio.com/'
})



def update_leaderboard(player_name, score): #add logic to check if score is better than user's previous score
    ref = db.reference('/leaderboard')
    ref.child(player_name).set(score)

def fetch_leaderboard(limit=10):
    ref = db.reference('/leaderboard')
    leaderboard = ref.get()

    if leaderboard:
        #convert the dictionary to a list of tuples (name, score). score will be changed to time in the future
        sorted_leaderboard = sorted(leaderboard.items(), key=lambda x: x[1])
        #limit entries, imagine a top 10 for now, but this is subject to change
        leaderboard = dict(sorted_leaderboard[-limit:])
    
    return leaderboard





#for testing purposes
update_leaderboard("Player5", 300)

#fetch and display the leaderboard
leaderboard = fetch_leaderboard()
if leaderboard:
    print("Leaderboard:")
    for i, (name, score) in enumerate(leaderboard.items(), start=1):
        print(f"{i}. {name}: {score}")

