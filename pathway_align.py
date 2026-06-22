from sqlcon import SearchSQLstnum, SearchSQLstSti, SearchSQLstAcc
import numpy as np
import copy

#比较单独两个stcode
def ST_similarity(st1, st2):
    if st1 == st2:
        sim = 1
        return sim
    else:
        str = ''
        a = []
        b = []
        #将st1和st2（两个信号通路）转换为两个列表
        for i in st1:
            if i != '.':
                str = str + i
            else:
                a.append(str)
                str = ''
        a.append(str)
        str=''
        for j in st2:
            if j != '.':
                str = str + j
            else:
                b.append(str)
                str = ''
        b.append(str)

        #进行比较
        if a[0] != b[0]:
            sim = 0
        elif a[1] != b[1]:
            sim = 0.25
        elif a[2] != b[2]:
            sim = 0.5
        elif a[3] != b[3]:
            sim = 0.75
        else:
            sim = 1
        return sim


#检查实体串并转化为stcode串
def CheckEnlist(enlist):
    #字符串转化成列表，k为列表长度
    str2 = ''
    entities = []
    k = 1
    for i in enlist:
        if i != ',':
            #我决定让entity串也用逗号隔开嘿嘿
            str2 = str2 + i
        else:
            entities.append(str2)
            str2 = ''
            k += 1
    entities.append(str2)
    # print(entities)

    #转换成stcode串
    stcodes = []
    j = 0
    while j < k-1 :
        interactions = SearchSQLstSti(entities[j])
        find1 = False
        for interaction in interactions:
            if interaction['Acceptor'] == entities[j+1]:
                stcodes.append(interaction['st_code'])
                j += 1
                find1 = True
                break
                #normal situation，break for
            else:
                continue

        if find1:
            continue
            #正常的找到了，next while
        else:
            #没找到的话给个挽救的机会
            interactions2 = SearchSQLstAcc(entities[j+1])
            find2 = False
            for interaction2 in interactions2:
                for interaction in interactions:
                    if interaction['Acceptor'] == interaction2['Stimulator']:
                        stcodes.append(interaction['st_code'])
                        stcodes.append(interaction2['st_code'])
                        find2 = True
                        break #break 了最里面的for
                        #中间多一个的情况
                    else:
                        continue
                if find2:
                    break
                    #找到了的话，结束第一层for
                else:
                    continue
                    #没找到的话下一层
            #两层for循环结束，找到了吗？
            if find2:
                j += 1
                continue #这个entity找完了，下一个,break了interaction的for
            else:
                #找不到呀直接none
                return None

    return stcodes


#检查stcode串
def CheckStlist(stlist):
    #字符串转化成列表，k为长度
    str1 = ''
    stcodes = []
    k = 1
    for i in stlist:
        if i != ',':
            str1 = str1 + i
        else:
            stcodes.append(str1)
            str1 = ''
            k += 1
    stcodes.append(str1)

    #检查连接并给出结果
    j = 0
    while j < k-1 :
        last_acc = SearchSQLstnum(stcodes[j])[0]['Acceptor']
        #print('——————error!——————————————————————————',k-1,j+1,stcodes[j+1],SearchSQLstnum(stcodes[j+1]))
        next_sti = SearchSQLstnum(stcodes[j+1])[0]['Stimulator']
        if last_acc == next_sti:
            j += 1 #没问题，下一个
            continue
        else:
            #寻找是否有中间的连接
            interactions = SearchSQLstSti(last_acc)
            new_stcode = None
            for sts in interactions:
                if sts['Acceptor'] == next_sti:
                    new_stcode = sts['st_code']
                    break
                else:
                    continue
            if new_stcode:
                stcodes.insert(j+1, new_stcode)
                j += 2
            else:
                #break
                return None #没有合适的，不给搞了
    return stcodes


#find path的递归函数
def FindPath(i, j, s_mat, path, OnePath, AllPaths):
    if all(path[i][j] == [0,0,0]):
        OnePath.append((i, j, s_mat[i][j]))
        AllPaths.append(copy.deepcopy(OnePath))
        OnePath.pop()
    else:
        for k in range(3):
            if path[i,j,k] == 1:
                if k == 2:
                    OnePath.append((i,j,s_mat[i][j]-s_mat[i-1][j-1]))
                    FindPath(i-1, j-1, s_mat, path, OnePath, AllPaths)
                    OnePath.pop()
                elif k == 1:
                    OnePath.append((i,j,2))
                    #用2表示在pathway1添加gap
                    FindPath(i-1, j, s_mat, path, OnePath, AllPaths)
                    OnePath.pop()
                elif k == 0:
                    OnePath.append((i,j,3))
                    #用3表示在pathway2添加gap
                    FindPath(i, j-1, s_mat, path, OnePath, AllPaths)
                    OnePath.pop()


#比较两条通路，输入是两个stcodes列表
def pw_similarity(pathway1, pathway2):
    #gap = 0
    m = len(pathway1)
    n = len(pathway2)
    L = max(m,n)
    s_mat = np.zeros((m, n))
    path = np.zeros((m,n,3))

    for i in range(0,m):
        for j in range(0,n):
            match = ST_similarity(pathway1[i], pathway2[j])
            if i == 0 and j == 0:
                s_mat[i][j] = match
                #起点的match
            elif i-1 < 0:
                #第一行
                s_mat[i][j] = max(match, s_mat[i][j-1])
                if s_mat[i][j-1] == s_mat[i][j]:
                    path[i,j,0] = 1
            elif j-1 < 0:
                # 第一列
                s_mat[i][j] = max(match, s_mat[i-1][j])
                if s_mat[i-1][j] == s_mat[i][j]:
                    path[i, j, 1] = 1
            else:
                s_mat[i][j] = max(s_mat[i-1][j-1]+match, s_mat[i-1][j], s_mat[i][j-1])
                #获取最大值
                if s_mat[i-1][j-1]+match == s_mat[i][j]:
                    path[i,j,2] = 1
                if s_mat[i-1][j] == s_mat[i][j]:
                    path[i,j,1] = 1
                if s_mat[i][j-1] == s_mat[i][j]:
                    path[i,j,0] = 1
                #记录了最大值来的方向，其中2代表对角，1代表从上面来，0代表从左边来

    score = round(s_mat[m-1][n-1]/L, 3)
    OnePath = []
    AllPaths = []
    FindPath(m-1, n-1, s_mat, path, OnePath, AllPaths)
    return (score, AllPaths)

p1 = '1.6.2.1,2.3.2.1,4.12.19.1,4.12.11.3,4.12.12.1,4.12.13.1,4.11.6.1,4.11.7.1,4.12.8.14'
p2 = '1.3.2.4,2.7.2.1,4.11.2.1,4.12.9.1,4.11.3.1,4.11.4.1,4.11.5.1,4.11.6.1,4.11.7.1,4.12.8.13'
p3 = 'FASLG,FAS,FADD,CASP8,BID,BAX,BAK1,CYCS,APAF1,CASP9,CASP7'

'''pw1 = CheckStlist(p1)
pw2 = CheckStlist(p2)
score = pw_similarity(pw1,pw2)[0]
paths = pw_similarity(pw1,pw2)[1]'''