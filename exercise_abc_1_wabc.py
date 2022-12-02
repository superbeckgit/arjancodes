from abc import ABC, abstractmethod
from dataclasses import dataclass
from time import time


# SocialChannel = tuple[str, int]
# each social channel has a type
# and the current number of followers
@dataclass
class SocialChannel(ABC):
    num_followers: int

    @property
    @abstractmethod
    def type(self) -> str:
        pass

    @abstractmethod
    def post_to_channel(self, message: str) -> None:
        pass


@dataclass
class FacebookChannel(SocialChannel):
    @property
    def type(self) -> str:
        return "Facebook"

    def post_to_channel(self, message: str) -> None:
        print(f"{self.type} channel: {message}")


@dataclass
class TwitterChannel(SocialChannel):
    @property
    def type(self) -> str:
        return "Twitter"

    def post_to_channel(self, message: str) -> None:
        print(f"{self.type} channel: {message}")


@dataclass
class YoutubeChannel(SocialChannel):
    @property
    def type(self) -> str:
        return "Youtube"

    def post_to_channel(self, message: str) -> None:
        print(f"{self.type} channel: {message}")


# Post = tuple[str, int]
# each post has a message and the timestamp when it should be posted
@dataclass
class Post:
    message: str
    timestamp: int


def process_schedule(posts: list[Post], channels: list[SocialChannel]) -> None:
    for post in posts:
        for channel in channels:
            if post.timestamp <= time():
                channel.post_to_channel(post.message)


def main() -> None:
    posts: list[Post] = [
        Post(msg, tme)
        for msg, tme in [
            (
                "Grandma's carrot cake is available again (limited quantities!)!",
                1568123400,
            ),
            ("Get your carrot cake now, the promotion ends today!", 1568133400),
        ]
    ]
    channels: list[SocialChannel] = [
        YoutubeChannel(100),
        FacebookChannel(100),
        TwitterChannel(100),
    ]
    process_schedule(posts, channels)


if __name__ == "__main__":
    main()
