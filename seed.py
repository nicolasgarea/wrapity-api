import random
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from app.db.database import engine
from app.models.activity import Activity
from app.models.favorite import Favorite
from app.models.follower import Follower
from app.models.like import Like
from app.models.review import Review
from app.models.user import User

pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")
random.seed(42)

ALBUMS = {
    "discovery": 302127,
    "ram": 6575789,
    "homework": 302130,
    "currents": 6477004,
    "am": 112897,
    "ok_computer": 1581090,
}

ALBUM_IDS = list(ALBUMS.values())

USERS_DATA = [
    ("nicolas", "Electronic music obsessive. Daft Punk forever.", "admin"),
    ("laura", "Indie and alternative lover. Strokes superfan."),
    ("marcos", "Rock and roll forever. Arctic Monkeys evangelist."),
    ("sofia", "All genres welcome. Music is therapy."),
    ("alex", "Hip-hop head. Kendrick is GOAT."),
    ("clara", "Pop enthusiast and Swiftie since 2008."),
    ("diego", "Jazz collector and vinyl hoarder."),
    ("elena", "Reggaeton, trap and everything Latin."),
    ("pablo", "Radiohead, Pink Floyd, anything melancholic."),
    ("lucia", "Bedroom pop and dream pop addict."),
    ("javier", "Metal, prog, and concept albums."),
    ("marta", "R&B, neo-soul, Frank Ocean apologist."),
    ("carlos", "70s rock will never die."),
    ("ana", "Discovering new artists weekly."),
    ("david", "Producer ear. I listen for the mix."),
    ("paula", "Indie folk and singer-songwriters."),
    ("ruben", "Electronic, techno, house. Berlin scene."),
    ("noelia", "Latin alternative and Rosalia stan."),
    ("mario", "Rap espanol y trap nacional."),
    ("irene", "Female artists only this year. Try me."),
    ("victor", "Albums > singles. Always."),
    ("cristina", "I rate everything. Ratings matter."),
    ("ivan", "90s nostalgia. Britpop forever."),
    ("rocio", "Lo-fi, ambient, study music."),
    ("sergio", "Live albums and bootlegs collector."),
    ("nuria", "Teen me loved emo. Adult me still does."),
    ("hugo", "Soundtrack and film score nerd."),
    ("beatriz", "Funk, disco, anything groovy."),
    ("oscar", "Punk, post-punk, hardcore."),
    ("silvia", "Just here for the vibes."),
]

REVIEW_TEMPLATES = {
    5: [
        "Absolute masterpiece. No skips, no filler, just brilliance.",
        "This album changed my life. Every listen reveals something new.",
        "A perfect record. Production, songwriting, vocals all flawless.",
        "Top 10 of all time, easily. Cannot stop revisiting this.",
        "Generational album. Defines an era and still feels fresh.",
        "Five stars feels insufficient. Pure art from start to finish.",
        "I keep coming back to this. It just hits every single time.",
        "A flawless body of work. I have no critiques whatsoever.",
    ],
    4: [
        "Really strong project. A couple of weaker tracks but mostly excellent.",
        "Loved it. Not quite a 5 but undeniably great.",
        "Beautifully crafted. Will be on repeat for months.",
        "Top tier production and writing. Minor pacing issues only.",
        "Excellent album. The highs are stratospheric.",
        "Almost perfect. Just shy of greatness but still essential.",
        "Cohesive, memorable, ambitious. Very impressed.",
    ],
    3: [
        "Decent but inconsistent. Some bangers, some skippable tracks.",
        "Solid mid-tier release. Worth a listen but not a revisit.",
        "Mixed feelings. The concept is better than the execution.",
        "Has its moments but drags in the middle.",
        "Good ideas, average execution. Expected more.",
        "Not bad, not great. Just kind of there.",
    ],
    2: [
        "Disappointing. A few good tracks lost in a sea of filler.",
        "Hard to get through. The production saves it from being worse.",
        "Underwhelming. Felt rushed and uninspired.",
        "Not for me. Maybe I am missing something.",
    ],
    1: [
        "Hated it. Cannot understand the hype around this one.",
        "A complete miss. Everything that could go wrong, did.",
        "Skippable from track one. Truly a chore to finish.",
    ],
}


