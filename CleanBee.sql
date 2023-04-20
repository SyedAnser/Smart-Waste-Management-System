create database CleanBee;
use CleanBee;
create table Users(username varchar(250),email varchar(250),password varchar(250),Company varchar(250),CompanyCode int(50));
insert into Users Values('Mehak', 'mehak@gmail.com', 'blah', 'ABC', 123);
create table Companies(CompanyName varchar(250), CompanyCode int(50));
insert into Companies values('ABC', 123);
select * from Users;
alter table Companies add NumEmployees int(250);
SET SQL_SAFE_UPDATES=0;
UPDATE Companies 
SET NumEmployees = (
  SELECT COUNT(*) 
  FROM Users 
  WHERE Users.CompanyCode = Companies.CompanyCode
);

