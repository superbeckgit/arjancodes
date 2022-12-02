from dataclasses import dataclass
from time import time
from typing import Callable


# each social channel has a type and the current number of followers
@dataclass
class SocialChannel:
    type: str
    num_followers: int


# each post has a message and the timestamp when it should be posted
@dataclass
class Post:
    message: str
    timestamp: int


def post_to_youtube(channel: SocialChannel, message: str) -> None:
    print(f"{channel.type} channel: {message}")


def post_to_facebook(channel: SocialChannel, message: str) -> None:
    print(f"{channel.type} channel: {message}")


def post_to_twitter(channel: SocialChannel, message: str) -> None:
    print(f"{channel.type} channel: {message}")


# Define a type to help enforce posting function signature
MessagePoster = Callable[[SocialChannel, str], None]

CHANNEL_TO_POSTER: dict[str, MessagePoster] = {
    "youtube": post_to_youtube,
    "facebook": post_to_facebook,
    "twitter": post_to_twitter,
}


def process_schedule(posts: list[Post], channels: list[SocialChannel]) -> None:
    for post in posts:
        for channel in channels:
            if post.timestamp <= time():
                CHANNEL_TO_POSTER[channel.type](channel, post.message)


def main() -> None:
    post_tups = [
        (
            "Grandma's carrot cake is available again (limited quantities!)!",
            1568123400,
        ),
        ("Get your carrot cake now, the promotion ends today!", 1568133400),
    ]
    posts: list[Post] = [Post(*tup) for tup in post_tups]
    channel_tups = [
        ("youtube", 100),
        ("facebook", 100),
        ("twitter", 100),
    ]
    channels: list[SocialChannel] = [SocialChannel(*tup) for tup in channel_tups]
    process_schedule(posts, channels)


if __name__ == "__main__":
    main()
