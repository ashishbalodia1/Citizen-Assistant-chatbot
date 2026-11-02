-- Seed Data for City Guardian

INSERT INTO wards (id, ward_name, team_name) VALUES
(1, 'Ward 7 - Civil Lines', 'Holkar Heroes'),
(2, 'Ward 12 - Old City', 'Shivaji Squad'),
(3, 'Ward 4 - Metro West', 'Green Sentinels');

INSERT INTO users (id, name, phone, email, ward_id, role) VALUES
(1, 'Rahul Sharma', '9876543210', 'rahul.sharma@example.com', 1, 'CITIZEN'),
(2, 'Priya Verma', '9876543211', 'priya.verma@example.com', 1, 'CITIZEN'),
(3, 'Municipal Officer Gupta', '9876543212', 'officer.gupta@citygov.in', 1, 'MUNICIPAL_OFFICER');

INSERT INTO rewards (id, user_id, points, badge_level) VALUES
(1, 1, 180, 'Active Citizen'),
(2, 2, 75, 'New Guardian');

INSERT INTO coupons (id, business_name, offer, points_required, expiry_date, is_active) VALUES
(1, 'GreenLeaf Nursery', '25% Off on Plants & Garden Composts', 50, '2026-12-31 23:59:59', 1),
(2, 'Metro Smart Mobility', 'Free Day Pass on City Electric Buses', 100, '2026-11-30 23:59:59', 1),
(3, 'Cafe Chai & Co', 'Free Ginger Tea + Samosa with any combo', 40, '2026-12-15 23:59:59', 1),
(4, 'City Heritage Bookshop', '15% Off on Books & Stationery', 80, '2026-12-31 23:59:59', 1);

INSERT INTO complaints (id, user_id, category, description, latitude, longitude, address, image_path, severity, status) VALUES
(101, 1, 'drainage', 'Main drainage pipe leaking foul water onto street near market', 28.6139, 77.2090, 'Sector 4, Main Market, Ward 7', 'uploads/sample_drainage.jpg', 'HIGH', 'IN_PROGRESS'),
(102, 2, 'pothole', 'Deep pothole causing traffic jam near flyover pillar 14', 28.6145, 77.2100, 'Flyover Road, Pillar 14', 'uploads/sample_pothole.jpg', 'MEDIUM', 'APPROVED'),
(103, 1, 'garbage', 'Overflowing garbage bin near Central School corner', 28.6150, 77.2120, 'Central School Corner', 'uploads/sample_garbage.jpg', 'HIGH', 'PENDING_VERIFICATION');

INSERT INTO missions (id, complaint_id, ward_id, assigned_team, deadline, status) VALUES
(7042, 101, 1, 'Holkar Heroes', '2026-11-05 18:00:00', 'IN_PROGRESS'),
(7043, 102, 1, 'Shivaji Squad', '2026-11-04 12:00:00', 'ASSIGNED');

INSERT INTO mission_updates (id, mission_id, update_text, created_at) VALUES
(1, 7042, 'Maintenance team dispatched with suction pump truck.', '2026-11-01 10:30:00');

