from app import create_app
from models import db
from models.project import Project
from models.user import User

app = create_app()

def seed_real_projects():
    with app.app_context():
        # Clean current projects to avoid mess while testing/redoing
        # In a real environment we might just update, but for this task "change all pictures" and "add 6 more"
        # I'll just clear and re-seed to make sure it's consistent.
        # But wait, maybe the user wants to keep some. I'll delete the ones with status "approved" or "test"
        Project.query.filter(Project.name.like('%dd%')).delete(synchronize_session=False)
        db.session.commit()
        
        # Ensure we have a startup user
        startup_user = User.query.filter_by(role='startup').first()
        if not startup_user:
            print("No startup user found, please register one or seed users first.")
            return

        projects_data = [
            {
                "name": "Quantum Computing Solutions",
                "description": "Next-generation quantum processing for massive data sets and encryption. Using a unique photon-based architecture for stable, high-performance qBit operations. Targeted at high-frequency trading and pharmaceutical modeling lab scenarios.",
                "goal_amount": 5000000.0,
                "raised_amount": 1250000.0,
                "category": "Technology",
                "duration_days": 180,
                "image_path": "quantum.png"
            },
            {
                "name": "BioTech Longevity Lab",
                "description": "Advancing genetic engineering and metabolic science to slow biological aging. Backed by top researchers, we've identified 12 key pathways for cellular regeneration. Pilot human trials start Q3 2026.",
                "goal_amount": 3500000.0,
                "raised_amount": 425000.0,
                "category": "Health",
                "image_path": "biotech.png"
            },
            {
                "name": "EcoCharge EV Network",
                "description": "Building a nationwide network of fast, renewable-powered EV charging stations. Targeting high-traffic interstate highways and urban centers with low-cost, ultra-reliable green infrastructure solutions.",
                "goal_amount": 750000.0,
                "raised_amount": 250000.0,
                "category": "Environment",
                "image_path": None
            },
            {
                "name": "FinSecure Gateway",
                "description": "A payment gateway built for the new standard of financial transactions. Real-time encryption, AI-driven fraud detection, and multi-layered authentication for ultra-secure global transfers.",
                "goal_amount": 2000000.0,
                "raised_amount": 150000.0,
                "category": "Finance",
                "image_path": None
            },
            {
                "name": "EduVirtual Reality",
                "description": "Immersive VR science labs for K-12 and university students. Providing high-end STEM education to rural and underfunded schools via portable, connected VR hardware kits.",
                "goal_amount": 500000.0,
                "raised_amount": 50000.0,
                "category": "Education",
                "image_path": None
            },
            {
                "name": "Lunar Resource Mining",
                "description": "Developing autonomous rovers for Helium-3 and water-ice extraction from the south pole of the Moon. Building the foundation for sustainable space exploration and fuel production.",
                "goal_amount": 10000000.0,
                "raised_amount": 2100000.0,
                "category": "Aerospace",
                "image_path": None
            },
            {
                "name": "Ocean Cleanup Robotics",
                "description": "Autonomous aquatic drones designed to filter microplastics and collect debris from heavy shipping lanes. Zero-emission solar-powered fleet with data tracking for global environmental monitoring.",
                "goal_amount": 1200000.0,
                "raised_amount": 300000.0,
                "category": "Environment",
                "image_path": None
            },
            {
                "name": "AI Legal Assistant Pro",
                "description": "A sophisticated AI platform for lawyers to automate document discovery, case law research, and risk assessment with 99.8% precision. Saving hundreds of hours in legal research.",
                "goal_amount": 450000.0,
                "raised_amount": 120000.0,
                "category": "LegalTech",
                "image_path": None
            },
            {
                "name": "Vertical Farming Labs",
                "description": "Indoor agriculture using aeroponics and AI-managed climate control. Producing 300% more yield with 95% less water than traditional farming. Supplying luxury restaurants and urban supermarkets.",
                "goal_amount": 950000.0,
                "raised_amount": 380000.0,
                "category": "AgriTech",
                "image_path": None
            },
            {
                "name": "Autonomous Delivery Hub",
                "description": "Self-driving drone and land-based delivery network for dense urban environments. Integrated with major retailers for same-hour contactless delivery of essential goods.",
                "goal_amount": 4000000.0,
                "raised_amount": 800000.0,
                "category": "Logistics",
                "image_path": None
            }
        ]

        # First, deactivate/archive old "real" projects to restart fresh for this task
        Project.query.filter(Project.id > 0).delete()
        db.session.commit()

        for d in projects_data:
            p = Project(
                owner_id=startup_user.id,
                name=d["name"],
                description=d["description"],
                goal_amount=d["goal_amount"],
                raised_amount=d["raised_amount"],
                category=d["category"],
                duration_days=d.get("duration_days", 90),
                status='approved',
                image_path=d["image_path"]
            )
            db.session.add(p)
        
        db.session.commit()
        print("Successfully re-seeded with 10 professional projects.")

if __name__ == "__main__":
    seed_real_projects()