def make_review_text(rating: int) -> str:
    return random.choice(REVIEW_TEMPLATES[rating])


def seed():
    with Session(engine) as db:
        print("Cleaning existing data...")
        db.query(Activity).delete()
        db.query(Like).delete()
        db.query(Follower).delete()
        db.query(Favorite).delete()
        db.query(Review).delete()
        db.query(User).delete()
        db.commit()

        print("Seeding users...")
        users: list[User] = []
        for entry in USERS_DATA:
            username = entry[0]
            bio = entry[1]
            role = entry[2] if len(entry) > 2 else "user"

            user = User(
                username=username,
                email=f"{username}@wrapity.com",
                password_hash=pwd.hash("password123"),
                bio=bio,
                role=role,
            )
            db.add(user)
            users.append(user)

        db.flush()
        print(f"  -> {len(users)} users created.")

        print("Seeding reviews...")
        reviews: list[Review] = []
        rating_pool = [5] * 5 + [4] * 6 + [3] * 4 + [2] * 2 + [1] * 1

        for user in users:
            n_reviews = random.randint(3, 5)
            chosen_albums = random.sample(ALBUM_IDS, n_reviews)
            for album_id in chosen_albums:
                rating = random.choice(rating_pool)
                review = Review(
                    user_id=user.id,
                    album_id=album_id,
                    rating=rating,
                    content=make_review_text(rating),
                )
                db.add(review)
                reviews.append(review)
        db.flush()
        review_count = len(reviews)
        print(f"  -> {review_count} reviews created.")

        for review in reviews:
            db.add(
                Activity(
                    user_id=review.user_id, type="review", review_id=review.id
                )
            )

        print("Seeding likes...")
        like_count = 0
        for user in users:
            candidates = [r for r in reviews if r.user_id != user.id]
            for review in random.sample(candidates, random.randint(3, 8)):
                db.add(Like(user_id=user.id, review_id=review.id))
                db.add(
                    Activity(
                        user_id=user.id, type="like", review_id=review.id
                    )
                )
                like_count += 1
        print(f"  -> {like_count} likes created.")

        print("Seeding favorites...")
        favorite_count = 0
        for user in users:
            favs = random.sample(ALBUM_IDS, 4)
            for position, album_id in enumerate(favs, start=1):
                db.add(
                    Favorite(
                        user_id=user.id,
                        album_id=str(album_id),
                        position=position,
                    )
                )
                favorite_count += 1
        db.flush()
        print(f"  -> {favorite_count} favorites created.")

        print("Seeding followers...")
        follow_pairs: set[tuple[int, int]] = set()
        for user in users:
            n_following = random.randint(8, 15)
            candidates = [u for u in users if u.id != user.id]
            for target in random.sample(candidates, n_following):
                follow_pairs.add((user.id, target.id))

        followers_count = {u.id: 0 for u in users}
        for _, followed_id in follow_pairs:
            followers_count[followed_id] += 1

        for user in users:
            while followers_count[user.id] < 5:
                candidates = [u for u in users if u.id != user.id]
                random.shuffle(candidates)
                for c in candidates:
                    if (c.id, user.id) not in follow_pairs:
                        follow_pairs.add((c.id, user.id))
                        followers_count[user.id] += 1
                        break

        for follower_id, followed_id in follow_pairs:
            db.add(Follower(follower_id=follower_id, followed_id=followed_id))
            db.add(
                Activity(
                    user_id=follower_id,
                    type="follow",
                    target_user_id=followed_id,
                )
            )

        print(f"  -> {len(follow_pairs)} follow relationships created.")

        db.commit()
        print("\nSeed completed successfully.")
        print(f"Users:     {len(users)}")
        print(f"Reviews:   {review_count}")
        print(f"Favorites: {favorite_count}")
        print(f"Likes:     {like_count}")
        print(f"Follows:   {len(follow_pairs)}")


if __name__ == "__main__":
    seed()
