import os
import re
import pandas as pd
from urllib.parse import quote

# 根据 frame 生成 Markdown 表格
def gen_markdown_table(frame, need_sort):
    
    ELEMENT = " {} |"

    H = frame.shape[0]
    W = frame.shape[1]

    LINE = "|" + ELEMENT * W

    head_name = ["题号", "标题", "题解", "标签", "难度"]

    lines = []

    ## 表头部分
    lines += [
        f"| {head_name[0]} | {head_name[1]} | {head_name[2]} | {head_name[3]} | {head_name[4]} |"
    ]


    ## 分割线
    SPLIT = ":{}"
    line = "|"
    for _ in range(W):
        line = f"{line} {SPLIT.format('-'*6)} |"
    lines += [line]

    ## 数据部分
    if need_sort:
        frame = frame.sort_values(by='题号')
    frame = frame.reset_index(drop=True)
    for i in range(H):
        lines += [
            f"| {frame.at[i, '题号']} | {frame.at[i, '标题']} | {frame.at[i, '题解']} | {frame.at[i, '标签']} | {frame.at[i, '难度']} |"
        ]

    return '\n'.join(lines)

# 根据题解目录 solotions_path 自动生成题解列表，并保存到 output_path 中
def gen_solutions_list(solotions_path, solotions_output_path):
    files =  os.listdir(solotions_path)
    frame = pd.DataFrame(columns=['题号', '标题', '题解', '标签', '难度'])
    frame_cout = 0
    for file in files:
        if not os.path.isdir(file) and ".md" in file: #判断是否是文件夹   
            with open(solotions_path + "/" + file) as f:
                lines = f.readlines()
                title_id = None
                title_offer_id = None
                title_offer_id1 = None
                title_offer_id2 = None
                title_name = None
                title_solution_url = None
                title_url = None
                title_label = None
                title_diff = None

                for i in range(len(lines)):
                    if i == 0:
                        pattern_1 = re.compile(r'\[剑指 Offer ([0-9]\d*|0)+( - [I]*)*\. (.*)\]\((.*)\)')
                        if re.search(pattern_1, lines[i]):
                            match_1 = pattern_1.finditer(lines[i])
                            for a in match_1:
#                            print(a)
                                title_offer_id1, title_offer_id2, title_name, title_url = a.group(1,2,3,4)
                                if title_offer_id2:
                                    title_offer_id = "剑指 Offer " + title_offer_id1 + title_offer_id2
                                else:
                                    title_offer_id = "剑指 Offer " + title_offer_id1
                            continue

                        pattern_2 = re.compile(r'\[剑指 Offer II ([0-9]\d*|0)+\. (.*)\]\((.*)\)')
                        if re.search(pattern_2, lines[i]):
                            match_2 = pattern_2.finditer(lines[i])
                            for a in match_2:
                                print(a)
                                title_offer_id1, title_name, title_url = a.group(1,2,3)
                                title_offer_id = "剑指 Offer II " + title_offer_id1
                            continue

                        pattern_3 = re.compile(r'\[面试题 ([0-9]\d*|0)+\.+([0-9]\d*|0)+\. (.*)\]\((.*)\)')
                        if re.search(pattern_3, lines[i]):
                            match_3 = pattern_3.finditer(lines[i])
                            for a in match_3:
                                print(a)
                                title_offer_id1, title_offer_id2, title_name, title_url = a.group(1,2,3,4)
                                title_offer_id = "面试题 " + title_offer_id1 + "." + title_offer_id2
                            continue


                        pattern = re.compile(r'\[([0-9]\d*|0)+\. (.*)\]\((.*)\)')
                        match = pattern.finditer(lines[i])
                        for a in match:
                            print(a)
                            title_id, title_name, title_url = a.group(1,2,3)
                    elif "标签" in lines[i]:
                        pattern = re.compile(r'- 标签：(.*)')
                        match = pattern.finditer(lines[i])
                        for a in match:
                            title_label = a.group(1)
                    elif "难度" in lines[i]:
                        pattern = re.compile(r'- 难度：(.*)')
                        match = pattern.finditer(lines[i])
                        for a in match:
                            title_diff = a.group(1)
                if not title_diff:
                    title_diff = "简单"
                if not title_label:
                    title_label = " "

                if title_offer_id and title_name and title_url and title_label and title_diff:
                    title_chinese = quote(title_offer_id + ". " + title_name + ".md")
                    title_solution_url = "[Python](https://github.com/itcharge/LeetCode-Py/blob/main/Solutions/" + title_chinese + ")"
                    title_name_url = "[" + title_name + "](" + title_url + ")"

                    frame.loc[frame_cout] = [title_offer_id, title_name_url, title_solution_url, title_label, title_diff]
                    frame_cout += 1
                    print(frame_cout, title_offer_id, title_name_url, title_url, title_label, title_diff, title_solution_url)
                elif title_id and title_name and title_url and title_label and title_diff:
                    title_id = "{:0>4d}".format(int(title_id))
                    title_chinese = quote(f"{title_id}. " + title_name + ".md")
                    title_solution_url = "[Python](https://github.com/itcharge/LeetCode-Py/blob/main/Solutions/" + title_chinese + ")"
                    title_name_url = "[" + title_name + "](" + title_url + ")"

                    frame.loc[frame_cout] = [title_id, title_name_url, title_solution_url, title_label, title_diff]
                    frame_cout += 1
                    print(frame_cout, title_id, title_name_url, title_url, title_label, title_diff, title_solution_url)    


    table = gen_markdown_table(frame, True)
    with open(solotions_output_path, 'w') as f:
        f.writelines("# LeetCode 题解（已完成 {} 道）\n\n".format(frame_cout))
        f.write(table)
    f.close()
    print("Create Solutions List Success")
    return frame_cout


