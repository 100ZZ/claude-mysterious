from sqlalchemy.orm import Session
from models import Node, User
from schemas import NodeCreate, NodeUpdate


def get_nodes(db: Session, skip: int = 0, limit: int = 10, name: str = None):
    """获取节点列表"""
    query = db.query(Node)
    if name:
        query = query.filter(Node.name.contains(name))
    return query.offset(skip).limit(limit).all()


def get_nodes_count(db: Session, name: str = None):
    """获取节点总数"""
    query = db.query(Node)
    if name:
        query = query.filter(Node.name.contains(name))
    return query.count()


def get_node(db: Session, node_id: int):
    """根据ID获取节点"""
    return db.query(Node).filter(Node.id == node_id).first()


def create_node(db: Session, node: NodeCreate, current_user: User):
    """创建节点"""
    db_node = Node(
        name=node.name,
        description=node.description or "",
        type=node.type,
        host=node.host,
        username=node.username,
        password=node.password,
        port=node.port,
        status=node.status,
        creator_id=str(current_user.id),
        creator=current_user.username,
        modifier_id=str(current_user.id),
        modifier=current_user.username
    )
    db.add(db_node)
    db.commit()
    db.refresh(db_node)
    return db_node


def update_node(db: Session, node_id: int, node: NodeUpdate, current_user: User):
    """更新节点"""
    db_node = get_node(db, node_id)
    if not db_node:
        return None
    
    update_data = node.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_node, field, value)
    
    db_node.modifier_id = str(current_user.id)
    db_node.modifier = current_user.username
    
    db.commit()
    db.refresh(db_node)
    return db_node


def delete_node(db: Session, node_id: int):
    """删除节点"""
    db_node = get_node(db, node_id)
    if not db_node:
        return False
    
    db.delete(db_node)
    db.commit()
    return True

