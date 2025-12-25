-- JALA Academy - SQL Assignments
-- ==============================

-- Create sample database and tables for demonstrating SQL queries
CREATE DATABASE IF NOT EXISTS jala_academy;
USE jala_academy;

-- Create Students table
CREATE TABLE Students (
    StudentID INT PRIMARY KEY AUTO_INCREMENT,
    FirstName VARCHAR(50) NOT NULL,
    LastName VARCHAR(50) NOT NULL,
    Email VARCHAR(100) UNIQUE,
    Age INT CHECK (Age >= 16 AND Age <= 60),
    EnrollmentDate DATE,
    Course VARCHAR(50),
    Grade VARCHAR(2)
);

-- Create Courses table
CREATE TABLE Courses (
    CourseID INT PRIMARY KEY AUTO_INCREMENT,
    CourseName VARCHAR(100) NOT NULL,
    Instructor VARCHAR(100),
    Credits INT,
    Department VARCHAR(50)
);

-- Create Enrollments table
CREATE TABLE Enrollments (
    EnrollmentID INT PRIMARY KEY AUTO_INCREMENT,
    StudentID INT,
    CourseID INT,
    EnrollmentDate DATE,
    Grade VARCHAR(2),
    FOREIGN KEY (StudentID) REFERENCES Students(StudentID),
    FOREIGN KEY (CourseID) REFERENCES Courses(CourseID)
);

-- Insert sample data into Students table
INSERT INTO Students (FirstName, LastName, Email, Age, EnrollmentDate, Course, Grade) VALUES
('John', 'Doe', 'john.doe@email.com', 20, '2023-08-15', 'Computer Science', 'A'),
('Jane', 'Smith', 'jane.smith@email.com', 19, '2023-08-15', 'Mathematics', 'B+'),
('Robert', 'Johnson', 'robert.johnson@email.com', 21, '2023-08-16', 'Physics', 'A-'),
('Emily', 'Williams', 'emily.williams@email.com', 20, '2023-08-16', 'Chemistry', 'B'),
('Michael', 'Brown', 'michael.brown@email.com', 22, '2023-08-17', 'Biology', 'A'),
('Sarah', 'Davis', 'sarah.davis@email.com', 19, '2023-08-17', 'History', 'B+'),
('David', 'Miller', 'david.miller@email.com', 21, '2023-08-18', 'English', 'A-'),
('Lisa', 'Wilson', 'lisa.wilson@email.com', 20, '2023-08-18', 'Computer Science', 'A+'),
('James', 'Moore', 'james.moore@email.com', 23, '2023-08-19', 'Mathematics', 'B'),
('Jennifer', 'Taylor', 'jennifer.taylor@email.com', 20, '2023-08-19', 'Physics', 'A');

-- Insert sample data into Courses table
INSERT INTO Courses (CourseName, Instructor, Credits, Department) VALUES
('Introduction to Programming', 'Dr. Smith', 3, 'Computer Science'),
('Calculus I', 'Prof. Johnson', 4, 'Mathematics'),
('General Physics I', 'Dr. Williams', 4, 'Physics'),
('General Chemistry I', 'Prof. Brown', 4, 'Chemistry'),
('Biology I', 'Dr. Davis', 3, 'Biology'),
('World History', 'Prof. Miller', 3, 'History'),
('English Composition', 'Dr. Wilson', 3, 'English'),
('Data Structures', 'Prof. Taylor', 3, 'Computer Science'),
('Linear Algebra', 'Dr. Anderson', 3, 'Mathematics'),
('Organic Chemistry', 'Prof. Thomas', 4, 'Chemistry');

