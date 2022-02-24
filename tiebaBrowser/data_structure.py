# -*- coding:utf-8 -*-
__all__ = ('BasicUserInfo', 'UserInfo',
           'Thread', 'Post', 'Comment',
           'Threads', 'Posts', 'Comments',
           'At')

import re
import traceback
from typing import Generic, Iterator, NoReturn, Optional, TypeVar, Union

from .logger import log

T = TypeVar('T')


class BasicUserInfo(object):
    """
    BasicUserInfo()
    基本用户属性

    _id: 用于快速构造UserInfo的自适应参数 输入用户名或portrait或user_id

    user_name: 发帖用户名
    nick_name: 发帖人昵称
    portrait: 用户头像portrait值
    user_id: 贴吧旧版uid
    """

    __slots__ = ['user_name', '_nick_name', '_portrait', '_user_id']

    def __init__(self, _id: Union[str, int, None] = None, user_name: str = '', nick_name: str = '', portrait: str = '', user_id: int = 0):
        if _id:
            if isinstance(_id, int):
                self.user_id = _id
                self.portrait = portrait
                self.user_name = user_name
            else:
                self.portrait = _id
                if not self.portrait:
                    self.user_name = _id
                else:
                    self.user_name = user_name
                self.user_id = user_id
        else:
            self.portrait = portrait
            self.user_name = user_name
            self.user_id = user_id

        self.nick_name = nick_name

    def __str__(self) -> str:
        return f"user_name:{self.user_name} / nick_name:{self._nick_name} / portrait:{self._portrait} / user_id:{self._user_id}"

    def __hash__(self) -> int:
        return self._user_id.__hash__()

    @property
    def nick_name(self) -> str:
        return self._nick_name

    @nick_name.setter
    def nick_name(self, new_nick_name: str) -> NoReturn:
        if self.user_name != new_nick_name:
            self._nick_name = new_nick_name
        else:
            self._nick_name = ''

    @property
    def portrait(self) -> str:
        return self._portrait

    @portrait.setter
    def portrait(self, new_portrait: str) -> NoReturn:
        if new_portrait and new_portrait.startswith('tb.'):
            try:
                self._portrait = re.match('[\w\-_.]+', new_portrait).group(0)
            except Exception:
                self._portrait = ''
        else:
            self._portrait = ''

    @property
    def user_id(self) -> int:
        return self._user_id

    @user_id.setter
    def user_id(self, new_user_id: int) -> NoReturn:
        if new_user_id:
            self._user_id = int(new_user_id)
        else:
            self._user_id = 0

    @property
    def show_name(self) -> str:
        return self.nick_name if self.nick_name else self.user_name

    @property
    def log_name(self) -> str:
        if self.user_name:
            return self.user_name
        else:
            return f'{self.nick_name}/{self.portrait}'


class UserInfo(BasicUserInfo):
    """
    UserInfo()
    用户属性

    _id: 用于快速构造UserInfo的自适应参数 输入用户名或portrait或user_id

    user_name: 发帖用户名
    nick_name: 发帖人昵称
    portrait: 用户头像portrait值
    user_id: 贴吧旧版uid
    level: 等级
    gender: 性别（1男2女0未知）
    is_vip: 是否vip
    is_god: 是否贴吧大神
    priv_like: 是否公开关注贴吧（1完全可见2好友可见3完全隐藏）
    priv_reply: 帖子评论权限（1所有人5我的粉丝6我的关注）
    """

    __slots__ = ['_level', '_gender',
                 'is_vip', 'is_god', '_priv_like', '_priv_reply']

    def __init__(self, _id: Union[str, int, None] = None, user_name: str = '', nick_name: str = '', portrait: str = '', user_id: int = 0, level: int = 0, gender: int = 0, is_vip: bool = False, is_god: bool = False, priv_like: int = 3, priv_reply: int = 1):
        super().__init__(_id, user_name, nick_name, portrait, user_id)
        self.level = level
        self.gender = gender
        self.is_vip = is_vip
        self.is_god = is_god
        self.priv_like = priv_like
        self.priv_reply = priv_reply

    @property
    def level(self) -> int:
        return self._level

    @level.setter
    def level(self, new_level: int) -> NoReturn:
        if new_level:
            self._level = int(new_level)
        else:
            self._level = 0

    @property
    def gender(self) -> int:
        return self._gender

    @gender.setter
    def gender(self, new_gender: int) -> NoReturn:
        if new_gender:
            self._gender = int(new_gender)
        else:
            self._gender = 0

    @property
    def priv_like(self) -> int:
        return self._priv_like

    @priv_like.setter
    def priv_like(self, new_priv_like: int) -> NoReturn:
        if new_priv_like:
            self._priv_like = int(new_priv_like)
        else:
            self._priv_like = 3

    @property
    def priv_reply(self) -> int:
        return self._priv_reply

    @priv_reply.setter
    def priv_reply(self, new_priv_reply: int) -> NoReturn:
        if new_priv_reply:
            self._priv_reply = int(new_priv_reply)
        else:
            self._priv_reply = 1


