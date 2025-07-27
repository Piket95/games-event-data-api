import wuwa_codes
import database.database as db

def codesScraping():
    db.migrate()
    wuwa_codes.scrapeCodes()
    return


if __name__ == "__main__":
    codesScraping()