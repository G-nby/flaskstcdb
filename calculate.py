import numpy as np

def calculate1(net_data, node_count, nodes):
    adj_mat = make_adj_mat(net_data, node_count, nodes)
    node_weights = dw_node_rank(adj_mat, 0.85)
    '''myres = []
    for i in range(10):
        myres.append(nodes[np.argmax(dw_node_rank(adj_mat, i/10+0.1))])
    print(myres)
    print("1")
    print(node_weights)
    print("1")
    print(np.argmax(node_weights))'''
    result = nodes[np.argmax(node_weights)]

    if result == "Ca2 ":
        result = "Ca2+"

    return f"The key factor is：{result}"

def dw_node_rank(adj_matrix, damping_factor, max_iter=100, tol=1e-8):
    num_nodes = adj_matrix.shape[0]
    out_degree = np.sum(adj_matrix, axis=1)    # 各个节点出度，对应source行的总和
    in_degree = np.sum(adj_matrix, axis=0)
    '''print(out_degree)
    print(in_degree)'''

    # 初始化节点权重（初始相同）
    node_weights = np.ones(num_nodes) / num_nodes

    # 迭代计算节点权重
    for _ in range(max_iter):
        prev_weights = np.copy(node_weights)

        for i in range(num_nodes):
            sum_weights = 0
            for j in range(num_nodes):
                if adj_matrix[j, i] != 0:
                    sum_weights += prev_weights[j] * adj_matrix[j, i] / out_degree[j]   # 按权值分配dwPR值,强调链入（作为target）

            node_weights[i] = (1 - damping_factor) / num_nodes + damping_factor * sum_weights

        # 检查收敛性
        if np.linalg.norm(node_weights - prev_weights, 1) < tol:
            break

    return node_weights


def make_adj_mat(net_data, node_count, nodes):
    adj_mat = np.zeros((node_count, node_count))
    for link in net_data:
        rowcount = nodes.index(link['source'])
        col_count = nodes.index(link['target'])
        adj_mat[rowcount][col_count] = link['width']/3
    '''
    for i in range(node_count):
        col_sum = np.sum(adj_mat[i, :])
        if col_sum:
            adj_mat[i, :] /= col_sum'''
    return adj_mat



adj_matrix = np.array([
    [0, 1, 1, 1, 5],
    [1, 0, 2, 1, 4],
    [1, 2, 0, 3, 1],
    [1, 1, 1, 0, 0],
    [1, 0, 0, 3, 1],
])


# 运行DWNodeRank算法
# node_weights = dw_node_rank(adj_matrix)
# print("Node Weights:", node_weights)