class BaseContent(object):
    """
    基本的内容信息

    fid: 所在吧id
    tid: 帖子编号
    pid: 回复编号
    text: 文本内容
    user: UserInfo类 发布者信息
    """

    __slots__ = ['fid', 'tid', 'pid', '_text', 'user']

    def __init__(self, fid: int = 0, tid: int = 0, pid: int = 0, text: str = '', user: UserInfo = UserInfo()):
        self.fid = fid
        self.tid = tid
        self.pid = pid
        self._text = text
        self.user = user

    @property
    def text(self) -> str:
        return self._text


class BaseContents(Generic[T]):
    """
    Threads/Posts/Comments的泛型基类
    约定取内容的通用接口
    """

    __slots__ = ['current_pn', 'total_pn', '_objs']

    def __init__(self) -> NoReturn:
        super().__init__()

    def __iter__(self) -> Iterator[T]:
        return iter(self._objs)

    def __getitem__(self, idx: int) -> T:
        return self._objs[idx]

    def __len__(self) -> int:
        return len(self._objs)

    @property
    def has_next(self) -> bool:
        return self.current_pn < self.total_pn


class Thread(BaseContent):
    """
    主题帖信息

    text: 所有文本
    fid: 所在吧id
    tid: 帖子编号
    pid: 回复编号
    user: UserInfo类 发布者信息
    title: 标题内容
    first_floor_text: 首楼内容
    has_audio: 是否含有音频
    has_video: 是否含有视频
    view_num: 浏览量
    reply_num: 回复数
    like: 点赞数
    dislike: 点踩数
    create_time: 10位时间戳 创建时间
    last_time: 10位时间戳 最后回复时间
    """

    __slots__ = ['title', 'first_floor_text', 'has_audio', 'has_video',
                 'view_num', 'reply_num', 'like', 'dislike', 'create_time', 'last_time']

    def __init__(self, fid: int = 0, tid: int = 0, pid: int = 0, user: UserInfo = UserInfo(), title: str = '', first_floor_text: str = '', has_audio: bool = False, has_video: bool = False, view_num: int = 0, reply_num: int = 0, like: int = 0, dislike: int = 0, create_time: int = 0, last_time: int = 0):
        super().__init__(fid=fid, tid=tid, pid=pid, user=user)
        self.title = title
        self.first_floor_text = first_floor_text
        self.has_audio = has_audio
        self.has_video = has_video
        self.view_num = view_num
        self.reply_num = reply_num
        self.like = like
        self.dislike = dislike
        self.create_time = create_time
        self.last_time = last_time

    @property
    def text(self) -> str:
        if not self._text:
            self._text = f'{self.title}\n{self.first_floor_text}'
        return self._text