# 将 readme_head、list 合并到，自动生成 README.md 并保存到 readme_path 中
def merge_readme_file(solotions_output_path, readme_head_path, readme_catalogue_list_path, content_index_path, readme_path, solutions_count):
    
    with open(readme_path,'w') as readme_file:
        with open(readme_head_path) as readme_head_file:
            readme_file.writelines(readme_head_file.readlines())
        with open(readme_catalogue_list_path) as readme_catelogue_list_file:
            readme_catelogue_list_lines = readme_catelogue_list_file.readlines()
            for readme_catelogue_list_line in readme_catelogue_list_lines:
                readme_catelogue_list_line = readme_catelogue_list_line.replace('https://github.com/itcharge/LeetCode-Py/blob/main', '.')
                readme_file.write(readme_catelogue_list_line)
        with open(solotions_output_path) as catalogue_list_file:
            catalogue_list_lines = catalogue_list_file.readlines()
            if len(catalogue_list_lines) > 0:
                catalogue_list_title = catalogue_list_lines[0].strip('\n')
                catalogue_list_title = '## [' + catalogue_list_title + '](./Contents/00.Introduction/04.Solutions-List.md)'
                catalogue_list_title = catalogue_list_title.replace('# LeetCode 题解', '10. LeetCode 题解')
                readme_file.writelines(catalogue_list_title)
    with open(content_index_path, 'w') as content_index_file:
        content_index_file.writelines("# 算法通关手册（LeetCode）\n\n")

        with open(readme_catalogue_list_path) as readme_catelogue_list_file:
            catalogue_list_lines = readme_catelogue_list_file.readlines()
            for catalogue_list_line in catalogue_list_lines:
                catalogue_list_line = catalogue_list_line.replace('https://github.com/itcharge/LeetCode-Py/blob/main/Contents', '.')
                content_index_file.write(catalogue_list_line)

