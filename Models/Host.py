# To use this code, make sure you
#
#     import json
#
# and then, to convert JSON from a string, do
#
#     result = host_from_dict(json.loads(json_string))

from dataclasses import dataclass
from typing import Optional, Any, List, TypeVar, Callable, Type, cast


T = TypeVar("T")


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def from_none(x: Any) -> Any:
    assert x is None
    return x


def from_union(fs, x):
    for f in fs:
        try:
            return f(x)
        except:
            pass
    assert False


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


def from_bool(x: Any) -> bool:
    assert isinstance(x, bool)
    return x


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]
    


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


def is_type(t: Type[T], x: Any) -> T:
    assert isinstance(x, t)
    return x

def from_float(x: Any) -> float:
    assert isinstance(x, (float, int)) and not isinstance(x, bool)
    return float(x)


def to_float(x: Any) -> float:
    assert isinstance(x, float)
    return x

@dataclass
class HostClass:
    avatar_url: Optional[str] = None
    content_language: Optional[str] = None
    display_name: Optional[str] = None
    email: Optional[str] = None
    id: Optional[int] = None
    user_name: Optional[str] = None
    is_admin: Optional[bool] = None
    comment: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'HostClass':
        assert isinstance(obj, dict)
        avatar_url = from_union([from_str, from_none], obj.get("avatarUrl"))
        content_language = from_union([from_str, from_none], obj.get("contentLanguage"))
        display_name = from_union([from_str, from_none], obj.get("displayName"))
        email = from_union([from_str, from_none], obj.get("email"))
        id = from_union([from_int, from_none], obj.get("id"))
        user_name = from_union([from_str, from_none], obj.get("userName"))
        is_admin = from_union([from_bool, from_none], obj.get("isAdmin"))
        comment = from_union([from_str, from_none], obj.get("comment"))
        return HostClass(avatar_url, content_language, display_name, email, id, user_name, is_admin, comment)

    def to_dict(self) -> dict:
        result: dict = {}
        result["avatarUrl"] = from_union([from_str, from_none], self.avatar_url)
        result["contentLanguage"] = from_union([from_str, from_none], self.content_language)
        result["displayName"] = from_union([from_str, from_none], self.display_name)
        result["email"] = from_union([from_str, from_none], self.email)
        result["id"] = from_union([from_int, from_none], self.id)
        result["userName"] = from_union([from_str, from_none], self.user_name)
        result["isAdmin"] = from_union([from_bool, from_none], self.is_admin)
        result["comment"] = from_union([from_str, from_none], self.comment)
        return result


@dataclass
class Definition:
    id: Optional[int] = None
    content: Optional[str] = None
    text: Optional[str] = None
    pos: Optional[str] = None
    kk: Optional[str] = None
    sound_url: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Definition':
        assert isinstance(obj, dict)
        id = from_union([from_int, from_none], obj.get("id"))
        content = from_union([from_str, from_none], obj.get("content"))
        text = from_union([from_str, from_none], obj.get("text"))
        pos = from_union([from_str, from_none], obj.get("pos"))
        kk = from_union([from_str, from_none], obj.get("kk"))
        sound_url = from_union([from_str, from_none], obj.get("soundUrl"))
        return Definition(id, content, text, pos, kk, sound_url)

    def to_dict(self) -> dict:
        result: dict = {}
        result["id"] = from_union([from_int, from_none], self.id)
        result["content"] = from_union([from_str, from_none], self.content)
        result["text"] = from_union([from_str, from_none], self.text)
        result["pos"] = from_union([from_str, from_none], self.pos)
        result["kk"] = from_union([from_str, from_none], self.kk)
        result["soundUrl"] = from_union([from_str, from_none], self.sound_url)
        return result


@dataclass
class Vocabulary:
    id: Optional[int] = None
    content: Optional[str] = None
    text: Optional[str] = None
    definitions: Optional[List[Definition]] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Vocabulary':
        assert isinstance(obj, dict)
        id = from_union([from_int, from_none], obj.get("id"))
        content = from_union([from_str, from_none], obj.get("content"))
        text = from_union([from_str, from_none], obj.get("text"))
        definitions = from_union([lambda x: from_list(Definition.from_dict, x), from_none], obj.get("definitions"))
        return Vocabulary(id, content, text, definitions)

    def to_dict(self) -> dict:
        result: dict = {}
        result["id"] = from_union([from_int, from_none], self.id)
        result["content"] = from_union([from_str, from_none], self.content)
        result["text"] = from_union([from_str, from_none], self.text)
        result["definitions"] = from_union([lambda x: from_list(lambda x: to_class(Definition, x), x), from_none], self.definitions)
        return result