-- Insert sample data into Enrollments table
INSERT INTO Enrollments (StudentID, CourseID, EnrollmentDate, Grade) VALUES
(1, 1, '2023-08-15', 'A'),
(1, 8, '2023-08-16', 'A-'),
(2, 2, '2023-08-15', 'B+'),
(2, 9, '2023-08-16', 'B'),
(3, 3, '2023-08-16', 'A-'),
(4, 4, '2023-08-16', 'B'),
(5, 5, '2023-08-17', 'A'),
(6, 6, '2023-08-17', 'B+'),
(7, 7, '2023-08-18', 'A-'),
(8, 1, '2023-08-18', 'A+'),
(8, 8, '2023-08-19', 'A'),
(9, 2, '2023-08-19', 'B'),
(9, 9, '2023-08-20', 'B+'),
(10, 3, '2023-08-19', 'A');

-- SQL QUERIES FOR ASSIGNMENTS
-- ===========================

-- 1. Basic SELECT queries
-- Retrieve all students
SELECT * FROM Students;

-- Retrieve specific columns
SELECT FirstName, LastName, Email FROM Students;

-- 2. Filtering with WHERE clause
-- Students older than 20
SELECT * FROM Students WHERE Age > 20;

-- Students in Computer Science course
SELECT * FROM Students WHERE Course = 'Computer Science';

-- 3. Sorting with ORDER BY
-- Students sorted by age (ascending)
SELECT * FROM Students ORDER BY Age ASC;

-- Students sorted by grade (descending)
SELECT * FROM Students ORDER BY Grade DESC;

-- 4. Aggregate functions
-- Count total number of students
SELECT COUNT(*) AS TotalStudents FROM Students;

-- Average age of students
SELECT AVG(Age) AS AverageAge FROM Students;

-- Maximum and minimum age
SELECT MAX(Age) AS MaxAge, MIN(Age) AS MinAge FROM Students;

-- 5. Grouping with GROUP BY
-- Count students by course
SELECT Course, COUNT(*) AS StudentCount 
FROM Students 
GROUP BY Course;

-- Average age by course
SELECT Course, AVG(Age) AS AverageAge 
FROM Students 
GROUP BY Course;

-- 6. JOIN operations
-- Get student names with their enrolled courses
SELECT s.FirstName, s.LastName, c.CourseName, e.Grade
FROM Students s
JOIN Enrollments e ON s.StudentID = e.StudentID
JOIN Courses c ON e.CourseID = c.CourseID;

-- Get all students and their courses (including those not enrolled)
SELECT s.FirstName, s.LastName, c.CourseName
FROM Students s
LEFT JOIN Enrollments e ON s.StudentID = e.StudentID
LEFT JOIN Courses c ON e.CourseID = c.CourseID;

-- 7. Subqueries
-- Students with grades higher than average
SELECT FirstName, LastName, Grade
FROM Students
WHERE Grade IN ('A', 'A+', 'A-');

-- Students enrolled in specific courses
SELECT s.FirstName, s.LastName
FROM Students s
WHERE s.StudentID IN (
    SELECT e.StudentID 
    FROM Enrollments e
    JOIN Courses c ON e.CourseID = c.CourseID
    WHERE c.CourseName = 'Introduction to Programming'
);

-- 8. Advanced queries
-- Students with their enrollment count
SELECT s.FirstName, s.LastName, COUNT(e.EnrollmentID) AS EnrollmentCount
FROM Students s
LEFT JOIN Enrollments e ON s.StudentID = e.StudentID
GROUP BY s.StudentID, s.FirstName, s.LastName;

-- Top 3 students by grade (assuming A+ is highest, then A, etc.)
SELECT FirstName, LastName, Grade
FROM Students
ORDER BY 
    CASE Grade
        WHEN 'A+' THEN 1
        WHEN 'A' THEN 2
        WHEN 'A-' THEN 3
        WHEN 'B+' THEN 4
        WHEN 'B' THEN 5
        ELSE 6
    END
LIMIT 3;

-- 9. UPDATE operations
-- Update a student's grade
UPDATE Students
SET Grade = 'A+'
WHERE FirstName = 'John' AND LastName = 'Doe';

-- 10. DELETE operations
-- Delete an enrollment (example - not actually executing for safety)
-- DELETE FROM Enrollments WHERE EnrollmentID = 1;