class Threads(BaseContents[Thread]):
    """
    thread列表
    """

    __slots__ = []

    def __init__(self, main_json: Optional[dict] = None):

        def _init_userinfo(user_dict: dict) -> UserInfo:
            try:
                user_id = int(user_dict['id'])
                if not user_id:
                    return UserInfo()
                priv_sets = user_dict['priv_sets']
                if not priv_sets:
                    priv_sets = {}
                user = UserInfo(user_name=user_dict['name'],
                                nick_name=user_dict['name_show'],
                                portrait=user_dict['portrait'],
                                user_id=user_id,
                                gender=user_dict['gender'],
                                is_vip=bool(user_dict['new_tshow_icon']),
                                is_god=user_dict.__contains__('new_god_data'),
                                priv_like=priv_sets.get('like', None),
                                priv_reply=priv_sets.get('reply', None)
                                )
                return user

            except Exception as err:
                log.error(
                    f"Failed to init UserInfo of {user_id} in {fid}. reason:{traceback.format_tb(err.__traceback__)[-1]}")
                return UserInfo()

        def _init_obj(obj_dict: dict) -> Thread:
            try:
                texts = []
                for fragment in obj_dict['first_post_content']:
                    ftype = int(fragment['type'])
                    if ftype in [0, 4, 9, 18]:
                        texts.append(fragment['text'])
                    elif ftype == 1:
                        texts.append(
                            f"{fragment['link']} {fragment['text']}")
                first_floor_text = ''.join(texts)

                if isinstance(obj_dict['agree'], dict):
                    like = int(obj_dict['agree']['agree_num'])
                    dislike = int(obj_dict['agree']['disagree_num'])
                else:
                    like = 0
                    dislike = 0

                author_id = int(obj_dict['author_id'])
                thread = Thread(fid=fid,
                                tid=int(obj_dict['tid']),
                                pid=int(obj_dict['first_post_id']),
                                user=users.get(author_id, UserInfo()),
                                title=obj_dict['title'],
                                first_floor_text=first_floor_text,
                                has_audio=True if obj_dict.get(
                                    'voice_info', None) else False,
                                has_video=True if obj_dict.get(
                                    'video_info', None) else False,
                                view_num=int(obj_dict['view_num']),
                                reply_num=int(obj_dict['reply_num']),
                                like=like,
                                dislike=dislike,
                                create_time=int(obj_dict['create_time']),
                                last_time=int(obj_dict['last_time_int'])
                                )
                return thread

            except Exception as err:
                log.error(
                    f"Failed to init Thread in {fid}. reason:{traceback.format_tb(err.__traceback__)[-1]}")
                return Thread()

        if main_json:
            try:
                self.current_pn = int(main_json['page']['current_page'])
                self.total_pn = int(main_json['page']['total_page'])
                fid = int(main_json['forum']['id'])
            except Exception as err:
                raise ValueError(
                    f"Null value at line {err.__traceback__.tb_lineno}")

            users = {int(user_dict['id']): _init_userinfo(user_dict)
                     for user_dict in main_json['user_list']}
            self._objs = [_init_obj(obj_dict)
                          for obj_dict in main_json['thread_list']]

        else:
            self._objs = []
            self.current_pn = 0
            self.total_pn = 0


class Post(BaseContent):
    """
    楼层信息

    text: 所有文本
    fid: 所在吧id
    tid: 帖子编号
    pid: 回复编号
    user: UserInfo类 发布者信息
    content: 正文
    sign: 小尾巴
    imgs: 图片列表
    smileys: 表情列表
    has_audio: 是否含有音频
    floor: 楼层数
    reply_num: 楼中楼回复数
    like: 点赞数
    dislike: 点踩数
    create_time: 10位时间戳，创建时间
    is_thread_owner: 是否楼主
    """

    __slots__ = ['content', 'sign', 'imgs', 'smileys', 'has_audio', 'floor',
                 'reply_num', 'like', 'dislike', 'create_time', 'is_thread_owner']

    def __init__(self, fid: int = 0, tid: int = 0, pid: int = 0, user: UserInfo = UserInfo(), content: str = '', sign: str = '', imgs: list[str] = [], smileys: list[str] = [], has_audio: bool = False, floor: int = 0, reply_num: int = 0, like: int = 0, dislike: int = 0, create_time: int = 0, is_thread_owner: bool = False):
        super().__init__(fid=fid, tid=tid, pid=pid, user=user)
        self.content = content
        self.sign = sign
        self.imgs = imgs
        self.smileys = smileys
        self.has_audio = has_audio
        self.floor = floor
        self.reply_num = reply_num
        self.like = like
        self.dislike = dislike
        self.create_time = create_time
        self.is_thread_owner = is_thread_owner

    @property
    def text(self) -> str:
        if not self._text:
            self._text = f'{self.content}\n{self.sign}'
        return self._text


