# -*- coding:utf-8 -*-
import csv
import re
import time

import tiebaBrowser as tb
brow = tb.Browser('default')

csv_file = open(f"asoul_bawu_vote_{time.time()}.csv", 'w', encoding='utf-8-sig', newline='')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['tid', 'floor', 'user_name', 'vote_num'])

tids = [7500446777, 7500484762, 7500514763]
user_name_exp = re.compile('@(.+)')
vote_res_list = []

start_time = time.time()
for tid in tids:
    for post_pn in range(1, 3):
        posts = brow.get_posts(tid, post_pn)

        for post in posts:
            if not post.is_thread_owner:
                continue
            user_name_obj = user_name_exp.search(post.text)
            if user_name_obj is None:
                continue
            user_name = user_name_obj.group(1)
            vote_set = set()

            for comment_pn in range(1, 0xff):
                comments = brow.get_comments(tid, post.pid, comment_pn)
                for comment in comments:
                    if comment.user.level < 8:
                        continue
                    if '支持' not in comment.text:
                        tb.log.warning(
                            f"Incorrect format. tid:{tid} floor:{post.floor} author:{comment.user.logname} text:{comment.text}")
                        continue
                    vote_set.add(comment.user.portrait)

                if not comments.has_next:
                    break

            vote_res = [tid, post.floor, user_name, len(vote_set)]
            tb.log.info(vote_res)
            vote_res_list.append(vote_res)

        if not posts.has_next:
            break

tb.log.info(f"IO time cost:{time.time()-start_time:.4f}")

# Sort accroding to [3]:vote_num
vote_res_list.sort(key=lambda row: row[3], reverse=True)
csv_writer.writerows(vote_res_list)
csv_file.close()
