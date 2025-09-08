import wuwa_codes
import database.database as db  
from dotenv import load_dotenv

if __name__ == "__main__":
    load_dotenv()
    
    if not db.check_table_codes_existing():
        db.migrate()
    
    wuwa_codes.scrape_codes()