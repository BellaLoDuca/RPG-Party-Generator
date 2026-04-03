# RPG Party Generator --

# A Python and MySQL application that generates and grades RPG-style parties
# picked by the user using stat-based scoring, duplicate penalties, and
# additional role weighting.

# Includes:
# - Interactive GUI using Tkinter
# - Terminal-based version
# - Simulation engine with CVS export for analysis

---

## Demo Flow

# 1. User selects 1 of 3 candidates per role
# 2. System builds a 5-character party
# 3. Backend calculates weighted stat score x suitability multiplier x
# duplicate penalties
# 4. Final party score and rank is displayed to user

## Tech Stack

- **Python**
- **Tkinter**
- **MySQL** 
- **mysql-connector-python**
- **python-dotenv**
- **Excel**

## Setup Instructions

### 1. Clone the repository
### 2. Install dependencies
### 3. Configure env variables:
##       Create a .env file in the root directory:
#           DB_HOST=localhost
#           DB_USER=root
#           DB_PASSWORD=your_password
#           DB_NAME=mydb
### 4. Ensure MySQL database is correct and online
### 5. Run the application
##       GUI: python gui.py
##       Terminal: python main.py
##       Simulation with CSV export: python simulate.py

## Author
# Bella LoDuca
# Cybersecurity at UTSA