class Posts(BaseContents[Post]):
    """
    post列表

    current_pn: 当前页数
    total_pn: 总页数
    """

    __slots__ = []

    def __init__(self, main_json: Optional[dict] = None):

        def _init_userinfo(user_dict: dict) -> UserInfo:
            try:
                user_id = int(user_dict['id'])
                if not user_id:
                    return UserInfo()
                priv_sets = user_dict['priv_sets']
                if not priv_sets:
                    priv_sets = {}
                user = UserInfo(user_name=user_dict['name'],
                                nick_name=user_dict['name_show'],
                                portrait=user_dict['portrait'],
                                user_id=user_id,
                                level=user_dict['level_id'],
                                gender=user_dict['gender'],
                                is_vip=bool(user_dict['new_tshow_icon']),
                                is_god=user_dict['new_god_data']['field_id'] != '',
                                priv_like=priv_sets.get('like', None),
                                priv_reply=priv_sets.get('reply', None)
                                )
                return user

            except Exception as err:
                log.error(
                    f"Failed to init UserInfo of {user_id} in {tid}. reason:{traceback.format_tb(err.__traceback__)[-1]}")
                return UserInfo()

        def _init_obj(obj_dict: dict) -> Post:
            try:
                texts = []
                imgs = []
                smileys = []
                has_audio = False
                for fragment in obj_dict['content']:
                    ftype = int(fragment.get('type', 0))
                    if ftype in [0, 4, 9, 18]:
                        texts.append(fragment['text'])
                    elif ftype == 1:
                        texts.append(fragment['link'])
                        texts.append(' ' + fragment['text'])
                    elif ftype == 2:
                        smileys.append(fragment['text'])
                    elif ftype == 3:
                        imgs.append(fragment['origin_src'])
                    elif ftype == 10:
                        has_audio = True
                content = ''.join(texts)

                author_id = int(obj_dict['author_id'])
                post = Post(fid=fid,
                            tid=tid,
                            pid=int(obj_dict['id']),
                            user=users.get(author_id, UserInfo()),
                            content=content,
                            sign=''.join([sign['text'] for sign in obj_dict['signature']['content']
                                         if sign['type'] == '0']) if obj_dict.get('signature', None) else '',
                            imgs=imgs,
                            smileys=smileys,
                            has_audio=has_audio,
                            floor=int(obj_dict['floor']),
                            reply_num=int(obj_dict['sub_post_number']),
                            like=int(obj_dict['agree']['agree_num']),
                            dislike=int(obj_dict['agree']['disagree_num']),
                            create_time=int(obj_dict['time']),
                            is_thread_owner=author_id == thread_owner_id,
                            )

                return post

            except Exception as err:
                log.error(
                    f"Failed to init Post in {tid}. reason:{traceback.format_tb(err.__traceback__)[-1]}")
                return Post()

        if main_json:
            try:
                self.current_pn = int(main_json['page']['current_page'])
                self.total_pn = int(main_json['page']['total_page'])
                thread_owner_id = int(main_json['thread']['author']['id'])
                fid = int(main_json['forum']['id'])
                tid = int(main_json['thread']['id'])
            except Exception as err:
                raise ValueError(
                    f"Null value at line {err.__traceback__.tb_lineno}")

            users = {int(user_dict['id']): _init_userinfo(user_dict)
                     for user_dict in main_json['user_list']}
            self._objs = [_init_obj(obj_dict)
                          for obj_dict in main_json['post_list']]

        else:
            self._objs = []
            self.current_pn = 0
            self.total_pn = 0


