# Tieba-Manager

[![gitee](https://badgen.net/badge/mirror/gitee/red)](https://gitee.com/Starry-OvO/Tieba-Manager)
[![license](https://badgen.net/github/license/Starry-OvO/Tieba-Manager?icon=github)](https://github.com/Starry-OvO/Tieba-Manager/blob/main/LICENSE)
[![release](https://badgen.net/github/release/Starry-OvO/Tieba-Manager?icon=github)](https://github.com/Starry-OvO/Tieba-Manager/releases)

## 功能概览

+ 按回复时间/发布时间/热门序获取贴吧主题帖/精华帖列表。支持获取带转发/投票/转发嵌套投票/各种卡片的主题帖信息
+ 获取带图片链接、小尾巴内容、点赞情况、用户信息（`用户名` `user_id` `portrait` `等级` `性别` `是否锁回复`）、每条回复的前排楼中楼（支持按`点赞数`排序）的回复列表
+ 获取带所有前述用户信息的楼中楼列表
+ 根据`用户名` `昵称` `portrait` `user_id`中的任一项反查其他用户信息
+ 使用小吧主、语音小编的`BDUSS`封禁用户3/10天，不论有没有`用户名`
+ 使用已被大吧主分配解封/恢复帖权限的吧务`BDUSS`解封/恢复帖
+ 使用吧务`BDUSS`拒绝所有申诉
+ 使用小吧主、语音小编的`BDUSS`删帖或屏蔽
+ 使用大吧主`BDUSS`推荐帖子到首页、移动帖子到指定分区、加精、撤精、置顶、撤置顶、添加黑名单、查看黑名单、取消黑名单
+ 获取用户主页信息、关注贴吧列表
+ 获取贴吧最新关注用户列表、等级排行榜
+ 使用`BDUSS`关注吧、签到吧、水帖

## 准备使用

+ 确保你的[`Python`](https://www.python.org/downloads/)版本为`3.10+`

+ 拉取代码

```bash
git clone https://github.com/Starry-OvO/Tieba-Manager.git
```

+ `pip`安装依赖

```bash
pip install aiohttp[speedups] protobuf aiomysql lxml beautifulsoup4 opencv-contrib-python
```

+ 修改`config/config-example.json`，填入你的`BDUSS`，将文件名修改为`config.json`

```json
{
    "BDUSS": {
        "default": "ABCDEFGai2LdUd5TTVHblhFeXoxdGyOVURGUE1OYzNqVXVRaWF-HnpGckRCNFJnRVFBQUFBJCQAAAAAAAAAAAEAAADiglQb0f3Osqmv0rbJ2QAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAMN6XGDDelxgc"
    }
}
```

## 尝试一下

```python
# -*- coding:utf-8 -*-
import asyncio

import tiebaBrowser as tb


async def main():
    # 使用键名"default"对应的BDUSS创建客户端
    async with tb.Browser("default") as brow:
        # 同时请求用户个人信息和asoul吧首页前30帖
        # asyncio.gather会为两个协程brow.get_self_info和brow.get_threads自动创建任务然后“合并”为一个协程
        # await释放当前协程持有的CPU资源并等待协程asyncio.gather执行完毕
        # 参考https://docs.python.org/zh-cn/3/library/asyncio-task.html#asyncio.gather
        user, threads = await asyncio.gather(brow.get_self_info(), brow.get_threads('asoul'))

    # 将获取的信息打印到日志
    tb.log.info(f"当前用户信息: {user}")
    for thread in threads:
        tb.log.info(f"tid: {thread.tid} 最后回复时间戳: {thread.last_time} 标题: {thread.title}")


# 执行协程main
# 参考https://docs.python.org/zh-cn/3/library/asyncio-task.html#asyncio.run
asyncio.run(main())

```

## 若要开启云审查功能

+ 在`config/config.json`中配置`database`字段。你需要一个`MySQL`数据库用来缓存通过检测的回复的pid以及记录黑、白名单用户
+ 在`config/config.json`中配置`tieba_name_mapping`字段。你需要为每个贴吧设置对应的英文名以方便建立数据库
+ 使用函数`Database.init_database()`一键建库
+ 自定义审查行为：请参照我给出的例子自己编程修改[`cloud_review_asoul.py`](https://github.com/Starry-OvO/Tieba-Manager/blob/main/cloud_review_asoul.py)，这是被实际应用于[`asoul吧`](https://tieba.baidu.com/f?ie=utf-8&kw=asoul)的云审查工具
+ 编写用于一键重启的bash脚本。下面是我用的`restart.sh`，需要重启时就`bash restart.sh`就行了

```bash
#! /bin/bash
pids=`ps -ef | grep "\.py" | grep -v grep | awk '{print $2}'`
if [ -n "$pids" ]; then
    kill $pids
fi

TIEBA_MANAGER_PATH="$HOME/Scripts/Tieba-Manager"
nohup python $TIEBA_MANAGER_PATH/admin_listen.py >/dev/null 2>&1 &
nohup python $TIEBA_MANAGER_PATH/cloud_review_asoul.py >/dev/null 2>&1 &
nohup python $TIEBA_MANAGER_PATH/cloud_review_diana.py >/dev/null 2>&1 &
```

## 友情链接

+ [百度贴吧接口合集](https://github.com/Starry-OvO/Tieba-Manager/blob/main/tiebaBrowser/_api.py)
+ [云审查案例](https://github.com/Starry-OvO/Tieba-Manager/blob/main/cloud_review_asoul.py)
+ [指令管理器](https://github.com/Starry-OvO/Tieba-Manager/wiki/%E6%8C%87%E4%BB%A4%E7%AE%A1%E7%90%86%E5%99%A8%E4%BD%BF%E7%94%A8%E8%AF%B4%E6%98%8E%E4%B9%A6)
+ [另一个仍在活跃更新的贴吧管理器（有用户界面）](https://github.com/dog194/TiebaManager)
+ [客户反馈（我的个人吧）](https://tieba.baidu.com/f?ie=utf-8&kw=starry)

## 用户名单

云审查工具&指令管理器已在以下贴吧应用（2022.05.14更新，按启用时间先后排序）

|      吧名      | 关注用户数 | 最近29天日均访问量 | 日均主题帖数 | 日均回复数 |
| :------------: | :--------: | :----------------: | :----------: | :--------: |
|     asoul      |  158,488   |      217,206       |    2,219     |   21,158   |
| vtuber自由讨论 |   16,180   |       3,702        |      4       |    107     |
|      嘉然      |   51,617   |       19,215       |     221      |   2,732    |
|      宫漫      | 1,221,944  |       63,064       |     371      |   4,948    |
|    lol半价     | 1,925,712  |      175,435       |     499      |   10,590   |
|     孙笑川     | 1,798,618  |      526,787       |    5,557     |  146,327   |
|      向晚      |   25,296   |       12,693       |     168      |   1,656    |
|      贝拉      |   20,300   |       15,599       |     118      |   1,985    |
|    王力口乐    |   8,112    |       28,625       |     457      |   5,795    |
|      乃琳      |   15,528   |       8,020        |      65      |   1,085    |
