CREATE TABLE "users" ("USERID"	INTEGER NOT NULL UNIQUE,"PHOTO"	TEXT NOT NULL UNIQUE,"NAME"	TEXT NOT NULL,"NATION"	TEXT NOT NULL,"DOB"	TEXT NOT NULL,"DNI"	TEXT UNIQUE,PRIMARY KEY("USERID" AUTOINCREMENT));
INSERT INTO users (PHOTO, NAME, NATION, DOB, DNI) VALUES 
('photo1.jpg', 'John Doe', 'USA', '1990-05-20', '123456789'),
('photo2.jpg', 'Jane Smith', 'Canada', '1985-09-15', '987654321'),
('photo3.jpg', 'David Lee', 'UK', '1982-03-10', '456789123'),
('photo4.jpg', 'Maria Garcia', 'Spain', '1995-11-02', '789123456'),
('photo5.jpg', 'Ahmed Khan', 'Pakistan', '1988-07-25', '654321987');