@dataclass
class Data:
    release_date_text: Optional[int] = None
    video_id: Optional[int] = None
    content: Optional[str] = None
    duration: Optional[float] = None
    host: Optional[HostClass] = None
    id: Optional[int] = None
    image_url: Optional[str] = None
    published_at: Optional[int] = None
    created_at: Optional[int] = None
    start_at: Optional[int] = None
    title: Optional[str] = None
    youtube_id: Optional[str] = None
    audio_url: Optional[str] = None
    translated_content: Optional[str] = None
    vocabularies: Optional[List[Vocabulary]] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Data':
        assert isinstance(obj, dict)
        release_date_text = from_union([from_none, lambda x: int(from_str(x))], obj.get("releaseDateText"))
        video_id = from_union([from_int, from_none], obj.get("videoId"))
        content = from_union([from_str, from_none], obj.get("content"))
        duration = from_union([from_float, from_none], obj.get("duration"))
        host = from_union([HostClass.from_dict, from_none], obj.get("host"))
        id = from_union([from_int, from_none], obj.get("id"))
        image_url = from_union([from_str, from_none], obj.get("imageUrl"))
        published_at = from_union([from_int, from_none], obj.get("publishedAt"))
        created_at = from_union([from_int, from_none], obj.get("createdAt"))
        start_at = from_union([from_float, from_none], obj.get("startAt"))
        title = from_union([from_str, from_none], obj.get("title"))
        youtube_id = from_union([from_str, from_none], obj.get("youtubeId"))
        audio_url = from_union([from_str, from_none], obj.get("audioUrl"))
        translated_content = from_union([from_str, from_none], obj.get("translatedContent"))
        vocabularies = from_union([lambda x: from_list(Vocabulary.from_dict, x), from_none], obj.get("vocabularies"))
        return Data(release_date_text, video_id, content, duration, host, id, image_url, published_at, created_at, start_at, title, youtube_id, audio_url, translated_content, vocabularies)

    def to_dict(self) -> dict:
        result: dict = {}
        result["releaseDateText"] = from_union([lambda x: from_none((lambda x: is_type(type(None), x))(x)), lambda x: from_str((lambda x: str((lambda x: is_type(int, x))(x)))(x))], self.release_date_text)
        result["videoId"] = from_union([from_int, from_none], self.video_id)
        result["content"] = from_union([from_str, from_none], self.content)
        result["duration"] = from_union([from_float, from_none], self.duration)
        result["host"] = from_union([lambda x: to_class(HostClass, x), from_none], self.host)
        result["id"] = from_union([from_int, from_none], self.id)
        result["imageUrl"] = from_union([from_str, from_none], self.image_url)
        result["publishedAt"] = from_union([from_int, from_none], self.published_at)
        result["createdAt"] = from_union([from_int, from_none], self.created_at)
        result["startAt"] = from_union([from_float, from_none], self.start_at)
        result["title"] = from_union([from_str, from_none], self.title)
        result["youtubeId"] = from_union([from_str, from_none], self.youtube_id)
        result["audioUrl"] = from_union([from_str, from_none], self.audio_url)
        result["translatedContent"] = from_union([from_str, from_none], self.translated_content)
        result["vocabularies"] = from_union([lambda x: from_list(lambda x: to_class(Vocabulary, x), x), from_none], self.vocabularies)
        return result


@dataclass
class Host:
    data: Optional[Data] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Host':
        assert isinstance(obj, dict)
        data = from_union([Data.from_dict, from_none], obj.get("data"))
        return Host(data)

    def to_dict(self) -> dict:
        result: dict = {}
        result["data"] = from_union([lambda x: to_class(Data, x), from_none], self.data)
        return result


def host_from_dict(s: Any) -> Host:
    return Host.from_dict(s)


def host_to_dict(x: Host) -> Any:
    return to_class(Host, x)
