import ast
import json

from flask import Flask, render_template, request, redirect, url_for, jsonify
# render_template可以返回html，request获取浏览器发送给服务器的数据，redirect网页重定向
from sqlcon import SearchSQL1, SearchSQL2, SearchSQL3, SearchSQLen, SearchSQLstnum, SearchSQLstSti, SearchSQLstAcc, SearchSQLpnum, SearchSQLpcontent, SearchSQLpwcontent
# import sqlcon
from pathway_align import ST_similarity,CheckStlist,CheckEnlist,pw_similarity,FindPath
import jinja2
from calculate import calculate1

# print(12)
# print(res_table)

# 给Flask一个实例化对象,其中__name__入参是你的模块名或者包名，
# Flask应用会根据这个来确定你的应用路径以及静态文件和模板文件夹的路径
app = Flask(__name__, static_url_path='/STCDB/static')
# app.config["APPLICATION_ROOT"] = "/STCDB"
#app = Flask(__name__)
# 路由（@）

'''
@app.route('/STCDB/')
# /斜杠是访问路径
def hello_world():
    return "Hello World! " \
           "ARE YOU READY? " \
           "I CAN'T HEAR YOU! " \
           "Who live in a pineapple under the sea? " \
           "SPONGE BOB SQUARE PANTS!"
# 这里是返回hello world，正常来说要返回html页面
'''

@app.route('/homepage', methods=['GET', 'POST'])
def homepage():
    if request.method == 'POST':
        # request 对象可以拿到前端浏览器传递给服务器的所有数据
        search_text = request.form.get('search_text')
        input_type = request.form.get('input_type')
        # print('password是凑数的试一试', search_text, input_type)
        # 这里链接数据库进行搜索，搜索后返回结果；1有结果2无结果返回无结果页面
        global res_table
        if input_type == "1":
            res_table = SearchSQL1(search_text)
            # print("app", res_table)
            return redirect('/entity_search')
        elif input_type == "2":
            res_table = SearchSQL2(search_text)
            return redirect('/interaction_search')
        elif input_type == "3":
            res_table = SearchSQL3(search_text)
            return redirect('/pathway_search')
    return render_template("homepage.html")

@app.route('/manual')
def manual():
    img_quicksearch = 'quicksearch.png'
    img_alignsingle = 'alignsingle.png'
    img_alignmulti = 'alignmulti.png'
    img_alignresultcheck = 'alignresultcheck.png'
    img_pathwaydbcheck = 'pathwaydbcheck.png'
    img_network = 'network.png'
    img_keyfactor = 'keyfactor.png'
    img_navigation = 'navigation.png'
    return render_template("manual.html", img_quicksearch=img_quicksearch,
                           img_alignsingle=img_alignsingle, img_alignmulti=img_alignmulti,
                           img_alignresultcheck=img_alignresultcheck, img_pathwaydbcheck=img_pathwaydbcheck,
                           img_network=img_network, img_keyfactor=img_keyfactor, img_navigation=img_navigation)

@app.route('/')
def index():
    image_name = 'example.jpg'  # 图片文件名
    return render_template('index.html', image_name=image_name)


@app.route('/align', methods=['GET', 'POST'])
def to_align():
    if request.method == 'POST':
        # request 对象可以拿到前端浏览器传递给服务器的所有数据
        pathway0 = request.form.get('pathway0')
        new = request.form.getlist("new")
        return redirect(f'/align_result?pathway0={pathway0}&new={new}')
    return render_template("align.html")


#align结果
@app.route('/align_result')
def align_result():
    pathway0 = request.args.get('pathway0')
    new1 = request.args.get('new') #用new1接收传过来的字符串
    new = ast.literal_eval(new1)
    #print(type(new),new)

    # let's 挪移一下哈哈。
    if pathway0[0].isalpha() or pathway0[1].isalpha() or pathway0[2].isalpha():
        pw0 = CheckEnlist(pathway0)
    else:
        pw0 = CheckStlist(pathway0)
    pw0content = SearchSQLpwcontent(pw0)
    sim_result = []
    # 上面判断输入类型
    if len(new):
        # 有其他输入
        for pathway in new:
            if pathway[0].isalpha() or pathway[1].isalpha() or pathway[2].isalpha():
                pw = CheckEnlist(pathway)
            else:
                pw = CheckStlist(pathway)
            # 把结果转化成stcode串
            if pw == None:
                continue
            else:
                score = pw_similarity(pw0, pw)[0]
                if score > 0:
                    paths = pw_similarity(pw0, pw)[1]
                    pwcontent = SearchSQLpwcontent(pw)
                    sim_result.append({'pw': pw, 'score': score, 'paths': paths, 'pwcontent': pwcontent})
            # for结束，for是对每个pathway进行比较
        sim_result.sort(key=lambda x: x['score'], reverse=True)
    else:
        # 无其他输入，和database进行align
        pathwaydb = SearchSQL3(None)
        sim_result = []
        for pathway in pathwaydb:
            pw = CheckStlist(pathway['pathway'])  # 把结果转化成stcode串
            if pw:
                score = pw_similarity(pw0, pw)[0]
                if score > 0:
                    paths = pw_similarity(pw0, pw)[1]
                    pwcontent = SearchSQLpwcontent(pw)
                    sim_result.append({'pw': pw, 'score': score, 'paths': paths, 'pwcontent': pwcontent})
        # for结束，for是对每个pathway进行比较
        sim_result.sort(key=lambda x: x['score'], reverse=True)
        # ###我们需要解释一下这些东西。总之现在这些是传进去的东西，有这些这些东西。
    if request.method == 'POST':
        # request 对象可以拿到前端浏览器传递给服务器的所有数据
        pathway0 = request.form.get('pathway0')
        new = request.form.getlist("new")
        return redirect(f'/view_pathway?pathway0={pathway0}&new={new}')
    return render_template("align_result.html", sim_result=sim_result, pw0=pw0, pw0content=pw0content)


