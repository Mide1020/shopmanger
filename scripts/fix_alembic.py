import os
from sqlalchemy import create_engine, text, inspect

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
            
            # Check if users table actually has the new columns using raw SQL on the SAME connection
            result_cols = conn.execute(text("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name='users' AND column_name='deleted_at'
            """)).fetchall()
            
            if not result_cols:
                print("Missing 'deleted_at' column! Resetting alembic_version to force migration b03920682977 to run.")
                conn.execute(text("DELETE FROM alembic_version"))
                conn.execute(text("INSERT INTO alembic_version (version_num) VALUES ('9569a32a391c')"))
                conn.commit()
                print("Reset successful.")
                return
            
            if 'b03920682977' in versions and '5f55d59008c3' in versions:
                print("Found overlapping versions. Removing the older version 'b03920682977'.")
                conn.execute(text("DELETE FROM alembic_version WHERE version_num = 'b03920682977'"))
                conn.commit()
                print("Fixed alembic_version table.")
    except Exception as e:
        print(f"Error fixing alembic_version (this might be normal if table doesn't exist yet): {e}")

if __name__ == "__main__":
    fix_alembic()
