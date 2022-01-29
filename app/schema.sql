DROP TABLE IF EXISTS booze;
DROP TABLE IF EXISTS boozeless;
DROP TABLE IF EXISTS ingredients;

CREATE TABLE booze (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT UNIQUE NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE boozeless (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT UNIQUE NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE ingredients (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT UNIQUE NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO booze (name) VALUES
  ('Whiskey'),
  ('Rum'),
  ('Vodka'),
  ('Cognac'),
  ('Vermouth'),
  ('Amaretto');

INSERT INTO boozeless (name) VALUES
  ('Vanilla Extract (Whiskey)'),
  ('Pineapple Juice (Rum)'),
  ('White Grape Juice (Vodka)'),
  ('Apricot Juice (Cognac)'),
  ('Apple Juice (Vermouth)'),
  ('Almond Extract (Amaretto)');

INSERT INTO ingredients (name) VALUES
  ('Club Soda'),
  ('Sprite'),
  ('Coke'),
  ('Sugar'),
  ('Lemon'),
  ('Egg');
