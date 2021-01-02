# To use this code, make sure you
#
#     import json
#
# and then, to convert JSON from a string, do
#
#     result = students_from_dict(json.loads(json_string))

from enum import Enum
from dataclasses import dataclass
from typing import Optional, Any, List, TypeVar, Type, cast, Callable


T = TypeVar("T")
EnumT = TypeVar("EnumT", bound=Enum)


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


def to_enum(c: Type[EnumT], x: Any) -> EnumT:
    assert isinstance(x, c)
    return x.value


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


class ContentLanguage(Enum):
    EN = "en"
    JA = "ja"
    ZH_TW = "zhTW"


@dataclass
class Owner:
    avatar_url: Optional[str] = None
    content_language: Optional[ContentLanguage] = None
    display_name: Optional[str] = None
    email: Optional[str] = None
    id: Optional[int] = None
    user_name: Optional[str] = None
    is_admin: Optional[bool] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Owner':
        assert isinstance(obj, dict)
        avatar_url = from_union([from_str, from_none], obj.get("avatarUrl"))
        content_language = from_union([ContentLanguage, from_none], obj.get("contentLanguage"))
        display_name = from_union([from_str, from_none], obj.get("displayName"))
        email = from_union([from_str, from_none], obj.get("email"))
        id = from_union([from_int, from_none], obj.get("id"))
        user_name = from_union([from_str, from_none], obj.get("userName"))
        is_admin = from_union([from_bool, from_none], obj.get("isAdmin"))
        return Owner(avatar_url, content_language, display_name, email, id, user_name, is_admin)

    def to_dict(self) -> dict:
        result: dict = {}
        result["avatarUrl"] = from_union([from_str, from_none], self.avatar_url)
        result["contentLanguage"] = from_union([lambda x: to_enum(ContentLanguage, x), from_none], self.content_language)
        result["displayName"] = from_union([from_str, from_none], self.display_name)
        result["email"] = from_union([from_str, from_none], self.email)
        result["id"] = from_union([from_int, from_none], self.id)
        result["userName"] = from_union([from_str, from_none], self.user_name)
        result["isAdmin"] = from_union([from_bool, from_none], self.is_admin)
        return result


@dataclass
class Datum:
    audio_url: Optional[str] = None
    content: Optional[str] = None
    created_at: Optional[int] = None
    id: Optional[int] = None
    owner: Optional[Owner] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Datum':
        assert isinstance(obj, dict)
        audio_url = from_union([from_str, from_none], obj.get("audioUrl"))
        content = from_union([from_str, from_none], obj.get("content"))
        created_at = from_union([from_int, from_none], obj.get("createdAt"))
        id = from_union([from_int, from_none], obj.get("id"))
        owner = from_union([Owner.from_dict, from_none], obj.get("owner"))
        return Datum(audio_url, content, created_at, id, owner)

    def to_dict(self) -> dict:
        result: dict = {}
        result["audioUrl"] = from_union([from_str, from_none], self.audio_url)
        result["content"] = from_union([from_str, from_none], self.content)
        result["createdAt"] = from_union([from_int, from_none], self.created_at)
        result["id"] = from_union([from_int, from_none], self.id)
        result["owner"] = from_union([lambda x: to_class(Owner, x), from_none], self.owner)
        return result


@dataclass
class Students:
    data: Optional[List[Datum]] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Students':
        assert isinstance(obj, dict)
        data = from_union([lambda x: from_list(Datum.from_dict, x), from_none], obj.get("data"))
        return Students(data)

    def to_dict(self) -> dict:
        result: dict = {}
        result["data"] = from_union([lambda x: from_list(lambda x: to_class(Datum, x), x), from_none], self.data)
        return result


def students_from_dict(s: Any) -> Students:
    return Students.from_dict(s)


def students_to_dict(x: Students) -> Any:
    return to_class(Students, x)
