-- ##JOB_PORTAL_SYSTEM##

CREATE DATABASE JobPortal;
USE JobPortal;

CREATE TABLE Jobs (
    JobID INT AUTO_INCREMENT PRIMARY KEY,
    JobTitle VARCHAR(255),
    CompanyName VARCHAR(255),
    Location VARCHAR(255),
    Salary DECIMAL(10, 2),
    RequiredSkills TEXT,
    JobDescription TEXT
);

CREATE TABLE Candidates (
    CandidateID INT AUTO_INCREMENT PRIMARY KEY,
    FirstName VARCHAR(255),
    LastName VARCHAR(255),
    Email VARCHAR(255),
    PhoneNumber VARCHAR(20),
    Skills TEXT
);

CREATE TABLE Applications (
    ApplicationID INT AUTO_INCREMENT PRIMARY KEY,
    JobID INT,
    CandidateID INT,
    Status VARCHAR(50),
    FOREIGN KEY (JobID) REFERENCES Jobs(JobID),
    FOREIGN KEY (CandidateID) REFERENCES Candidates(CandidateID)
);

INSERT INTO Jobs (JobTitle, CompanyName, Location, Salary, RequiredSkills, JobDescription)
VALUES 
('Frontend Developer', 'WebSolutions', 'Los Angeles', 95000, 'HTML, CSS, JavaScript', 'Develop user interfaces for web applications.'),
('Backend Developer', 'CodeBase Inc.', 'Austin', 110000, 'Node.js, SQL, APIs', 'Build and maintain server-side logic.'),
('Data Scientist', 'InsightsPro', 'Chicago', 130000, 'Python, Machine Learning, SQL', 'Analyze data and develop predictive models.'),
('Project Manager', 'InnovateWorks', 'Seattle', 100000, 'Agile, Scrum, Communication', 'Manage project timelines and team coordination.'),
('DevOps Engineer', 'CloudNet', 'Denver', 115000, 'AWS, Docker, Jenkins', 'Maintain and automate CI/CD pipelines.');


INSERT INTO Candidates (FirstName, LastName, Email, PhoneNumber, Skills)
VALUES 
('Charlie', 'Brown', 'charlie.brown@example.com', '5551234567', 'HTML, CSS, JavaScript'),
('Diana', 'Prince', 'diana.prince@example.com', '5559876543', 'Python, Machine Learning, SQL'),
('Edward', 'Norton', 'edward.norton@example.com', '5556543210', 'AWS, Docker, Jenkins'),
('Fiona', 'Green', 'fiona.green@example.com', '5558765432', 'Agile, Scrum, Communication'),
('George', 'Clark', 'george.clark@example.com', '5554321098', 'Node.js, SQL, APIs');


INSERT INTO Applications (JobID, CandidateID, Status)
VALUES 
(1, 3, 'Pending'),
(2, 4, 'Pending'),
(3, 5, 'Pending'),
(4, 2, 'Pending'),
(5, 1, 'Pending');
