CREATE DATABASE waitless_aadhaar;
USE waitless_aadhaar;

CREATE TABLE applicants (
    id INT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    dob DATE NOT NULL,
    gender ENUM('Male','Female','Other') NOT NULL,
    mobile VARCHAR(10) UNIQUE NOT NULL,
    email VARCHAR(100),
    address TEXT NOT NULL,
    pincode VARCHAR(6) NOT NULL,
    latitude DECIMAL(10,8),
    longitude DECIMAL(11,8),
    document_type VARCHAR(50),
    application_type ENUM('New','Update','Reprint') DEFAULT 'New',
    status ENUM('Pending','Scheduled','Completed','Cancelled') DEFAULT 'Pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE biometric_centers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(150) NOT NULL,
    address TEXT NOT NULL,
    pincode VARCHAR(6),
    latitude DECIMAL(10,8) NOT NULL,
    longitude DECIMAL(11,8) NOT NULL,
    capacity_per_day INT DEFAULT 50,
    current_load INT DEFAULT 0,
    is_active BOOLEAN DEFAULT TRUE
);

CREATE TABLE appointments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    applicant_id INT NOT NULL,
    center_id INT NOT NULL,
    slot_date DATE NOT NULL,
    slot_time TIME NOT NULL,
    token_number VARCHAR(20) UNIQUE NOT NULL,
    status ENUM('Booked','Completed','Cancelled') DEFAULT 'Booked',
    FOREIGN KEY (applicant_id) REFERENCES applicants(id),
    FOREIGN KEY (center_id) REFERENCES biometric_centers(id)
);

-- Sample centers (add real coordinates for your city)
INSERT INTO biometric_centers (name, address, pincode, latitude, longitude, capacity_per_day) VALUES
('Aadhaar Seva Kendra - MG Road', 'MG Road, Bengaluru', '560001', 12.9716, 77.5946, 60),
('Aadhaar Center - Whitefield', 'Whitefield, Bengaluru', '560066', 12.9698, 77.7500, 40),
('Aadhaar Center - Jayanagar', 'Jayanagar, Bengaluru', '560041', 12.9259, 77.5937, 50);