@app.route('/view_pathway', methods=['GET', 'POST'])
def draw_network():
    selected_results = request.args.get('selectedResults', '').split(',')
    pwlist = []
    pwtemp = []
    nodelist = []
    linklist = []
    #print("Selected Results:", selected_results)
    for stcode in selected_results:
        if stcode[-1] == ']':
            stcodetemp = stcode[2:-2]
            pwtemp.append(stcodetemp)
            pwlist.append(pwtemp)
            pwtemp = []
        # elif stcode[0] == '[':
            # stcodetemp = stcode[2:-1]
            # pwtemp.append(stcodetemp)
        # 发现首个和中间位置的code所取位置一样，主要是因为有空格啦；
        # 另外之所以把结尾判断放在最前面是因为如果先判断是否首个或中间的话，长度为一的pathway就会出问题。又修复了一个bug呢
        else:
            stcodetemp = stcode[2:-1]
            pwtemp.append(stcodetemp)
        # print(pwlist) 将结果分割成了二级列表了
        #下面顺便把这个stcodetemp的node和link搞了
        if linklist:
            flag = 0
            for link in linklist:
                if stcodetemp == link["label"]:
                    flag = 1 #已有的互作
                    index = linklist.index(link)    #已有互作在link列表里的index
            #上面的for是在判断是否已经有这个互作了
            if flag:
                linklist[index]["width"] += 3
                continue
            else:
                temp = SearchSQLstnum(stcodetemp)[0]
                newlink = {'label': stcodetemp, 'source': temp['Stimulator'], 'target': temp['Acceptor'], 'width': 3}
                linklist.append(newlink)
                if temp['Stimulator'] in nodelist:
                    if temp['Acceptor'] in nodelist:
                        continue
                    else:
                        nodelist.append(temp['Acceptor'])
                        continue
                else:
                    nodelist.append(temp['Stimulator'])
                    if temp['Acceptor'] in nodelist:
                        continue
                    else:
                        nodelist.append(temp['Acceptor'])
                        continue
        else:
            # print("stcodetemp")
            # print(stcodetemp)
            temp = SearchSQLstnum(stcodetemp)[0]
            newlink = {'label': stcodetemp, 'source': temp['Stimulator'], 'target': temp['Acceptor'], 'width': 3}
            linklist.append(newlink)
            nodelist.append(temp['Stimulator'])
            nodelist.append(temp['Acceptor'])

    pwlist_json = json.dumps(pwlist)
    nodelist_json = json.dumps(nodelist)
    linklist_json = json.dumps(linklist)
    if request.method == 'POST':
        # request 对象可以拿到前端浏览器传递给服务器的所有数据
        # return redirect(f'/calculate?pwlist={pwlist}&nodelist={nodelist}&linklist={linklist}&pwlist_json={pwlist_json}&nodelist_json={nodelist_json}&linklist_json={linklist_json}')
        return redirect(f'/calculate?nodelist_json={nodelist_json}&linklist_json={linklist_json}')
    return render_template("draw_network.html",
                           pwlist=pwlist, nodelist=nodelist, linklist=linklist,
                           pwlist_json=pwlist_json, nodelist_json=nodelist_json, linklist_json=linklist_json)

# 关键节点识别按钮那里
@app.route('/calculate', methods=['GET', 'POST'])
def do_calculation():
    # linklist = request.args.get('linklist')
    linklist_json = request.args.get('linklist_json')
    # nodelist = request.args.get('nodelist')
    nodelist_json = request.args.get('nodelist_json')
    # pwlist = request.args.get('pwlist')
    # pwlist_json = request.args.get('pwlist_json')

    net_data = json.loads(linklist_json)
    nodes = json.loads(nodelist_json)
    node_count = len(nodes)
    result = calculate1(net_data, node_count, nodes)
    # print("!!!!!")
    # print(result)
    '''return render_template('draw_network.html', result=result, pwlist=pwlist, pwlist_json=pwlist_json,
                           nodelist_json=nodelist_json, linklist_json=linklist_json,
                           nodelist=nodelist, linklist=linklist)'''
    return render_template('draw_network.html', result=result,
                           nodelist_json=nodelist_json, linklist_json=linklist_json)

# 搜索结果跳转
# 搜索结果的超链接-条目展示页面
@app.route('/entity_search')
def result_entity():
    # kwargs = {
    # "res_table": res_table
    # }
    return render_template("result_entity.html", res_table=res_table)

