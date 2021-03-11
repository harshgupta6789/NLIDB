CREATE TABLE Course (
  Courseid int PRIMARY KEY,
  CourseName varchar(255)
);

INSERT INTO Course VALUES
(1, 'English'),
(2, 'Hindi'),
(3, 'Maths'),
(4, 'Science'),
(5, 'Social Science'),
(6, 'History'),
(7, 'Geography'),
(8, 'Politics'),
(9, 'Marathi'),
(10, 'French'),
(11, 'Economics'),
(12, 'Accounts'),
(13, 'Computer'),
(14, 'IT'),
(15, 'ML'),
(16, 'NLP'),
(17, 'PT'),
(18, 'Life Skills'),
(19, 'Music'),
(20, 'Library');

CREATE TABLE Student (
  Studentid int PRIMARY KEY,
  Name varchar(255),
  Course varchar(255)
);

INSERT INTO Student VALUES
(1, 'Ram', 'NLP'),
(2, 'Shyam', 'NLP'),
(3, 'Geeta', 'NLP'),
(4, 'Seeta', 'NLP'),
(5, 'Kishan', 'NLP'),
(6, 'Shyam', 'English'),
(7, 'Geeta', 'English'),
(8, 'Seeta', 'Maths'),
(9, 'Kishan', 'Maths'),
(10, 'priya', 'NLP'),
(11, 'Tanya', 'NLP'),
(12, 'Priyanka', 'NLP'),
(13, 'rahul', 'NLP'),
(14, 'Abhishek', 'ML'),
(15, 'Aditya', 'ML'),
(16, 'divya', 'ML'),
(17, 'Amit', 'Hindi'),
(18, 'tanvi', 'Hindi'),
(19, 'mahesh', 'Science'),
(20, 'Ishita', 'Science'),
(21, 'ROHIT', 'Science'),
(22, 'vani', 'History'),
(23, 'yash', 'History'),
(24, 'Anjali', 'History'),
(25, 'Ankit', 'Geography'),
(26, 'Shreya', 'Geography'),
(27, 'shyam', 'PT'),
(28, 'riya', 'PT'),
(29, 'Deepak', 'Politics'),
(30, 'Sneha', 'Politics'),
(31, 'Aryan', 'IT'),
(32, 'Aishwarya', 'IT'),
(33, 'Raj', 'Computer'),
(34, 'Gayatri', 'Accounts');