import sys
import zipfile


WATCHED = 'watched.csv'
LIKED = 'likes/films.csv'
WATCHLIST = 'watchlist.csv'


def options():
    print("""Options:
h/help - show this help
s/stats - show stats

m/movies - list shared watched movies
l/liked - list shared liked movies
w/watchlist - list shared movies in watchlist

ml/movies_liked - list movies that one person watched and the other liked
mw/movies_watchlist - list movies that one person watched and the other watchlisted
lw/liked_watchlist - list movies that one person liked and the other watchlisted

q/quit - quit""")


def init(args: list):
    if len(args) != 5:
        print("Usage: python main.py <name person 1> <zip person 1> <name person 2> <zip person 2>")
        sys.exit(1)
    person1 = Person(args[1], args[2])
    person2 = Person(args[3], args[4])
    return person1, person2


def from_csv_text(text: str) -> set:
    movies_set = set()
    movies = text.decode().splitlines()[1:]
    for movie in movies:
        splitted = movie.split('"')
        if len(splitted) == 1:
            splitted = movie.split(',')
            year = splitted[2]
        else:
            year = splitted[2].split(',')[1]
        movies_set.add(f"{splitted[1]} ({year})")
    return movies_set


class Person:
    def __init__(self, name, zip):
        print(f"loading {name} from {zip}")
        self.name = name
        loaded_zip = zipfile.ZipFile(zip)
        self.watched = from_csv_text(loaded_zip.read(WATCHED))
        self.liked = from_csv_text(loaded_zip.read(LIKED))
        self.watchlist = from_csv_text(loaded_zip.read(WATCHLIST))


def stats_person(person):
    print(f"""    -> {person.name}:
        watched {len(person.watched)} movies
        liked {len(person.liked)} movies
        watchlisted {len(person.watchlist)} movies""")


def stats_shared(person1, person2):
    print(f"""    -> share {len(shared_movies(person1, person2))} watched movies
    -> share {len(shared_liked(person1, person2))} liked movies
    -> share {len(shared_watchlist(person1, person2))} movies in watchlist

    -> {person1.name} watched {len(p1_watched_p2_liked(person1, person2))} movies that {person2.name} liked
    -> {person2.name} watched {len(p1_watched_p2_liked(person2, person1))} movies that {person1.name} liked

    -> {person1.name} watched {len(p1_watched_p2_watchlist(person1, person2))} movies that {person2.name} watchlisted
    -> {person2.name} watched {len(p1_watched_p2_watchlist(person2, person1))} movies that {person1.name} watchlisted

    -> {person1.name} liked {len(p1_liked_p2_watchlist(person1, person2))} movies that {person2.name} watchlisted
    -> {person2.name} liked {len(p1_liked_p2_watchlist(person2, person1))} movies that {person1.name} watchlisted
""")


def stats(person1, person2):
    print("loaded info:")
    stats_person(person1)
    stats_person(person2)
    print("\nshared info:")
    stats_shared(person1, person2)


def shared_movies(p1, p2):
    return p1.watched.intersection(p2.watched)


def shared_liked(p1, p2):
    return p1.liked.intersection(p2.liked)


def shared_watchlist(p1, p2):
    return p1.watchlist.intersection(p2.watchlist)


def p1_watched_p2_liked(p1, p2):
    return p1.watched.intersection(p2.liked)


def p1_watched_p2_watchlist(p1, p2):
    return p1.watched.intersection(p2.watchlist)


def p1_liked_p2_watchlist(p1, p2):
    return p1.liked.intersection(p2.watchlist)


def list_shared(person1, person2, shared_func, shared_type):
    shared = shared_func(person1, person2)
    print(f"-> you both share {len(shared)} {shared_type} movies")
    for movie in sorted(shared):
        print(movie)


def list_shared_movies(person1, person2):
    list_shared(person1, person2, shared_movies, 'watched')


def list_shared_liked(person1, person2):
    list_shared(person1, person2, shared_liked, 'liked')


def list_shared_watchlist(person1, person2):
    list_shared(person1, person2, shared_watchlist, 'watchlisted')


def list_p1_vs_p2(person1, person2, vs_func, vs_type_p1, vs_type_p2):
    movies = vs_func(person1, person2)
    print(f"-> {person1.name} {vs_type_p1} {len(movies)
                                            } movies that {person2.name} {vs_type_p2}")
    for movie in sorted(movies):
        print(movie)


def list_p1_watched_p2_liked(person1, person2):
    list_p1_vs_p2(person1, person2, p1_watched_p2_liked, 'watched', 'liked')


def list_p1_watched_p2_watchlist(person1, person2):
    list_p1_vs_p2(person1, person2, p1_watched_p2_watchlist,
                  'watched', 'watchlisted')


def list_p1_liked_p2_watchlist(person1, person2):
    list_p1_vs_p2(person1, person2, p1_liked_p2_watchlist,
                  'liked', 'watchlisted')


def console(person1, person2):
    while True:
        command = input(">> ").lower()
        if command == 'h' or command == 'help':
            options()
        elif command == 's' or command == 'stats':
            stats(person1, person2)
        elif command == 'm' or command == 'movies':
            list_shared_movies(person1, person2)
        elif command == 'l' or command == 'liked':
            list_shared_liked(person1, person2)
        elif command == 'w' or command == 'watchlist':
            list_shared_watchlist(person1, person2)
        elif command == 'ml' or command == 'movies_liked':
            list_p1_watched_p2_liked(person1, person2)
            list_p1_watched_p2_liked(person2, person1)
        elif command == 'mw' or command == 'movies_watchlist':
            list_p1_watched_p2_watchlist(person1, person2)
            list_p1_watched_p2_watchlist(person2, person1)
        elif command == 'lw' or command == 'liked_watchlist':
            list_p1_liked_p2_watchlist(person1, person2)
            list_p1_liked_p2_watchlist(person2, person1)
        elif command == 'q' or command == 'quit':
            print("bye!")
            sys.exit(0)


if __name__ == '__main__':
    person1, person2 = init(sys.argv)
    try:
        console(person1, person2)
    except (KeyboardInterrupt, EOFError):
        sys.exit(0)
