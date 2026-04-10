from app.db.database import engine
from app.models.user import User
from app.models.review import Review
from app.models.favorite import Favorite
from app.models.follower import Follower
from sqlalchemy.orm import Session
from passlib.context import CryptContext

pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")

DISCOVERY = 302127
RAM = 6575789
HOMEWORK = 302130
AM = 112897
OK_COMPUTER = 1581090
CURRENTS = 6477004
IS_THIS_IT = 6192479

def seed():
    with Session(engine) as db:
        nicolas = User(username="nicolas", email="nicolas@wrapity.com", password_hash=pwd.hash("password123"), bio="Electronic music obsessive", role="admin")
        laura = User(username="laura", email="laura@wrapity.com", password_hash=pwd.hash("password123"), bio="Indie and alternative lover")
        marcos = User(username="marcos", email="marcos@wrapity.com", password_hash=pwd.hash("password123"), bio="Rock and roll forever")
        sofia = User(username="sofia", email="sofia@wrapity.com", password_hash=pwd.hash("password123"), bio="All genres welcome")
        db.add_all([nicolas, laura, marcos, sofia])
        db.flush()

        db.add_all([
            Review(user_id=nicolas.id, album_id=DISCOVERY, rating=5, content="A timeless electronic masterpiece. Every track is perfect."),
            Review(user_id=nicolas.id, album_id=AM, rating=5, content="AM is flawless from start to finish."),
            Review(user_id=nicolas.id, album_id=OK_COMPUTER, rating=5, content="Changed the way I listen to music."),
            Review(user_id=laura.id, album_id=DISCOVERY, rating=4, content="Iconic. Get Lucky alone is worth it."),
            Review(user_id=laura.id, album_id=IS_THIS_IT, rating=5, content="Is This It never gets old."),
            Review(user_id=laura.id, album_id=CURRENTS, rating=5, content="Currents is a journey you never want to end."),
            Review(user_id=marcos.id, album_id=RAM, rating=5, content="RAM is the most ambitious album of the decade."),
            Review(user_id=marcos.id, album_id=AM, rating=4, content="Arctic Monkeys at their absolute best."),
            Review(user_id=sofia.id, album_id=HOMEWORK, rating=3, content="Good but not their best work."),
            Review(user_id=sofia.id, album_id=OK_COMPUTER, rating=5, content="Radiohead redefined rock with this one."),
        ])

        db.add_all([
            Favorite(user_id=nicolas.id, album_id=str(DISCOVERY), position=1),
            Favorite(user_id=nicolas.id, album_id=str(AM), position=2),
            Favorite(user_id=nicolas.id, album_id=str(OK_COMPUTER), position=3),
            Favorite(user_id=laura.id, album_id=str(IS_THIS_IT), position=1),
            Favorite(user_id=laura.id, album_id=str(CURRENTS), position=2),
            Favorite(user_id=marcos.id, album_id=str(RAM), position=1),
            Favorite(user_id=marcos.id, album_id=str(AM), position=2),
            Favorite(user_id=sofia.id, album_id=str(OK_COMPUTER), position=1),
            Favorite(user_id=sofia.id, album_id=str(HOMEWORK), position=2),
        ])

        db.add_all([
            Follower(follower_id=nicolas.id, followed_id=laura.id),
            Follower(follower_id=nicolas.id, followed_id=marcos.id),
            Follower(follower_id=laura.id, followed_id=nicolas.id),
            Follower(follower_id=marcos.id, followed_id=nicolas.id),
            Follower(follower_id=sofia.id, followed_id=nicolas.id),
            Follower(follower_id=sofia.id, followed_id=laura.id),
        ])

        db.commit()
        print("Seed completed successfully")

if __name__ == "__main__":
    seed()