class Comment(BaseContent):
    """
    楼中楼信息

    text: 正文
    fid: 所在吧id
    tid: 帖子编号
    pid: 回复编号
    user: UserInfo类 发布者信息
    like: 点赞数
    dislike: 点踩数
    has_audio: 是否含有音频
    create_time: 10位时间戳，创建时间
    smileys: 表情列表
    """

    __slots__ = ['smileys', 'has_audio', 'like', 'dislike', 'create_time']

    def __init__(self, fid: int = 0, tid: int = 0, pid: int = 0, user: UserInfo = UserInfo(), text: str = '', smileys: list[str] = [], has_audio: bool = False, like: int = 0, dislike: int = 0, create_time: int = 0):
        super().__init__(fid=fid, tid=tid, pid=pid, user=user)
        self._text = text
        self.smileys = smileys
        self.has_audio = has_audio
        self.like = like
        self.dislike = dislike
        self.create_time = create_time


class Comments(BaseContents[Comment]):
    """
    comment列表

    current_pn: 当前页数
    total_pn: 总页数
    """

    __slots__ = []

    def __init__(self, main_json: Optional[dict] = None):

        def _init_obj(obj_dict: dict) -> Comment:
            try:
                texts = []
                smileys = []
                has_audio = False
                for fragment in obj_dict['content']:
                    ftype = int(fragment['type'])
                    if ftype in [0, 4, 9]:
                        texts.append(fragment['text'])
                    elif ftype == 1:
                        texts.append(fragment['link'])
                        texts.append(' ' + fragment['text'])
                    elif ftype == 2:
                        smileys.append(fragment['text'])
                    elif ftype == 10:
                        has_audio = True
                text = ''.join(texts)

                user_dict = obj_dict['author']
                priv_sets = user_dict['priv_sets']
                if not priv_sets:
                    priv_sets = {}
                user = UserInfo(user_name=user_dict['name'],
                                nick_name=user_dict['name_show'],
                                portrait=user_dict['portrait'],
                                user_id=user_dict['id'],
                                level=user_dict['level_id'],
                                gender=user_dict['gender'],
                                is_vip=bool(user_dict['new_tshow_icon']),
                                is_god=user_dict['new_god_data']['field_id'] != '',
                                priv_like=priv_sets.get('like', None),
                                priv_reply=priv_sets.get('reply', None)
                                )

                comment = Comment(fid=fid,
                                  tid=tid,
                                  pid=int(obj_dict['id']),
                                  user=user,
                                  text=text,
                                  smileys=smileys,
                                  has_audio=has_audio,
                                  like=int(obj_dict['agree']['agree_num']),
                                  dislike=int(
                                      obj_dict['agree']['disagree_num']),
                                  create_time=int(obj_dict['time'])
                                  )
                return comment

            except Exception as err:
                log.error(
                    f"Failed to init Comment in {tid}. reason:{traceback.format_tb(err.__traceback__)[-1]}")
                return Comment()

        if main_json:
            try:
                self.current_pn = int(main_json['page']['current_page'])
                self.total_pn = int(main_json['page']['total_page'])
                fid = int(main_json['forum']['id'])
                tid = int(main_json['thread']['id'])
            except Exception as err:
                raise ValueError(
                    f"Null value at line {err.__traceback__.tb_lineno}")

            self._objs = [_init_obj(obj_dict)
                          for obj_dict in main_json['subpost_list']]

        else:
            self._objs = []
            self.current_pn = 0
            self.total_pn = 0

    @property
    def has_next(self) -> bool:
        return self.current_pn < self.total_pn


class At(object):
    """
    @信息

    text: 标题文本
    tieba_name: 帖子所在吧
    tid: 帖子编号
    pid: 回复编号
    user: UserInfo类 发布者信息
    create_time: 10位时间戳，创建时间
    """

    __slots__ = ['tieba_name', 'tid', 'pid', 'user', 'text', 'create_time']

    def __init__(self, tieba_name: str = '', tid: int = 0, pid: int = 0, user: UserInfo = UserInfo(), text: str = '', create_time: int = 0):
        self.tieba_name = tieba_name
        self.tid = tid
        self.pid = pid
        self.user = user
        self.text = text
        self.create_time = create_time
