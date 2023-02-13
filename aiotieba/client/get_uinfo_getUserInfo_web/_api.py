import yarl

from .._core import HttpCore
from .._helper import pack_web_get_request, parse_json, send_request
from ..const import WEB_BASE_HOST
from ..exception import TiebaServerError
from ._classdef import UserInfo_guinfo_web


def null_ret_factory() -> UserInfo_guinfo_web:
    return UserInfo_guinfo_web()._init_null()


def parse_body(body: bytes) -> UserInfo_guinfo_web:
    res_json = parse_json(body)
    if code := res_json['errno']:
        raise TiebaServerError(code, res_json['errmsg'])

    user_dict = res_json['chatUser']
    user = UserInfo_guinfo_web()._init(user_dict)

    return user


async def request(http_core: HttpCore, user_id: int) -> UserInfo_guinfo_web:
    params = [('chatUid', user_id)]

    request = pack_web_get_request(
        http_core,
        yarl.URL.build(scheme="http", host=WEB_BASE_HOST, path="/im/pcmsg/query/getUserInfo"),
        params,
    )

    __log__ = "user_id={user_id}"  # noqa: F841

    body = await send_request(request, http_core.connector, read_bufsize=2 * 1024)
    return parse_body(body)
