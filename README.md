# Wikiracing game
### Have you heard anything about the game where you have to get from one Wikipedia article to another(sometimes it's an article about Hitler) for the minimum number of transitions.
___
### What we do?
Technologies used: threading, beautifulsoup4, wikipedia, Postgres DB

We wrote a function that takes two article names as a parameter and returns a list of page names through which you 
can get to it, or an empty list if such a path could not be found.<p>
Conditions:
1. We are looking for articles only on the Ukrainian Wikipedia;<br>
2. Error handling and retry for requests should be provided;
3. We take only the first 200 links on each page;
4. We use database to save links on the article and title of the article;
5. The next time you run it, you need to use database connections so you don't make the same queries twice;

We store the received information about links from the page in the postgres database. 
We create a table where the entry is the name of the article. 
And we also create a second table where we describe the relationship between the article and the links on the page.
___
### How to start project?
1. pip install -r requerements.txt;
2. Create .env file and write to it enviroment variables:
	- DB_NAME
	- DB_USER
	- DB_PASSWORD
	- DB_HOST
	- DB_PORT	
3. Run 'docker-compose up -d' to make a container with Postgres DB;
4. Create database with the name like in env file;
5. Create WikiRacer;

