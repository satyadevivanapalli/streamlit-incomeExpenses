ALTER TABLE incomeExpenses
ALTER City SET DEFAULT 'Sandnes';


ALTER TABLE incomeExpenses
ADD comments varchar(255);


ALTER TABLE incomeExpenses
ADD Email varchar(255);
incomeExpenses


ALTER TABLE Persons
ADD DateOfBirth date;


create table savings (id int AUTOINCREMENT PRIMARY KEY);


CREATE TABLE Persons (
    PersonID int,
    LastName varchar(255),
    FirstName varchar(255),
    Address varchar(255),
    City varchar(255)
);


CREATE TABLE savings (
    id int NOT NULL AUTO_INCREMENT,
    user_id int,
    FOREIGN KEY (user_id) REFERENCES usersInfo(id),
    PRIMARY KEY (id)
);

FOREIGN KEY (PersonID) REFERENCES Persons(PersonID)


CREATE TABLE Orders (
    OrderID int NOT NULL,
    OrderNumber int NOT NULL,
    PersonID int,
    PRIMARY KEY (OrderID),
    CONSTRAINT FK_PersonOrder FOREIGN KEY (PersonID)
    REFERENCES Persons(PersonID)
);


CREATE TABLE savings (
    id int NOT NULL AUTO_INCREMENT,
    user_id int NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (user_id)
    REFERENCES usersInfo(id)
);
CREATE TABLE employees (
    id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE,
    hire_date DATE,
    salary FLOAT,
    department_id INT,
    FOREIGN KEY (department_id) REFERENCES departments(department_id)
);


CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    userName VARCHAR(500) NOT NULL,
    email  VARCHAR(500) NOT NULL UNIQUE,
    password VARCHAR(500) NOT NULL
);


CREATE TABLE savings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    salary int,
    other_income int,
    rent int,
    groceries int,
    other_expenses int,
    savings int,
    user_id int,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    month_year varchar(1000),
    comments varchar(1000), 
    FOREIGN KEY (user_id) REFERENCES users(id)
);


,
    UNIQUE(user_id,month_year)