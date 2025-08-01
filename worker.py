import wuwa_codes
import database.database as db  
from dotenv import load_dotenv

if __name__ == "__main__":
    load_dotenv()
    
    db.migrate()
    wuwa_codes.scrapeCodes()