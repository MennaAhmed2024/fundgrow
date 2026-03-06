import pymysql

def seed_sql():
    try:
        connection = pymysql.connect(
            host='localhost',
            user='root',
            password='',
            database='fundgrow',
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        with connection.cursor() as cursor:
            # 1. Ensure startup user exists
            cursor.execute("SELECT id FROM users WHERE role='startup' LIMIT 1")
            user = cursor.fetchone()
            if not user:
                from werkzeug.security import generate_password_hash
                pw = generate_password_hash('Startup@123')
                cursor.execute("INSERT INTO users (name, email, password_hash, role) VALUES ('Innovate Labs', 'startup@fundgrow.com', %s, 'startup')", (pw,))
                connection.commit()
                cursor.execute("SELECT id FROM users WHERE role='startup' LIMIT 1")
                user = cursor.fetchone()
            
            user_id = user['id']

            # 2. Clear all projects and dependencies
            cursor.execute("DELETE FROM transactions")
            cursor.execute("DELETE FROM investments")
            cursor.execute("DELETE FROM projects")
            connection.commit()

            # 3. Insert 10 projects
            projects = [
                ("Quantum Computing Solutions", "Next-generation quantum processing for massive data sets and encryption. Using a unique photon-based architecture for stable, high-performance qBit operations.", 5000000, 1250000, "Technology", "quantum.png"),
                ("BioTech Longevity Lab", "Advancing genetic engineering and metabolic science to slow biological aging. Backed by top researchers, identifying 12 key pathways for cellular regeneration.", 3500000, 425000, "Health", "biotech.png"),
                ("EcoCharge EV Network", "Building a nationwide network of fast, renewable-powered EV charging stations. Targeting urban centers with low-cost, ultra-reliable green infrastructure.", 750000, 250000, "Environment", "eco.png"),
                ("FinSecure Gateway", "A payment gateway built for the new standard of financial transactions. Real-time encryption, AI-driven fraud detection, and multi-layered authentication.", 2000000, 150000, "Finance", "fin.png"),
                ("EduVirtual Reality", "Immersive VR science labs for students worldwide. Providing high-end STEM education to rural and underfunded schools via portable hardware kits.", 500000, 50000, "Education", "edu.png"),
                ("HealthAI Diagnostics", "AI-powered diagnostic tool for early detection of rare diseases through automated blood work analysis and pattern recognition.", 1500000, 450000, "Health", "health.png"),
                ("Ocean Cleanup Robotics", "Autonomous aquatic drones filtering microplastics from heavy shipping lanes. Zero-emission solar-powered fleet with global data tracking.", 1200000, 300000, "Environment", None),
                ("AI Legal Assistant Pro", "AI platform for lawyers to automate document discovery and case law research with 99.8% precision. Saving hundreds of hours daily.", 450000, 120000, "LegalTech", None),
                ("Vertical Farming Labs", "Indoor agriculture using aeroponics and AI-managed climate control. Producing 300% more yield with 95% less water than traditional farming.", 950000, 380000, "AgriTech", None),
                ("Autonomous Delivery Hub", "Self-driving drone and land-based delivery network for dense urban environments. Contactless delivery of essential goods.", 4000000, 800000, "Logistics", None)
            ]

            for name, desc, goal, raised, cat, img in projects:
                cursor.execute("""
                    INSERT INTO projects (owner_id, name, description, goal_amount, raised_amount, category, duration_days, status, image_path)
                    VALUES (%s, %s, %s, %s, %s, %s, 90, 'approved', %s)
                """, (user_id, name, desc, goal, raised, cat, img))
            
            connection.commit()
            print("Successfully seeded 10 projects via SQL.")
            
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if 'connection' in locals():
            connection.close()

if __name__ == "__main__":
    seed_sql()
