import os
from sqlalchemy import create_engine, text

def fix_alembic():
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        print("No DATABASE_URL found.")
        return
        
    if db_url.startswith("postgres://"):
        db_url = db_url.replace("postgres://", "postgresql://", 1)
        
    try:
        engine = create_engine(db_url)
        with engine.connect() as conn:
            result = conn.execute(text("SELECT version_num FROM alembic_version")).fetchall()
            versions = [r[0] for r in result]
            print(f"Current alembic versions in DB: {versions}")
            
            if 'b03920682977' in versions and '5f55d59008c3' in versions:
                print("Found overlapping versions. Removing the older version 'b03920682977'.")
                conn.execute(text("DELETE FROM alembic_version WHERE version_num = 'b03920682977'"))
                conn.commit()
                print("Fixed alembic_version table.")
    except Exception as e:
        print(f"Error fixing alembic_version (this might be normal if table doesn't exist yet): {e}")

if __name__ == "__main__":
    fix_alembic()
