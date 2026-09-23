-- Update admin schema for profile management
USE product_marketing;

-- Add new columns to users table for enhanced profile
ALTER TABLE users 
ADD COLUMN IF NOT EXISTS profile_picture VARCHAR(255) DEFAULT NULL,
ADD COLUMN IF NOT EXISTS bio TEXT,
ADD COLUMN IF NOT EXISTS last_login TIMESTAMP NULL,
ADD COLUMN IF NOT EXISTS last_login_ip VARCHAR(45),
ADD COLUMN IF NOT EXISTS is_active BOOLEAN DEFAULT TRUE,
ADD COLUMN IF NOT EXISTS preferences JSON;

-- Create admin_activity_log table for tracking admin actions
CREATE TABLE IF NOT EXISTS admin_activity_log (
    log_id INT AUTO_INCREMENT PRIMARY KEY,
    admin_id INT NOT NULL,
    action VARCHAR(100) NOT NULL,
    details TEXT,
    ip_address VARCHAR(45),
    user_agent TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (admin_id) REFERENCES users(user_id) ON DELETE CASCADE,
    INDEX idx_admin_actions (admin_id, created_at)
);

-- Create system_settings table for admin configuration
CREATE TABLE IF NOT EXISTS system_settings (
    setting_id INT AUTO_INCREMENT PRIMARY KEY,
    setting_key VARCHAR(100) UNIQUE NOT NULL,
    setting_value TEXT,
    setting_type VARCHAR(50) DEFAULT 'text',
    description TEXT,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Insert default system settings
INSERT IGNORE INTO system_settings (setting_key, setting_value, setting_type, description) VALUES
('site_name', 'Product Marketing System', 'text', 'Website name'),
('site_description', 'Your one-stop shop for amazing products', 'textarea', 'Site description for SEO'),
('contact_email', 'admin@example.com', 'email', 'Main contact email'),
('items_per_page', '12', 'number', 'Products per page'),
('maintenance_mode', '0', 'boolean', 'Enable maintenance mode'),
('currency_symbol', '$', 'text', 'Currency symbol'),
('currency_code', 'USD', 'text', 'Currency code');

-- Update existing admin user to have admin role
UPDATE users SET role = 'admin' WHERE email = 'admin@example.com';