-- 11. INSERT operations
-- Add a new student
INSERT INTO Students (FirstName, LastName, Email, Age, EnrollmentDate, Course, Grade)
VALUES ('New', 'Student', 'new.student@email.com', 20, '2023-09-01', 'Computer Science', 'B+');

-- 12. Creating indexes for performance
-- Create index on frequently searched columns
CREATE INDEX idx_student_email ON Students(Email);
CREATE INDEX idx_student_course ON Students(Course);

-- 13. Views for simplified access
-- Create a view for student grades
CREATE VIEW StudentGrades AS
SELECT s.FirstName, s.LastName, s.Course, e.Grade, c.CourseName
FROM Students s
JOIN Enrollments e ON s.StudentID = e.StudentID
JOIN Courses c ON e.CourseID = c.CourseID;

-- Query the view
SELECT * FROM StudentGrades;

-- 14. Transactions for data integrity
-- Example transaction (not executed to avoid conflicts)
/*
START TRANSACTION;
INSERT INTO Students (FirstName, LastName, Email, Age, EnrollmentDate, Course, Grade)
VALUES ('Transaction', 'Test', 'transaction.test@email.com', 22, '2023-09-01', 'Mathematics', 'B');
INSERT INTO Enrollments (StudentID, CourseID, EnrollmentDate, Grade)
VALUES (LAST_INSERT_ID(), 2, '2023-09-01', 'B');
COMMIT;
*/

-- 15. Complex query combining multiple concepts
-- Get students with their courses, grades, and instructor names
SELECT 
    s.FirstName,
    s.LastName,
    c.CourseName,
    c.Instructor,
    e.Grade AS EnrollmentGrade,
    s.Grade AS OverallGrade
FROM Students s
JOIN Enrollments e ON s.StudentID = e.StudentID
JOIN Courses c ON e.CourseID = c.CourseID
ORDER BY s.LastName, c.CourseName;

-- 16. Using HAVING clause with GROUP BY
-- Find courses with more than 2 enrolled students
SELECT c.CourseName, COUNT(e.StudentID) AS StudentCount
FROM Courses c
JOIN Enrollments e ON c.CourseID = e.CourseID
GROUP BY c.CourseID, c.CourseName
HAVING COUNT(e.StudentID) > 2;

-- 17. Using CASE statement
-- Categorize students based on their grades
SELECT 
    FirstName,
    LastName,
    Grade,
    CASE 
        WHEN Grade IN ('A+', 'A', 'A-') THEN 'Excellent'
        WHEN Grade IN ('B+', 'B') THEN 'Good'
        WHEN Grade = 'B-' THEN 'Average'
        ELSE 'Needs Improvement'
    END AS PerformanceCategory
FROM Students;

-- 18. Date functions
-- Find students enrolled in the last 30 days (relative to a reference date)
SELECT FirstName, LastName, EnrollmentDate
FROM Students
WHERE DATEDIFF('2023-09-15', EnrollmentDate) <= 30;

-- 19. String functions
-- Get students with email domains
SELECT 
    FirstName,
    LastName,
    Email,
    SUBSTRING(Email, LOCATE('@', Email) + 1) AS EmailDomain
FROM Students;

-- 20. Window functions (if supported by your database)
-- Rank students by grade within each course
SELECT 
    FirstName,
    LastName,
    Course,
    Grade,
    ROW_NUMBER() OVER (PARTITION BY Course ORDER BY 
        CASE Grade
            WHEN 'A+' THEN 1
            WHEN 'A' THEN 2
            WHEN 'A-' THEN 3
            WHEN 'B+' THEN 4
            WHEN 'B' THEN 5
            ELSE 6
        END
    ) AS RankInCourse
FROM Students;

-- Clean up (commented out to preserve data)
-- DROP VIEW IF EXISTS StudentGrades;
-- DROP TABLE IF EXISTS Enrollments;
-- DROP TABLE IF EXISTS Students;
-- DROP TABLE IF EXISTS Courses;
-- DROP DATABASE IF EXISTS jala_academy;