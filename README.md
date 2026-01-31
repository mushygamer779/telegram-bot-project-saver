#Project Portfolio Telegram Bot

<img width="1368" height="733" alt="image" src="https://github.com/user-attachments/assets/a8650866-110c-4c45-ac8a-5350886c3c92" />

## Introduction
A Telegram bot designed to help developers and creators manage their portfolio of projects. 
This bot allows users to store project details, track development statuses, and list the technical skills used in each project.

### Functions and features 
Features:
  Project Management: Add, view, update, and delete projects from your personal portfolio.
  
  Skill Tracking: Associate specific technical skills (e.g., Python, SQL, API) with each project.
  
  Status Updates: Track the lifecycle of your projects from "In Design" to "Completed."
  
  Persistent Storage: Uses a SQLite database to ensure all your data is saved securely.
  
  Interactive UI: Uses Telegram's Reply Keyboards and Inline Keyboards for easy navigation.

Project Structure:
  main.py: The entry point of the application containing the bot's command handlers and user interaction logic.
  
  logic.py: Contains the DB_Manager class which handles all SQL queries and database operations.
  
  config.py: Stores sensitive configuration data like the Telegram Bot API Token and the database filename.

Database Schema:
  The bot utilizes a relational database with four main tables:
  
  projects: Stores core project information (name, description, URL, user ID).
  
  skills: A list of available technical skills.
  
  project_skills: A many-to-many relationship table linking projects to skills.
  
  status: Defines the various stages a project can be in.

Setup Instructions
  Install Dependencies: Make sure you have pyTelegramBotAPI installed:
  
  Bash
  pip install pyTelegramBotAPI
  Configuration: Open config.py and replace the placeholder TOKEN with your actual bot token from @BotFather.
  
  Initialize Database: The first time you run the project, the create_tables() and default_insert() methods in logic.py will set up your SQLite database file.

Run the Bot:

  Bash
  python main.py
  
Bot Commands
  /start - Welcome message and introduction.
  
  /info - List all available commands.
  
  /new_project - Start the step-by-step process to add a new project.
  
  /projects - View your list of saved projects.
  
  /update_projects - Modify information for an existing project.
  
  /skills - Link technical skills to a specific project.
  
  /delete - Remove a project from your portfolio.

Technologies Used:
  Python: Primary programming language.
  
  pyTelegramBotAPI: Library for interacting with the Telegram Bot API.
  
  SQLite3: Lightweight relational database for data storage.


