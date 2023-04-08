import copy

from flask import Blueprint, jsonify, render_template
from flask import send_from_directory

from app.utils import *


bp = Blueprint('views', __name__)

meta = load_json_file(['data', 'meta.json'])
functions = load_json_file(['data', 'functions.json'])
prompts = load_json_file(['data', 'prompts.json'])
classes_tree = load_json_file(['data', 'class_tree.json'])

# print([f['function_id'] for f in functions])


# get function dict:
functions_dict = {f['function_id']: f for f in functions}


# class id to names,
cid_to_cnames = {}
def get_cname_dict(d):
    id = d['id']
    cnames = d['names']
    cid_to_cnames[id] = cnames
    children = d.get('children', None)
    if children is not None:
        for c in children:
            get_cname_dict(c)

for c in classes_tree:
    get_cname_dict(c)


# class id to icon_name, style
cid_to_icon_name = {}
cid_to_icon_style = {}
def get_cicon_dict(d):
    cid = d['id']
    icon_style = d.get('icon_style', None)
    icon_name = d.get('icon_name', None)
    if icon_name is not None:
        cid_to_icon_name[cid] = icon_name
        cid_to_icon_style[cid] = icon_style

    children = d.get('children', None)
    if children is not None:
        for c in children:
            get_cicon_dict(c)

for c in classes_tree:
    get_cicon_dict(c)

# function id to class name
# {'function_id': [{"eng": Code Development, "chn": "代码开发"}, ...]}
fid_to_cnames = {}
for f in functions:
    fid = f['function_id']
    cid_lst = f['class'] # a function can have many classes
    cnames_lst = [cid_to_cnames[cid] for cid in cid_lst]
    fid_to_cnames[fid] = cnames_lst


is_function_in_class_tree = True
if is_function_in_class_tree:

     # build class_function_dict
    from collections import defaultdict
    c_f_dict = defaultdict(set)
    for f in functions:
        c_lst = f['class']
        fid = f['function_id']
        for c in c_lst:
            c_f_dict[c].add(fid)


    # change the function class
    for f in functions:
        f['class'].append(f['function_id'])

   
    # change the class tree, mount the function as the second class 
    def mount_function_in_class_tree(d: dict):
        cid = d['id']
        # print('##', cid_to_cnames[cid]['chn'])
        if cid == 'office': return 0# do not conduct for office
        children_lst = []
        fid_lst = c_f_dict.get(cid, [])
        for fid in fid_lst:
            # print('###', functions_dict[fid]['desc']['chn'])
            names = functions_dict[fid]['desc']
            tmp = {'id': fid, 'names': names}
            children_lst.append(tmp)
        d['children'] = children_lst
    
    for c in classes_tree:
        mount_function_in_class_tree(c)



@bp.route('/')
@bp.route('/index')
def index():
    return render_template('index.html')

@bp.route('/baidu_verify_codeva-1JQHTA7UR3')
@bp.route('/baidu_verify_codeva-1JQHTA7UR3.html')
def baidu_verify():
    return render_template('baidu_verify_codeva-1JQHTA7UR3.html')

@bp.route('/baidu_verify_codeva-kNM5HwgeNE')
@bp.route('/baidu_verify_codeva-kNM5HwgeNE.html')
def baidu_verify1():
    return render_template('baidu_verify_codeva-kNM5HwgeNE.html')

@bp.route('/BingSiteAuth')
@bp.route('/BingSiteAuth.xml')
def baidu_verify():
    return render_template('BingSiteAuth.xml')

