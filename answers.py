import praw
import json

reddit = praw.Reddit(
    client_id="4gyGRAZg0UiK5Y9lWEa00w",
    client_secret="nO0q9PyH8Q1WGijwpIYr82t5ngXnaw",
    user_agent="zilean_bot",
)

from googlesearch import search

def get_comments(query):
    google_query = query + " site:reddit.com"
    url = next(search(google_query, num_results=1))

    submission = reddit.submission(url=url)

    comments = submission.comments
    comments_sorted = sorted(comments, key=lambda comment: comment.score, reverse=True)
    top_comments = comments_sorted[:5]

    comments_list = []
    for comment in top_comments:
        comment_dict = {
            "content": comment.body,
            "score": comment.score
        }
        comments_list.append(comment_dict)

    # use python dict here
    json_object = {"question": query, "answers": comments_list}
    json_string = json.dumps(json_object, indent=4)

    return json_string
