import pymysql

db = pymysql.connect(
    # 本机使用localhost，服务器使用ip地址
    host='localhost',
    # 用户名，如变动请按变动后修改
    user='root',
    # 密码，如变动请按变动后修改
    password='mclab236',
    # 数据库名，如变动请按变动后修改
    database='nstcdb')

#模糊搜索entity
def SearchSQL1(search_text):
    if search_text :
        sql = "select * from entity where name like '%" + search_text + "%' or ID like '%"+ search_text + "%'"
    elif not search_text :
        sql = "select * from entity"
        print(sql)
    # sql = "select * from entity where name like '%nrg%'"

    try:
        cursor = db.cursor()
        cursor.execute(sql)
        results = cursor.fetchall()
        print(results)
        #print(results[1][1])

    except:
        print("no return")
        res_table = []

    else:
        i = 0
        res_table = []
        for x in results:
            res_dic = {
                "Name": results[i][0],
                "Full_Name": results[i][1],
                "Kind": results[i][2],
                "ID": results[i][3]
            }
            # res_dic["Name"] = results[i][0]
            # res_dic["Full_Name"] = results[i][1]
            # res_dic["Kind"] = results[i][2]
            # res_dic["ID"] = results[i][3]
            res_table.append(res_dic)
            i = i+1
    # print("sqlcon", res_table)
    return res_table

#精准搜索entity，搜索关键词是name
def SearchSQLen(search_text):
    if search_text :
        sql = "select * from entity where name like '" + search_text + "'"
    elif not search_text :
        sql = "select * from entity"
        print(sql)
    # sql = "select * from entity where name like '%nrg%'"

    try:
        cursor = db.cursor()
        cursor.execute(sql)
        results = cursor.fetchall()
        print(results)
        #print(results[1][1])

    except:
        print("no return")
        res_table = []

    else:
        i = 0
        res_table = []
        for x in results:
            res_dic = {
                "Name": results[i][0],
                "Full_Name": results[i][1],
                "Kind": results[i][2],
                "ID": results[i][3]
            }
            # res_dic["Name"] = results[i][0]
            # res_dic["Full_Name"] = results[i][1]
            # res_dic["Kind"] = results[i][2]
            # res_dic["ID"] = results[i][3]
            res_table.append(res_dic)
            i = i+1
    # print("sqlcon", res_table)
    return res_table


#模糊搜索st_interact
def SearchSQL2(search_text):
    if search_text:
        sql = "select * from st_interact where st_number like '%" + search_text + "%' or stimulator like '%" + search_text + "%' or acceptor like '%" + search_text + "%'"
    elif not search_text :
        sql = "select * from st_interact"

    try:
        cursor = db.cursor()
        cursor.execute(sql)
        results = cursor.fetchall()
        print(results)
        # print(results[1][1])

    except:
        print("no return")
        res_table = []

    else:
        i = 0
        res_table = []
        for x in results:
            res_dic = {
                "st_code": results[i][0],
                "Stimulator": results[i][1],
                "Acceptor": results[i][2]
            }
            # res_dic["Name"] = results[i][0]
            # res_dic["Full_Name"] = results[i][1]
            # res_dic["Kind"] = results[i][2]
            # res_dic["ID"] = results[i][3]
            res_table.append(res_dic)
            i = i + 1
            # print("sqlcon", res_table)
        return res_table


#精准搜索st_interact，关键词是st_number
def SearchSQLstnum(search_text):
    if search_text:
        sql = "select * from st_interact where st_number like '" + search_text + "'"
    elif not search_text :
        sql = "select * from st_interact"

    try:
        cursor = db.cursor()
        cursor.execute(sql)
        results = cursor.fetchall()
        # print("here!")
        # print(results)
        # print(results[1][1])

    except:
        print("no return")
        res_table = []

    else:
        i = 0
        res_table = []
        for x in results:
            res_dic = {
                "st_code": results[i][0],
                "Stimulator": results[i][1],
                "Acceptor": results[i][2]
            }
            # res_dic["Name"] = results[i][0]
            # res_dic["Full_Name"] = results[i][1]
            # res_dic["Kind"] = results[i][2]
            # res_dic["ID"] = results[i][3]
            res_table.append(res_dic)
            i = i + 1
            # print("sqlcon", res_table)
        return res_table