# https://flask.palletsprojects.com/en/1.1.x/patterns/favicon/
@bp.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(bp.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


@bp.route('/fetch_meta/<meta_name>')
def fetch_meta(meta_name):
    return jsonify({"content": meta[meta_name], "message": "success"})


# @bp.route('/fetch_class/<param>')
# def fetch_class(param):
#     if param == 'with_example':
#         result = []
#         for item in copy.deepcopy(classes):
#             one_class = item
#             class_id = one_class['id']
#             for function in functions: # 遍历所有的function，找到属于某个class的function
#                 if class_id in function['class']:
#                     one_class['example'] = function
#                     break
#             result.append(one_class)
#     elif param == 'raw':
#         result = classes
#     else:
#         return jsonify({"message": f'Invalid parameter "{param}"'})
#     return jsonify({"content": result, "message": "success"})


# @bp.route('/fetch_meta/<meta_name>')
# def fetch_class_(meta_name):
#     return jsonify({"content": meta[meta_name], "message": "success"})


# By Haomin Wen
@bp.route('/fetch_tree/')
def fetch_tree():

    result = copy.deepcopy(classes_tree)

    return jsonify({"content": result, "message": "success"})

@bp.route('/fetch_prompt/<class_id>/<lan_code>')
def fetch_prompt(class_id, lan_code):
    result = []

    # find all funcions that has the class
    if class_id == 'all_class' or class_id == 'popular':
        f_lst = [f['function_id'] for f in functions]
    else:
        f_lst = [f['function_id'] for f in functions if class_id in f['class']]

    # find all prompts that has the function
    for data in prompts:
        fid = data['function_id']
        if fid not in f_lst: continue
        for p in data['content'][lan_code]:
            # prompt filter condition
            if class_id=='popular' and int(p['priority']) != 2: continue  # priority=2, means popular

            tmp = get_prompt_info_for_render(fid, p, lan_code)

            result.append(tmp)
    return jsonify({"content": result, "message": "success"})


def get_prompt_info_for_render(fid: str, p: dict, lan_code: str):
    tmp = {}
    tmp['chat_list'] = [p['content']]
    tmp['class_list'] = [name[lan_code] for name in fid_to_cnames[fid]]  # get class names
    tmp['author'] = p.get('author', '')
    if tmp['author'] == 'whm': tmp['author'] = ''
    tmp['author_link'] = p.get('author_link', '')
    tmp['model'] = p.get('model', 'GPT 3.5')
    tmp['function_desc'] = functions_dict[fid]['desc'][lan_code]

    # get one class icon
    tmp['icon_style'] = 'mdui-icon material-icons mdui-text-color-blue'
    tmp['icon_name'] = 'lightbulb_outline'
    cid_lst = functions_dict[fid]['class']
    for cid in cid_lst:
        cid_style = cid_to_icon_style.get(cid, None)
        cid_name = cid_to_icon_name.get(cid, None)
        if (cid_name is not None) and (cid_style is not None):
            tmp['icon_style'] = cid_style
            tmp['icon_name'] = cid_name

    return  tmp



@bp.route('/search_prompt/<search_text>/<lan_code>')
def search_prompt(search_text, lan_code):
    result = []

    for data in prompts:
        fid = data['function_id']
        if fid not in functions_dict.keys(): continue
        function_desc = functions_dict[fid]['desc'][lan_code]
        class_list = [name[lan_code] for name in fid_to_cnames[fid]] 
        for p in data['content'][lan_code]:
            p_text = p['content'][0]

            # also take output the class label
            compare_text_lst = class_list + [p_text, function_desc]

            for c_text in compare_text_lst:
                score  = text_similarity_score(search_text, c_text, lan_code)
                if score > 0.5:

                    tmp = get_prompt_info_for_render(fid, p, lan_code)

                    result.append(tmp)
                    continue
    return jsonify({"content": result, "message": "success"})


# remove duplicate value

# one function can have many class. Add a class, popular: 
# 1) add  popular in classes.json
# {
#     "id": "popular",
#     "names": {
#         "chn": "popular",
#         "eng": "popular",
#         "jpn": "popular",
#         "fra": "popular",
#         "kor": "popular",
#         "deu": "popular"
#     }
# },



# 3) add popular into the class_level.json
#  {
#         "id": "popular",
#         "icon_style": "mdui-list-item-icon mdui-icon material-icons mdui-text-color-blue",
#         "icon_name": "code",
#         "names": {
#             "chn": "popular",
#             "eng": "popular",
#             "jpn": "popular",
#             "fra": "popular",
#             "kor": "popular",
#             "deu": "popular"
#         }
#     },

# 3) add popular data into prompts.json
# solutioin 2: change the  fetch_prompt function, iter all prompts to check its priority, if priority = 2, it is popular
# priority = 0, normal 
# priority = 1, good, 
# priority = 2, popular
# priority = 3, precious, do do show


















