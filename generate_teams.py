import os
import pandas as pd
import numpy as np

os.makedirs("data", exist_ok=True)

teams = {
    "rcb": ["Virat Kohli", "Faf du Plessis", "Glenn Maxwell", "Rajat Patidar", "Cameron Green", "Dinesh Karthik", "Mahipal Lomror", "Mohammed Siraj", "Lockie Ferguson", "Yash Dayal", "Karn Sharma"],
    "csk": ["Ruturaj Gaikwad", "Rachin Ravindra", "Ajinkya Rahane", "Shivam Dube", "Daryl Mitchell", "Ravindra Jadeja", "MS Dhoni", "Deepak Chahar", "Shardul Thakur", "Matheesha Pathirana", "Mustafizur Rahman"],
    "mi": ["Rohit Sharma", "Ishan Kishan", "Suryakumar Yadav", "Hardik Pandya", "Tilak Varma", "Tim David", "Romario Shepherd", "Mohammad Nabi", "Piyush Chawla", "Jasprit Bumrah", "Gerald Coetzee"],
    "gt": ["Shubman Gill", "Sai Sudharsan", "Kane Williamson", "David Miller", "Vijay Shankar", "Rahul Tewatia", "Rashid Khan", "Nurul Hasan", "Mohit Sharma", "Umesh Yadav", "Spencer Johnson"],
    "rr": ["Yashasvi Jaiswal", "Jos Buttler", "Sanju Samson", "Riyan Parag", "Shimron Hetmyer", "Dhruv Jurel", "Ravi Ashwin", "Trent Boult", "Avesh Khan", "Yuzvendra Chahal", "Sandeep Sharma"],
    "kkr": ["Phil Salt", "Sunil Narine", "Venkatesh Iyer", "Shreyas Iyer", "Rinku Singh", "Andre Russell", "Ramandeep Singh", "Mitchell Starc", "Harshit Rana", "Varun Chakaravarthy", "Vaibhav Arora"],
    "srh": ["Travis Head", "Abhishek Sharma", "Aiden Markram", "Heinrich Klaasen", "Nitish Reddy", "Abdul Samad", "Shahbaz Ahmed", "Pat Cummins", "Bhuvneshwar Kumar", "T Natarajan", "Mayank Markande"],
    "dc": ["David Warner", "Prithvi Shaw", "Mitchell Marsh", "Rishabh Pant", "Tristan Stubbs", "Axar Patel", "Lalit Yadav", "Kuldeep Yadav", "Anrich Nortje", "Khaleel Ahmed", "Mukesh Kumar"],
    "lsg": ["KL Rahul", "Quinton de Kock", "Devdutt Padikkal", "Marcus Stoinis", "Nicholas Pooran", "Ayush Badoni", "Krunal Pandya", "Ravi Bishnoi", "Naveen-ul-Haq", "Mohsin Khan", "Yash Thakur"],
    "pbks": ["Shikhar Dhawan", "Jonny Bairstow", "Prabhsimran Singh", "Sam Curran", "Liam Livingstone", "Jitesh Sharma", "Shashank Singh", "Harpreet Brar", "Kagiso Rabada", "Arshdeep Singh", "Harshal Patel"]
}

roles = ["batsman", "batsman", "batsman", "batsman", "allrounder", "batsman", "allrounder", "bowler", "bowler", "bowler", "bowler"]

for team, players in teams.items():
    data = []
    for i, name in enumerate(players):
        role = roles[i]
        
        # Generator boundaries
        if role == 'batsman':
            sr = np.random.randint(125, 170)
            avg = np.random.randint(25, 55)
            wickets = 0
            econ = 0
        elif role == 'bowler':
            sr = np.random.randint(0, 50)
            avg = np.random.randint(0, 15)
            wickets = np.random.randint(10, 25)
            econ = round(np.random.uniform(6.5, 9.5), 2)
        else:
            sr = np.random.randint(120, 160)
            avg = np.random.randint(20, 35)
            wickets = np.random.randint(5, 15)
            econ = round(np.random.uniform(7.0, 9.0), 2)
            
        recent_form = np.random.randint(45, 96) 
        
        # Hardcode some stars for "Clutch" verification
        if name in ["Virat Kohli", "Suryakumar Yadav", "Ruturaj Gaikwad", "Travis Head"]: recent_form = 95; avg = 55
        if name in ["Jasprit Bumrah", "Rashid Khan", "Trent Boult"]: econ = 6.2; recent_form = 92
        if name in ["Mahipal Lomror", "Lalit Yadav"]: recent_form = 45 # Induce pressure score
            
        data.append({
            'player_name': name,
            'role': role,
            'strike_rate': sr,
            'average': avg,
            'wickets': wickets,
            'economy': econ,
            'recent_form': recent_form
        })
        
    df = pd.DataFrame(data)
    df.to_csv(f"data/{team}_2026.csv", index=False)

print("10 team datasets generated in /data!")
