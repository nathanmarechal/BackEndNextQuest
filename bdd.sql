
#DROP DATABASE IF EXISTS NextQuest;

#CREATE DATABASE IF NOT EXISTS NextQuest;

USE NextQuest;

#DROP TABLE IF EXISTS perspectives_games;
#DROP TABLE IF EXISTS themes_games;
#DROP TABLE IF EXISTS game_modes_games;
#DROP TABLE IF EXISTS platforms_games;
#DROP TABLE IF EXISTS genres_games;
#DROP TABLE IF EXISTS review;
#DROP TABLE IF EXISTS games;
#DROP TABLE IF EXISTS developers;
#DROP TABLE IF EXISTS perspectives;
#DROP TABLE IF EXISTS themes;
#DROP TABLE IF EXISTS game_modes;
#DROP TABLE IF EXISTS platforms;
#DROP TABLE IF EXISTS genres;
#DROP TABLE IF EXISTS users;


CREATE TABLE users(
   id_user INT AUTO_INCREMENT,
   password VARCHAR(50),
   name_user VARCHAR(250) NOT NULL,
   age_user INT,
   email_user VARCHAR(250) NOT NULL,
   PRIMARY KEY(id_user)
);

CREATE TABLE genres(
   id_genre INT AUTO_INCREMENT,
   name_genre VARCHAR(500),
   PRIMARY KEY(id_genre)
);

CREATE TABLE platforms(
   id_platform INT AUTO_INCREMENT,
   nom_platform VARCHAR(500),
   PRIMARY KEY(id_platform)
);

CREATE TABLE game_modes(
   Id_Game_mode INT AUTO_INCREMENT,
   nom_game_mode VARCHAR(500),
   PRIMARY KEY(Id_Game_mode)
);

CREATE TABLE themes(
   id_theme INT AUTO_INCREMENT,
   nom_theme VARCHAR(500),
   PRIMARY KEY(id_theme)
);

CREATE TABLE perspectives(
   id_perspective INT AUTO_INCREMENT,
   nom_perspective VARCHAR(50),
   PRIMARY KEY(id_perspective)
);

CREATE TABLE developers(
   id_developer INT AUTO_INCREMENT,
   name_developer TEXT,
   PRIMARY KEY(id_developer)
);

CREATE TABLE games(
   app_id INT AUTO_INCREMENT,
   name VARCHAR(50),
   game_summary TEXT,
   storyline TEXT,
   cover_url TEXT,
   artwork_url TEXT,
   website TEXT,
   id_developer INT NOT NULL,
   PRIMARY KEY(app_id),
   FOREIGN KEY(id_developer) REFERENCES developers(id_developer)
);

CREATE TABLE review(
   id_user INT,
   app_id INT,
   review VARCHAR(200),
   review_score INT,
   PRIMARY KEY(id_user, app_id),
   FOREIGN KEY(id_user) REFERENCES users(id_user),
   FOREIGN KEY(app_id) REFERENCES games(app_id)
);

CREATE TABLE genres_games(
   app_id INT,
   id_genre INT,
   PRIMARY KEY(app_id, id_genre),
   FOREIGN KEY(app_id) REFERENCES games(app_id),
   FOREIGN KEY(id_genre) REFERENCES genres(id_genre)
);

CREATE TABLE platforms_games(
   app_id INT,
   id_platform INT,
   PRIMARY KEY(app_id, id_platform),
   FOREIGN KEY(app_id) REFERENCES games(app_id),
   FOREIGN KEY(id_platform) REFERENCES platforms(id_platform)
);

CREATE TABLE game_modes_games(
   app_id INT,
   Id_Game_mode INT,
   PRIMARY KEY(app_id, Id_Game_mode),
   FOREIGN KEY(app_id) REFERENCES games(app_id),
   FOREIGN KEY(Id_Game_mode) REFERENCES game_modes(Id_Game_mode)
);

CREATE TABLE themes_games(
   app_id INT,
   id_theme INT,
   PRIMARY KEY(app_id, id_theme),
   FOREIGN KEY(app_id) REFERENCES games(app_id),
   FOREIGN KEY(id_theme) REFERENCES themes(id_theme)
);

CREATE TABLE perspectives_games(
   app_id INT,
   id_perspective INT,
   PRIMARY KEY(app_id, id_perspective),
   FOREIGN KEY(app_id) REFERENCES games(app_id),
   FOREIGN KEY(id_perspective) REFERENCES perspectives(id_perspective)
);

SELECT * FROM users;

SELECT * FROM genres;

SELECT * FROM platforms;

SELECT * FROM game_modes;

SELECT * FROM themes;

SELECT * FROM perspectives;

SELECT * FROM developers;

SELECT * FROM games;

#ajouter une date a review
ALTER TABLE review ADD COLUMN date_review DATE;

#ajouter à toutes les reviews la date d'aujourd'hui
UPDATE review SET date_review = CURDATE();

#afficher les 10 premiers avis
SELECT * FROM review LIMIT 10;

SELECT * FROM users WHERE id_user = 1;

#ajouter isliked à review et lui attribuer la valeur de review_score
ALTER TABLE review ADD COLUMN isliked BOOLEAN;
UPDATE review SET isliked = CASE WHEN review_score >= 1 THEN TRUE ELSE FALSE END;

select * from review where isliked = 1;

SELECT * FROM games WHERE name LIKE '%Arma%';