# 根据题解目录, 题目分类原始列表目录，生成分类题解，并将整体保存到 categories_list_path
def gen_categories_list(solotions_path, categories_origin_list_path, categories_list_path):
    
    f = open(categories_origin_list_path)
    lines = f.readlines()
    category_h2 = None
    category_h3 = None
    category_h4 = None
    category_h6 = None
    category_h3_file_path = None
    category_h3_file_content = ""
    category_file_content = ""

    for i in range(len(lines)):
        pattern = re.compile(r'(#{2,6}) (.*)')
        if match := pattern.match(lines[i]):
            title_size, title_content =  match.group(1,2)
            if title_size == "##":
                category_h2 = title_content
                category_file_content += "## " + category_h2 + "\n\n"
            elif title_size == "###":
                if category_h3 and category_h3_file_path and category_h3_file_content:
#                    print(category_h3_file_content)
                    with open(category_h3_file_path, 'w') as fi:
                        fi.write(category_h3_file_content)
                    fi.close()
                    category_h3 = None
                    category_h3_file_path = None
                    category_h3_file_content = ""
                pattern1 = re.compile(r'\[(.*)\]\((.*)\)')
                if match1 := pattern1.match(title_content):
                    category_h3, category_h3_file_path = match1.group(1,2)
                    category_h3_file_content += "### " + category_h3 + "\n\n"
                else:
                    category_h3 = title_content
                category_file_content += "### " + category_h3 + "\n\n"
            elif title_size == "####":
                category_h4 = title_content
                category_h3_file_content += "#### " + category_h4 + "\n\n"
                category_file_content += "#### " + category_h4 + "\n\n"
            elif title_size == "######":
                category_h6 = title_content
                problem_ids = title_content.split('、')
                if not problem_ids:
                    continue

                frame = pd.DataFrame(columns=['题号', '标题', '题解', '标签', '难度'])
                frame_cout = 0
                for problem_id in problem_ids:
                    problem_id_path = solotions_path + "/" + problem_id + ".md"
                    if res := get_problem_id_row(problem_id_path, problem_id):
                        frame.loc[frame_cout] = res
                        frame_cout += 1
                table = gen_markdown_table(frame, False)
                category_h3_file_content += table + "\n\n"
                category_file_content += table + "\n\n"

    if category_h3 and category_h3_file_path and category_h3_file_content:
        with open(category_h3_file_path, 'w') as fi:
            fi.write(category_h3_file_content)
        fi.close()

    if category_file_content:
        with open(categories_list_path, 'w') as fi:
            fi.write(category_file_content)
        fi.close()

    print("Create Categories List Success")
        
        
