import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

def recommendation(choice_id):
    books=pd.read_csv("./articles/database/bookdata.csv", encoding='UTF-8')
    ratings=pd.read_csv("./articles/database/ratings.csv", encoding='UTF-8')

    book_ratings = pd.merge(ratings,books, on="bookId" )

    user_book = book_ratings.pivot_table('rating', index='bookId', columns='userId')
    user_book = user_book.fillna(0)

    result_cosine = cosine_similarity(user_book,user_book)

    item_based_collab = pd.DataFrame(result_cosine, index=user_book.index, columns=user_book.index)
    try:
        result = item_based_collab[choice_id].sort_values(ascending=False)[:3]
        result_id = list(result.index.values)
        return result_id
    except KeyError:
        pass


