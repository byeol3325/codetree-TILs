# 다양한 색 노드들. 각 노드는 color, max_depth
# 동적으로 노드 추가, 색깔 변경 시스템
# 처음에 아무 노드도 없음

# 4가지 명령
class Node:
    def __init__(self, m_id, p_id, color, max_depth):
        self.m_id = m_id
        self.p_id = p_id
        self.c_id = []
        self.color = color
        self.max_depth = max_depth
    
    def change_color(self, ncolor):
        self.color = ncolor

    def show_node(self):
        print("About node(m_id, p_id, c_id, color, max_depth) : ", self.m_id, self.p_id, self.c_id, self.color, self.max_depth)

class Tree:
    def __init__(self, nodes={}):
        self.nodes = nodes # m_id : Node
    
    def add_node(self, new_node):
        if new_node.p_id == -1: # 루트라서 그냥 넣으면 끝
            self.nodes[new_node.m_id] = new_node
            return None
        
        # node 넣어도 되는지 확인
        now_depth = 1
        node = new_node
        while True:
            if node.max_depth < now_depth:
                return None
            
            if node.p_id == -1:
                break
            else:
                node = self.nodes[node.p_id]
                now_depth += 1
        
        # node 추가됨. nodes에 추가
        self.nodes[new_node.m_id] = new_node
        # node 추가됨. nodes에 c_id에 추가
        parent_id = new_node.p_id
        self.nodes[parent_id].c_id.append(new_node.m_id)
    
    def get_color_node(self, m_id):
        return self.nodes[m_id].color
    
    def show_nodes(self):
        for k, v in self.nodes.items():
            v.show_node()

FOREST = [] # many Tree
NODE_TO_TREEIDX = {} # m_id : tree_index

"""
노드 추가 100 m_id p_id color max_depth
- 노드 트리에 추가. 각 노드는 m_id(고유번호), p_id(부모 노드), color(색깔), 최대 깊이(max_depth)
- color는 1~5. 12345 - 빨/주/노/초/파
- p_id : -1이면, 해당 노드는 새로운 트리의 루트 노드
- max_depth : 해당 노드를 루트로 하는 서브트리의 최대 깊이. 자기 자신에 해당하는 노드의 깊이는 1
- 기존 노드들의 max_depth 값으로 인해 노드가 추가됨으로써 모순이 발생한다면, 현재 노드는 추가하지 않음
"""
def Rule1(q):
    new_node = Node(q[1], q[2], q[3], q[4])

    if q[2] == -1: # p_id == -1 이면 새로운 트리 만들어잇!
        FOREST.append(Tree(nodes={}))
        tree_idx = len(FOREST)-1
    else:
        tree_idx = NODE_TO_TREEIDX[q[2]]
    
    FOREST[tree_idx].add_node(new_node)
    NODE_TO_TREEIDX[q[1]] = tree_idx
    return None


"""
색깔 변경 200 m_id color
- m_id를 루트로 하는 서브트리의 모든 노드의 색을 지정된 색 color로 변경
"""
def Rule2(q):
    global FOREST, NODE_TO_TREEIDX
    tree_idx = NODE_TO_TREEIDX[q[1]]
    
    color_tree = FOREST[tree_idx]
    node = color_tree.nodes[q[1]]
    need_color_nodes_id = [q[1]] + node.c_id
    while True:
        if len(need_color_nodes_id) == 0:
            break
        
        need_color_nodes_id = change_color_nodes(color_tree, need_color_nodes_id, q[2])
    
    return None

def change_color_nodes(tree, nodes_id, ncolor):
    next_nodes_id = []
    for node_id in nodes_id:
        tree.nodes[node_id].change_color(ncolor)
        next_nodes_id += tree.nodes[node_id].c_id
    return next_nodes_id

"""
색깔 조회 300 m_id
- m_id 현재 색 조회
"""
def Rule3(q):
    tree_idx = NODE_TO_TREEIDX[q[1]]
    print(FOREST[tree_idx].get_color_node(q[1]))
    return None

"""
점수 조회 400
- 모든 노드의 가치를 계산하여 가치 제곱 합을 출력.
- 각 노드의 가치는 해당 노드를 루트로 하는 서브트리 내의 서로 다른 색깔의 수
"""
def Rule4(q):
    total = 0

    for tree in FOREST:
        nodes = tree.nodes # m_id, node
        for k, v in nodes.items():
            color_set = set()
            color_set.add(v.color)# 하나의 노드 컬러

            nodes_id = [k]
            while True:
                nodes_id, color_set = add_color(tree, nodes_id, color_set)
                if len(color_set) == 5: # 5가지 칼라 다 해당
                    break
                if len(nodes_id) == 0: # 더 이상 노드 없음
                    break
            
            total += len(color_set)**2
    print(total)
    return None

def add_color(tree, nodes_id, color_set):
    next_nodes_id = []
    for node_id in nodes_id:
        ncolor = tree.get_color_node(node_id)
        if ncolor not in color_set:
            color_set.add(ncolor)

        next_nodes_id += tree.nodes[node_id].c_id
    return next_nodes_id, color_set




Q = int(input())
stop = -1
for i in range(Q):
    if stop == i:
        print("now command :", command)
        break
    
    command = list(map(int, input().split()))
    if command[0] == 100:
        Rule1(command)
    elif command[0] == 200:
        Rule2(command)
    elif command[0] == 300:
        Rule3(command)
    else: # command[0] == 400
        Rule4(command)

"""
print("node to tree idx : ", NODE_TO_TREEIDX)
for i, tree in enumerate(FOREST):
    print("==================", i ,"th tree=====================")
    tree.show_nodes()
    #print("=================================================")
"""