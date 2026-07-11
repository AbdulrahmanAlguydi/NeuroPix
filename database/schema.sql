-- Reset database for development environment
DROP DATABASE IF EXISTS neuropix_db;
CREATE DATABASE neuropix_db;
USE neuropix_db;

-- 1. Users Table
CREATE TABLE Users (
    UserID INT AUTO_INCREMENT PRIMARY KEY,
    Username VARCHAR(50) NOT NULL UNIQUE,
    PasswordHash VARCHAR(255) NOT NULL,
    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_username (Username) -- Speeds up authentication lookups by avoiding full-table scans
);

-- 2. Images Table
CREATE TABLE Images (
    ImageID INT AUTO_INCREMENT PRIMARY KEY,
    UserID INT NOT NULL,
    OriginalFilePath VARCHAR(512) NOT NULL,
    ModifiedFilePath VARCHAR(512) NULL,
    EditType ENUM('standard', 'ai') NULL, -- Restricts values to standard or ai to enforce strict data integrity
    UploadDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
    CONSTRAINT fk_image_user FOREIGN KEY (UserID) -- Links image to user; cascading delete automatically removes user's images if account is deleted
        REFERENCES Users(UserID) 
        ON DELETE CASCADE
);