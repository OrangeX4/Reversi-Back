from flask import Flask, request
from flask_socketio import SocketIO, emit, join_room, leave_room, close_room

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
socketio = SocketIO(app, cors_allowed_origins="*")

# 房间列表
rooms_list = []


def get_room(room_id):
    for i in range(len(rooms_list)):
        if rooms_list[i]['id'] == room_id:
            return rooms_list[i]

# 房间数据
rooms_data = []


def get_room_data(room_id):
    for i in range(len(rooms_data)):
        if rooms_data[i]['id'] == room_id:
            return rooms_data[i]


@socketio.event
def connect():
    print('connect')


@socketio.event
def disconnect():
    for room_data in rooms_data:
        if room_data['owner'] == request.sid:
            room = get_room(room_data['id'])
            if not room:
                continue
            if room_data['rival'] != '':
                # 有对手存在时, 交换房主权限, 并更新房间的 isReady
                room_data['owner'] = room_data['rival']
                room_data['rival'] = ''
                room['isReady'] = False
            else:
                # 无对手存在时, 删除这个房间
                rooms_list.remove(room)
                rooms_data.remove(room_data)
                emit('closeRoom', to=str(room_data['id']))
                close_room(str(room_data['id']))
            emit('exitRoomForRival', to=str(room_data['id']))
            # 给所有人重新广播房间列表
            emit('updateRoomList', rooms_list, broadcast=True)
        # 是对手时
        if room_data['rival'] == request.sid:
            room = get_room(room_data['id'])
            if not room:
                continue
            room_data['rival'] = ''
            room['isReady'] = False
            emit('exitRoomForOwner', to=str(room_data['id']))
            # 发送退出信息
            # 给所有人重新广播房间列表
            emit('updateRoomList', rooms_list, broadcast=True)
    


# 更新房间列表
@socketio.event
def updateRoomList():
    emit('updateRoomList', rooms_list)


# 新建房间
@socketio.event
def createRoom(name):
    # 获取最新的 room id
    if rooms_list:
        room_id = rooms_list[-1]['id'] + 1
    else:
        room_id = 0
    new_room = {
        'id': room_id,
        'name': name,
        'isReady': False
    }
    new_room_data = {
        'id': room_id,
        'owner': request.sid,
        'rival': '',
        'isOwnerFirst': True
    }
    rooms_list.append(new_room)
    rooms_data.append(new_room_data)
    # 使用 join_room
    join_room(str(room_id))
    # 给房主发送创建成功的消息
    emit('createRoom', rooms_list)
    # 给所有人重新广播房间列表
    emit('updateRoomList', rooms_list, broadcast=True)


# 其他人加入房间
@socketio.event
def addRoom(room_id):
    room = get_room(room_id)
    room_data = get_room_data(room_id)
    # 为空就退出
    if not room_data or not room:
        return
    # 可以加入时
    if room['isReady'] == False:
        room['isReady'] = True
        room_data['rival'] = request.sid
        join_room(str(room_id))
        emit('addRoom', to=str(room_id))
        # 给所有人重新广播房间列表
        emit('updateRoomList', rooms_list, broadcast=True)



# 退出房间
@socketio.event
def exitRoom(room_id):
    room = get_room(room_id)
    room_data = get_room_data(room_id)
    # 为空就退出
    if not room_data or not room:
        return
    # 是房主时
    if room_data['owner'] == request.sid:
        if room_data['rival'] != '':
            # 有对手存在时, 交换房主权限, 并更新房间的 isReady
            room_data['owner'] = room_data['rival']
            room_data['rival'] = ''
            room['isReady'] = False
        else:
            # 无对手存在时, 删除这个房间
            rooms_list.remove(room)
            rooms_data.remove(room_data)
            emit('closeRoom', to=str(room_id))
            close_room(str(room_id))
        emit('exitRoomForRival', to=str(room_id))
        # 给所有人重新广播房间列表
        emit('updateRoomList', rooms_list, broadcast=True)
    # 是对手时
    if room_data['rival'] == request.sid:
        room_data['rival'] = ''
        room['isReady'] = False
        emit('exitRoomForOwner', to=str(room_id))
        # 发送退出信息
        # 给所有人重新广播房间列表
        emit('updateRoomList', rooms_list, broadcast=True)
    # 使用 leave_room
    leave_room(str(room_id))



# 旁观者
@socketio.event
def observeRoom(room_id):
    room = get_room(room_id)
    room_data = get_room_data(room_id)
    # 为空就退出
    if not room_data or not room:
        return
    join_room(str(room_id))
    emit('observeRoom', {'id': room_id, 'isReady': room['isReady']})



# 更换先手顺序
@socketio.event
def setPlayerPiece(room_id, is_owner_first):
    room = get_room(room_id)
    room_data = get_room_data(room_id)
    # 为空就退出
    if not room_data or not room:
        return
    # 是房主时
    if room_data['owner'] == request.sid:
        room_data['isOwnerFirst'] = is_owner_first
        emit('setPlayerPiece', is_owner_first, to=str(room_id))

@socketio.event
def updateBoard(room_id, new_board, newest, reversal, current_piece):
    room = get_room(room_id)
    room_data = get_room_data(room_id)
    # 为空就退出
    if not room_data or not room:
        return
    emit('updateBoard', {'board': new_board, 'newest': newest, 'reversal': reversal, 'currentPiece': current_piece}, to=str(room_id))
    


    

if __name__ == '__main__':
    socketio.run(app, debug=False, port=7686, host='0.0.0.0')
