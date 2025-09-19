-- HOTELS ---------------------------------------------------------------------
DROP TABLE IF EXISTS hotels;
CREATE TABLE hotels (
  IDhotel INTEGER PRIMARY KEY,
  city TEXT NOT NULL,
  name TEXT NOT NULL,
  stars INTEGER,
  CONSTRAINT UQname_city UNIQUE (name, city)
);

-- CLIENTS --------------------------------------------------------------------
DROP TABLE IF EXISTS clients;
CREATE TABLE clients (
  IDclient INTEGER PRIMARY KEY,
  name TEXT NOT NULL,
  forename TEXT
);

-- ROOMS ----------------------------------------------------------------------
DROP TABLE IF EXISTS rooms;
CREATE TABLE rooms (
  IDroom INTEGER NOT NULL,
  IDhotel INTEGER NOT NULL,
  floor INTEGER,
  type TEXT,
  price REAL NOT NULL,
  CONSTRAINT PKroom PRIMARY KEY (IDroom, IDhotel),
  CONSTRAINT FKhotel FOREIGN KEY (IDhotel) REFERENCES hotels (IDhotel)
);

-- SELLINGS -------------------------------------------------------------------
DROP TABLE IF EXISTS sellings;
CREATE TABLE sellings (
  IDselling INTEGER PRIMARY KEY,
  IDclient INTEGER NOT NULL,
  IDhotel INTEGER NOT NULL,
  IDroom INTEGER NOT NULL,
  arrival DATE NOT NULL,
  departure DATE, -- NULL if unknown
  CONSTRAINT FKroom FOREIGN KEY (IDroom, IDhotel)
  REFERENCES rooms(IDroom, IDhotel),
  CONSTRAINT FKclient FOREIGN KEY (IDclient)
  REFERENCES clients(IDclient) ON DELETE CASCADE,
  CONSTRAINT FKhotel FOREIGN KEY (IDhotel)
  REFERENCES hotels(IDhotel) ON DELETE CASCADE ,
  CONSTRAINT CKdates CHECK (arrival < departure)
);

-- BOOKINGS -------------------------------------------------------------------
DROP TABLE IF EXISTS bookings;
CREATE TABLE bookings (
  IDbooking INTEGER PRIMARY KEY,
  IDclient INTEGER NOT NULL,
  IDhotel INTEGER NOT NULL,
  IDroom INTEGER NOT NULL,
  arrival DATE NOT NULL,
  departure DATE NOT NULL,
  CONSTRAINT FKroom FOREIGN KEY (IDroom, IDhotel)
  REFERENCES rooms(IDroom, IDhotel) ON DELETE CASCADE,
  CONSTRAINT FKclient FOREIGN KEY (IDclient)
  REFERENCES clients(IDclient) ON DELETE CASCADE,
  CONSTRAINT FKhotel FOREIGN KEY (IDhotel)
  REFERENCES hotels(IDhotel) ON DELETE CASCADE,
  CONSTRAINT CKdates CHECK (arrival < departure)
);

PRAGMA foreign_keys = ON; -- Activate FOREIGN KEY for all tables