@app.route('/entity_detail/<res_id>')
def detail_entity(res_id):
    # kwargs = {
    # "res_table": res_table
    # }
    res_detail = SearchSQLen(res_id)[0]
    res_assti = SearchSQLstSti(res_id)
    res_asacc = SearchSQLstAcc(res_id)
    return render_template("detail_entity.html", res_id=res_id, res_asacc=res_asacc, res_detail=res_detail, res_assti=res_assti)


@app.route('/interaction_search')
def result_interact():
    # kwargs = {
    # "res_table": res_table
    # }
    return render_template("result_interact.html", res_table=res_table)

@app.route('/interaction_detail/<res_stnum>')
def detail_interact(res_stnum):
    # kwargs = {
    # "res_table": res_table
    # }
    res_detail = SearchSQLstnum(res_stnum)[0]
    res_inpath = SearchSQL3(res_stnum) #interaction 在哪些pathway里，字典列表
    for respath in res_inpath:
        stlist = SearchSQLpcontent(respath['pathway_number'])
        respath.update({'stlist': stlist}) #每个stlist是个字典列表
    # print("hh", res_inpath)
    return render_template("detail_interaction.html", res_stnum=res_stnum, res_inpath=res_inpath, res_detail=res_detail)



@app.route('/pathway_search')
def result_pathway():
    # kwargs = {
    # "res_table": res_table
    # }
    if request.method == 'POST':
        # request 对象可以拿到前端浏览器传递给服务器的所有数据
        pathway0 = request.form.get('pathway0')
        new = request.form.getlist("new")
        return redirect(f'/view_pathway_1?pathway0={pathway0}&new={new}')
    return render_template("result_pathway.html", res_table=res_table)

@app.route('/pathway_detail/<res_pnum>')
def detail_pathway(res_pnum):
    # kwargs = {
    # "res_table": res_table
    # }
    res_detail = SearchSQLpnum(res_pnum)[0]
    st_list = SearchSQLpcontent(res_pnum)
    return render_template("detail_pathway.html", res_pnum=res_pnum, res_detail=res_detail, st_list=st_list)


# 展示数据库
@app.route('/entitydb')
def entitydb():
    search_text = None
    res_table = SearchSQL1(search_text)
    return render_template("result_entity.html", res_table=res_table)


@app.route('/interactdb')
def interactdb():
    search_text = None
    res_table = SearchSQL2(search_text)
    return render_template("result_interact.html", res_table=res_table)

@app.route('/pathwaydb')
def pathwaydb():
    search_text = None
    res_table = SearchSQL3(search_text)
    return render_template("result_pathway.html", res_table=res_table)


@app.route('/view_pathway_1', methods=['GET', 'POST'])
def draw_network_1():
    selected_results = request.args.get('selectedResults', '').split(',')
    pwlist = []
    pwtemp = []
    nodelist = []
    linklist = []
    # print("Selected Results:", selected_results)
    for stcode in selected_results:
        stcodetemp = stcode
        pwtemp.append(stcodetemp)
        pwlist.append(pwtemp)
        if stcode == selected_results[-1]:
            pwtemp = []

        #下面顺便把这个stcodetemp的node和link搞了
        if linklist:
            flag = 0
            for link in linklist:
                if stcodetemp == link["label"]:
                    flag = 1 #已有的互作
                    index = linklist.index(link)    #已有互作在link列表里的index
            #上面的for是在判断是否已经有这个互作了
            if flag:
                linklist[index]["width"] += 3
                continue
            else:
                temp = SearchSQLstnum(stcodetemp)[0]
                newlink = {'label': stcodetemp, 'source': temp['Stimulator'], 'target': temp['Acceptor'], 'width': 3}
                linklist.append(newlink)
                if temp['Stimulator'] in nodelist:
                    if temp['Acceptor'] in nodelist:
                        continue
                    else:
                        nodelist.append(temp['Acceptor'])
                        continue
                else:
                    nodelist.append(temp['Stimulator'])
                    if temp['Acceptor'] in nodelist:
                        continue
                    else:
                        nodelist.append(temp['Acceptor'])
                        continue
        else:
            # print("stcodetemp")
            # print(stcodetemp)
            temp = SearchSQLstnum(stcodetemp)[0]
            newlink = {'label': stcodetemp, 'source': temp['Stimulator'], 'target': temp['Acceptor'], 'width': 3}
            linklist.append(newlink)
            nodelist.append(temp['Stimulator'])
            nodelist.append(temp['Acceptor'])

    pwlist_json = json.dumps(pwlist)
    nodelist_json = json.dumps(nodelist)
    linklist_json = json.dumps(linklist)
    # print(nodelist)
    if request.method == 'POST':
        # request 对象可以拿到前端浏览器传递给服务器的所有数据
        return redirect(f'/calculate?nodelist_json={nodelist_json}&linklist_json={linklist_json}')
    return render_template("draw_network.html", nodelist_json=nodelist_json, linklist_json=linklist_json)


# 运行
if __name__ == '__main__':
    app.run()
