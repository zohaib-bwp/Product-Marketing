-- Use the database
USE product_marketing;

-- Create product_images table for multiple images
CREATE TABLE IF NOT EXISTS product_images (
    image_id INT AUTO_INCREMENT PRIMARY KEY,
    product_id INT NOT NULL,
    image_url VARCHAR(500) NOT NULL,
    is_primary BOOLEAN DEFAULT FALSE,
    sort_order INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (product_id) REFERENCES products(product_id) ON DELETE CASCADE,
    INDEX idx_product_images (product_id, is_primary)
);

-- Add region/country columns to users table
ALTER TABLE users 
ADD COLUMN IF NOT EXISTS country VARCHAR(100),
ADD COLUMN IF NOT EXISTS city VARCHAR(100),
ADD COLUMN IF NOT EXISTS zip_code VARCHAR(20),
ADD COLUMN IF NOT EXISTS region VARCHAR(100);

-- Add region/country columns to products table for region-based pricing
ALTER TABLE products 
ADD COLUMN IF NOT EXISTS base_price DECIMAL(10, 2),
ADD COLUMN IF NOT EXISTS region_pricing JSON;

-- Create product_region_pricing table for different region prices
CREATE TABLE IF NOT EXISTS product_region_pricing (
    pricing_id INT AUTO_INCREMENT PRIMARY KEY,
    product_id INT NOT NULL,
    region VARCHAR(100) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    currency VARCHAR(3) DEFAULT 'USD',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (product_id) REFERENCES products(product_id) ON DELETE CASCADE,
    UNIQUE KEY unique_product_region (product_id, region),
    INDEX idx_region (region)
);

-- Create user_profiles table for additional user details
CREATE TABLE IF NOT EXISTS user_profiles (
    profile_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    profile_picture VARCHAR(500),
    date_of_birth DATE,
    gender VARCHAR(20),
    occupation VARCHAR(100),
    company VARCHAR(100),
    website VARCHAR(200),
    social_media JSON,
    preferences JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    UNIQUE KEY unique_user_profile (user_id)
);

-- Insert sample regions
INSERT IGNORE INTO regions (region_name, currency, currency_symbol) VALUES
('USA', 'USD', '$'),
('Europe', 'EUR', '€'),
('UK', 'GBP', '£'),
('Canada', 'CAD', 'C$'),
('Australia', 'AUD', 'A$'),
('India', 'INR', '₹'),
('Pakistan', 'PKR', 'Rs'),
('UAE', 'AED', 'د.إ'),
('Singapore', 'SGD', 'S$'),
('Malaysia', 'MYR', 'RM');