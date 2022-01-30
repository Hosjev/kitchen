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
  ('7-Up'),
  ('Ale'),
  ('Angelica root'),
  ('Apple juice'),
  ('Berries'),
  ('Bitters'),
  ('Cantaloupe'),
  ('Carbonated water'),
  ('Chocolate'),
  ('Chocolate syrup'),
  ('Coca-cola'),
  ('Cocoa powder'),
  ('Coffee'),
  ('Cranberries'),
  ('Cranberry juice'),
  ('Egg'),
  ('Egg yolk'),
  ('Espresso'),
  ('Ginger'),
  ('Grape juice'),
  ('Grapefruit juice'),
  ('Grapes'),
  ('Heavy cream'),
  ('Kiwi'),
  ('Lemon'),
  ('Lemon juice'),
  ('Lemonade'),
  ('Lime'),
  ('Lime juice'),
  ('Mango'),
  ('Milk'),
  ('Orange'),
  ('Orange bitters'),
  ('Peach nectar'),
  ('Pineapple juice'),
  ('Sprite'),
  ('Strawberries'),
  ('Sugar'),
  ('Sugar syrup'),
  ('Tea'),
  ('Tomato juice'),
  ('Water'),
  ('Watermelon'),
  ('Yoghurt');
