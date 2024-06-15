from enum import Enum
import heapq
class Movie:
    def __init__(self, title: str, id: int = 0):
        self.title = title
        self.id = id
    def __str__(self):
        return f'{{id: {self.id}, title: "{self.title}"}}'
class User:
    def __init__(self, id: int = 0):
        self.id = id

class RecommendationRegistry:
    def __init__(self):
        self.movie_ratings = {}
        self.users = {}
        self.movies = {}
    def rate(self, user: User, movie: Movie, rating: int):
        if rating <= 0 and rating > 5: 
            raise ValueError("Rating should be between 1 to 5.")
        if not movie in self.movie_ratings:
            self.movie_ratings[movie] = {}
            self.movies[movie.id] = movie
        self.movie_ratings[movie][user] = rating
        if not user in self.users:
            self.users[user] = {}
        self.users[user][movie] = rating
    def ratings(self):
        res = {}
        for movie,user_ratings in self.movie_ratings.items():
            res[movie.id] = sum(user_ratings.values()) / len(user_ratings)
        return res
    def recommend(self, user: User):
        if not user in self.users:
            return self._recommend_newuser()
        else: 
            return self._recommend_by_similarity(user)
    # get movie with best rating
    def _recommend_newuser(self):
        maxR = float("-inf")
        movie = None
        for id, rating in self.ratings().items():
            if rating > maxR:
                maxR = rating
                movie = self.movies[id]
        return movie
    # find user with similar ratings 'closeUser', from his watched movies, recommend the best
    # movie that user has not watched/rated
    def _recommend_by_similarity(self, user):
        closeUser = self.get_similar_user(user)
        bestMovieRating = 0
        movieRecommendation = None
        for m, ratings in self.movie_ratings.items():
            if closeUser in ratings and user not in ratings:
                if ratings[closeUser] > bestMovieRating:
                    bestMovieRating = ratings[closeUser]
                    movieRecommendation = m
        return movieRecommendation

    def get_similar_user(self, user):
        bestScore = float("inf")
        for u in self.users:
            if u != user:
                score = self.get_similarity_score(u, user)
                if score < bestScore:
                    closeUser = u
                    bestScore = score
        return closeUser
    def get_similarity_score(self, user1: User, user2: User):
        score = 0
        cnt = 0
        for r in self.movie_ratings.values():
            if user1 in r and user2 in r:
                cnt += 1
                score += abs(r[user1] - r[user2])
        return score / cnt if cnt != 0 else 0


u1 = User(1)
u2 = User(2)
u3 = User(3)

m1 = Movie("Batman Begins", 1)
m2 = Movie("Your Name", 2)
m3 = Movie("Her", 3)
m4 = Movie("The Notebook", 4)
m5 = Movie("The Mercenaries", 5)


r = RecommendationRegistry()
r.rate(u1, m1, 5)
r.rate(u1, m2, 2)
r.rate(u1, m3, 1)
r.rate(u1, m4, 5)
r.rate(u1, m5, 5)

r.rate(u2, m1, 3)
r.rate(u2, m2, 5)
r.rate(u2, m3, 5)
r.rate(u2, m4, 5)

r.rate(u3, m1, 1)
r.rate(u3, m2, 5)
r.rate(u3, m3, 5)

print(r.ratings()) # {1: 3.0, 2: 4.0, 3: 3.6666666666666665, 4: 5.0, 0: 5.0}

print(r.recommend(u3)) # {id: 4, title: "The Notebook"}
print(r.get_similarity_score(u1, u2)) # 2.25
print(r.get_similarity_score(u2, u1)) # 2.25
print(r.get_similarity_score(u1, u3)) # 3.66
print(r.get_similarity_score(u3, u1)) # 3.66
print(r.get_similarity_score(u2, u3)) # 0.66
print(r.get_similarity_score(u3, u2)) # 0.66

print(r.get_similar_user(u1).id) # 2
print(r.get_similar_user(u2).id) # 3
print(r.get_similar_user(u3).id) # 2