# 根据本地题解目录，获取对应题目 id 编号对应的行
def get_problem_id_row(problem_id_path, problem_id):
    title_id = None
    title_offer_id = None
    title_offer_id1 = None
    title_offer_id2 = None
    title_name = None
    title_solution_url = None
    title_url = None
    title_label = None
    title_diff = None
    res = None

    # 本地不存在
    if not os.path.exists(problem_id_path):
        title_offer_id = ""
        pattern_1 = re.compile(r'剑指 Offer ([0-9]\d*|0)+( - [I]*)*\. (.*)')
        pattern_2 = re.compile(r'剑指 Offer II ([0-9]\d*|0)+\. (.*)')
        pattern_3 = re.compile(r'面试题 ([0-9]\d*|0)+\.+([0-9]\d*|0)+\. (.*)')
        pattern_4 = re.compile(r'([0-9]\d*|0)+\. (.*)')

        if re.search(pattern_1, problem_id):
            match_1 = pattern_1.finditer(problem_id)
            for a in match_1:
                title_offer_id1, title_offer_id2, title_name = a.group(1,2,3)
                if title_offer_id2:
                    title_offer_id = "剑指 Offer " + title_offer_id1 + title_offer_id2
                else:
                    title_offer_id = "剑指 Offer " + title_offer_id1
        elif re.search(pattern_2, problem_id):
            match_2 = pattern_2.finditer(problem_id)
            for a in match_2: 
                title_offer_id1, title_name = a.group(1,2)
                title_offer_id = "剑指 Offer II " + title_offer_id1
        elif re.search(pattern_3, problem_id):
            match_3 = pattern_3.finditer(problem_id)
            for a in match_3:
                title_offer_id1, title_offer_id2, title_name = a.group(1,2,3)
                title_offer_id = "面试题 " + title_offer_id1 + "." + title_offer_id2
        elif re.search(pattern_4, problem_id):
            match_4 = pattern_4.finditer(problem_id)
            for a in match_4:
                title_offer_id, title_name = a.group(1,2)

        title_chinese = " "
        title_solution_url = " "
        title_name_url = title_name
        title_label = " "
        title_diff = " "
        res = [title_offer_id, title_name_url, title_solution_url, title_label, title_diff]
        return res

    with open(problem_id_path) as f:
        lines = f.readlines()
        for i in range(len(lines)):
            if i == 0:
                pattern_1 = re.compile(r'\[剑指 Offer ([0-9]\d*|0)+( - [I]*)*\. (.*)\]\((.*)\)')
                pattern_2 = re.compile(r'\[剑指 Offer II ([0-9]\d*|0)+\. (.*)\]\((.*)\)')
                pattern_3 = re.compile(r'\[面试题 ([0-9]\d*|0)+\.+([0-9]\d*|0)+\. (.*)\]\((.*)\)')
                pattern_4 = re.compile(r'\[([0-9]\d*|0)+\. (.*)\]\((.*)\)')
                if re.search(pattern_1, lines[i]):
                    match_1 = pattern_1.finditer(lines[i])
                    for a in match_1:
                        title_offer_id1, title_offer_id2, title_name, title_url = a.group(1,2,3,4)
                        if title_offer_id2:
                            title_offer_id = "剑指 Offer " + title_offer_id1 + title_offer_id2
                        else:
                            title_offer_id = "剑指 Offer " + title_offer_id1
                elif re.search(pattern_2, lines[i]):
                    match_2 = pattern_2.finditer(lines[i])
                    for a in match_2: 
                        title_offer_id1, title_name, title_url = a.group(1,2,3)
                        title_offer_id = "剑指 Offer II " + title_offer_id1
                elif re.search(pattern_3, lines[i]):
                    match_3 = pattern_3.finditer(lines[i])
                    for a in match_3:
                        title_offer_id1, title_offer_id2, title_name, title_url = a.group(1,2,3,4)
                        title_offer_id = "面试题 " + title_offer_id1 + "." + title_offer_id2
                else:
                    match_4 = pattern_4.finditer(lines[i])
                    for a in match_4:
                        title_id, title_name, title_url = a.group(1,2,3)
            elif "标签" in lines[i]:
                pattern = re.compile(r'- 标签：(.*)')
                match = pattern.finditer(lines[i])
                for a in match:
                    title_label = a.group(1)
            elif "难度" in lines[i]:
                pattern = re.compile(r'- 难度：(.*)')
                match = pattern.finditer(lines[i])
                for a in match:
                    title_diff = a.group(1)
        if not title_diff:
            title_diff = "简单"
        if not title_label:
            title_label = " "

        if title_offer_id and title_name and title_url and title_label and title_diff:
            title_chinese = quote(title_offer_id + ". " + title_name + ".md")
            title_solution_url = "[Python](https://github.com/itcharge/LeetCode-Py/blob/main/Solutions/" + title_chinese + ")"
            title_name_url = "[" + title_name + "](" + title_url + ")"

            res = [title_offer_id, title_name_url, title_solution_url, title_label, title_diff]
        elif title_id and title_name and title_url and title_label and title_diff:
            title_id = "{:0>4d}".format(int(title_id))
            title_chinese = quote(f"{title_id}. " + title_name + ".md")
            title_solution_url = "[Python](https://github.com/itcharge/LeetCode-Py/blob/main/Solutions/" + title_chinese + ")"
            title_name_url = "[" + title_name + "](" + title_url + ")"

            res = [title_id, title_name_url, title_solution_url, title_label, title_diff]
        else:
            title_id = problem_id
            title_chinese = " "
            title_solution_url = " "
            title_name_url = " "
            title_label = " "
            title_diff = " "
            res = [title_id, title_name_url, title_solution_url, title_label, title_diff]
    return res