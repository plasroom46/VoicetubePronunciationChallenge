# To use this code, make sure you
#
#     import json
#
# and then, to convert JSON from a string, do
#
#     result = comment_ids_from_dict(json.loads(json_string))

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


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


@dataclass
class Host:
    displayname: Optional[str] = None
    id: Optional[int] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Host':
        assert isinstance(obj, dict)
        displayname = from_union([from_str, from_none], obj.get("displayname"))
        id = from_union([from_int, from_none], obj.get("id"))
        return Host(displayname, id)

    def to_dict(self) -> dict:
        result: dict = {}
        result["displayname"] = from_union([from_str, from_none], self.displayname)
        result["id"] = from_union([from_int, from_none], self.id)
        return result


@dataclass
class CommentIDS:
    hosts: Optional[List[Host]] = None
    users: Optional[List[Host]] = None

    @staticmethod
    def from_dict(obj: Any) -> 'CommentIDS':
        assert isinstance(obj, dict)
        hosts = from_union([lambda x: from_list(Host.from_dict, x), from_none], obj.get("hosts"))
        users = from_union([lambda x: from_list(Host.from_dict, x), from_none], obj.get("users"))
        return CommentIDS(hosts, users)

    def to_dict(self) -> dict:
        result: dict = {}
        result["hosts"] = from_union([lambda x: from_list(lambda x: to_class(Host, x), x), from_none], self.hosts)
        result["users"] = from_union([lambda x: from_list(lambda x: to_class(Host, x), x), from_none], self.users)
        return result


def comment_ids_from_dict(s: Any) -> CommentIDS:
    return CommentIDS.from_dict(s)


def comment_ids_to_dict(x: CommentIDS) -> Any:
    return to_class(CommentIDS, x)
