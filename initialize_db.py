from models import db, BioID, CommitteeMember, AppConfig
from flask_bcrypt import Bcrypt


def initialize_bioids():
    bioid_codes = [
        '1K3JTWHA05', '1PUQV970LA', '2BIB99Z54V', '2WYIM3QCK9', '30MY51J1CJ', 
        '340B1EOCMG', '49YFTUA96K', '4HTOAI9YKO', '6EBQ28A62V', '6X6I6TSUFG',
        '7DMPYAZAP2', '88V3GKIVSF', '8OLYIE2FRC', '9JSXWO4LGH', 'ABQYUQCQS2',
        'AT66BX2FXM', 'BPX8O0YB5L', 'BZW5WWDMUY', 'C7IFP4VWIL', 'CCU1D7QXDT',
        'CET8NUAE09', 'CG1I9SABLL', 'D05HPPQNJ4', 'DHKFIYHMAZ', 'E7D6YUPQ6J',
        'F3ATSRR5DQ', 'FH6260T08H', 'FINNMWJY0G', 'FPALKDEL5T', 'GOYWJVDA8A',
        'H5C98XCENC', 'JHDCXB62SA', 'K1YL8VA2HG', 'LZK7P0X0LQ', 'O0V55ENOT0',
        'O3WJFGR5WE', 'PD6XPNB80J', 'PGPVG5RF42', 'QJXQOUPTH9', 'QTLCWUS8NB',
        'RYU8VSS4N5', 'S22A588D75', 'SEIQTS1H16', 'TLFDFY7RDG', 'TTK74SYYAN',
        'V2JX0IC633', 'V30EPKZQI2', 'VQKBGSE3EA', 'X16V7LFHR2', 'Y4FC3F9ZGS'
    ]

    if not BioID.query.first():
        print("BioID table is empty. Initializing default values...")
        try:
            for code in bioid_codes:
                bioid = BioID(code=code, used=0)
                db.session.add(bioid)
            db.session.commit()
            print("BioID table populated successfully.")
        except Exception as e:
            print(f"Error initializing BioID table: {str(e)}")
            db.session.rollback()
    else:
        print("BioID table already initialized.")


def initialize_committee_members(bcrypt):
    member = {"email": "admin@petition.parliament.sr", "password": "2025%shangrila"}

    if not CommitteeMember.query.first():
        try:
            hashed_password = bcrypt.generate_password_hash(member["password"]).decode('utf-8')
            new_member = CommitteeMember(
            email=member["email"],
            password_hash=hashed_password,
            )

            db.session.add(new_member)
            db.session.commit()
        except Exception as e:
            print(f"Error initializing CommitteeMember table: {str(e)}")
            db.session.rollback()
    else:
        print("CommitteeMember table already initialized.")

def initialize_app_config():
    if not AppConfig.query.first():
        default_config = AppConfig(signature_threshold=100)
        db.session.add(default_config)
        db.session.commit()
    else:
        print("AppConfig table already initialized.")