#精准搜索st_interact，关键词是entity,作为stimulator
def SearchSQLstSti(search_text):
    if search_text:
        sql = "select * from st_interact where stimulator like '" + search_text + "'"
    elif not search_text :
        sql = "select * from st_interact"

    try:
        cursor = db.cursor()
        cursor.execute(sql)
        results = cursor.fetchall()
        # print(results)
        # print(results[1][1])

    except:
        print("no return")
        res_table = []

    else:
        i = 0
        res_table = []
        for x in results:
            res_dic = {
                "st_code": results[i][0],
                "Stimulator": results[i][1],
                "Acceptor": results[i][2]
            }
            # res_dic["Name"] = results[i][0]
            # res_dic["Full_Name"] = results[i][1]
            # res_dic["Kind"] = results[i][2]
            # res_dic["ID"] = results[i][3]
            res_table.append(res_dic)
            i = i + 1
            # print("sqlcon", res_table)
        return res_table


#精准搜索st_interact，关键词是entity,作为acceptor
def SearchSQLstAcc(search_text):
    if search_text:
        sql = "select * from st_interact where acceptor like '" + search_text + "'"
    elif not search_text :
        sql = "select * from st_interact"

    try:
        cursor = db.cursor()
        cursor.execute(sql)
        results = cursor.fetchall()
        # print(results)
        # print(results[1][1])

    except:
        print("no return")
        res_table = []

    else:
        i = 0
        res_table = []
        for x in results:
            res_dic = {
                "st_code": results[i][0],
                "Stimulator": results[i][1],
                "Acceptor": results[i][2]
            }
            # res_dic["Name"] = results[i][0]
            # res_dic["Full_Name"] = results[i][1]
            # res_dic["Kind"] = results[i][2]
            # res_dic["ID"] = results[i][3]
            res_table.append(res_dic)
            i = i + 1
            # print("sqlcon", res_table)
        return res_table


#search pathway,模糊
def SearchSQL3(search_text):
    if search_text:
        sql = "select * from pathway where pathway like '%" + search_text + "%'"
    elif not search_text:
        sql = "select * from pathway"

    try:
        cursor = db.cursor()
        cursor.execute(sql)
        results = cursor.fetchall()
        # print(results)

    except:
        print("no return")
        res_table = []

    else:
        i = 0
        res_table = []
        for x in results:
            res_dic = {
                "pathway_number": results[i][0],
                "length": results[i][1],
                "pathway": results[i][2]
            }
            # res_dic["Name"] = results[i][0]
            # res_dic["Full_Name"] = results[i][1]
            # res_dic["Kind"] = results[i][2]
            # res_dic["ID"] = results[i][3]
            res_table.append(res_dic)
            i = i + 1
            # print("sqlcon", res_table)
        return res_table

#pathway精准
def SearchSQLpnum(search_text):
    if search_text:
        sql = "select * from pathway where pathway_number like " + str(search_text)
    elif not search_text:
        sql = "select * from pathway"

    try:
        cursor = db.cursor()
        cursor.execute(sql)
        results = cursor.fetchall()

    except:
        print("no return")
        res_table = []

    else:
        i = 0
        res_table = []
        for x in results:
            res_dic = {
                "pathway_number": results[i][0],
                "length": results[i][1],
                "pathway": results[i][2]
            }
            # res_dic["Name"] = results[i][0]
            # res_dic["Full_Name"] = results[i][1]
            # res_dic["Kind"] = results[i][2]
            # res_dic["ID"] = results[i][3]
            res_table.append(res_dic)
            i = i + 1
        return res_table


#搜索pathway中每一个interaction的detail
def SearchSQLpcontent(search_text):
    #先将pathwaynum转换为pathway
    pway = SearchSQLpnum(search_text)[0]
    stcode_list = []
    k = 0
    str1 = ""
    for j in pway['pathway']:
        #print(j)
        if j == ',':
            stcode_list.append(str1)
            str1 = ""
            k += 1
        else:
            str1 = str1 + j

    stcode_list.append(str1)

    #然后search每一个元素
    st_list = []
    for stcode in stcode_list:
        st_inter = SearchSQLstnum(stcode)[0]
        st_list.append(st_inter)
    return st_list

#搜索pathway中每一个interaction的detail
def SearchSQLpwcontent(stcode_list):
    #输入是stcode串
    #然后search每一个元素
    st_list = []
    for stcode in stcode_list:
        st_inter = SearchSQLstnum(stcode)[0]
        st_list.append(st_inter)
    return st_list