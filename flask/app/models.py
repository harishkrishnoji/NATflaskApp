from app import db

class nat(db.Model):
    # id = db.Column(db.String(), primary_key=True)
    Firewall = db.Column(db.String())
    FirewallName = db.Column(db.String())
    Name = db.Column(db.String(), primary_key=True)
    OriginalDestination = db.Column(db.String())
    OriginalSource = db.Column(db.String())
    Method = db.Column(db.String())
    TranslatedDestination = db.Column(db.String())
    TranslatedSource = db.Column(db.String())
