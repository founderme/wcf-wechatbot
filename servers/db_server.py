import os
import sqlite3
from utils.common import logger

current_path = os.path.dirname(__file__)
userDb = current_path + '/../data/user.db'
roomDb = current_path + '/../data/room.db'

def openDb(dbPath, ):
    conn = sqlite3.connect(database=dbPath, )
    cursor = conn.cursor()
    return conn, cursor

def closeDb(conn, cursor):
    cursor.close()
    conn.close()

class DbInitServer:
    def __init__(self):
        pass

    def createTable(self, cursor, table_name, columns):
        """
        :param table_name:  要创建的表名
        :param columns:  要创建的字段名 要符合SQL语法
        :return:
        """
        try:
            cursor.execute(
                f"CREATE TABLE IF NOT EXISTS {table_name} ({columns})"
            )
            return True
        except Exception as e:
            logger.error(f'[-]: 创建数据表出现错误, 错误信息: {e}')
            return False

    def initDb(self, ):
        # 初始化用户数据库 用户表 管理员表
        userConn, userCursor = openDb(userDb)
        self.createTable(userCursor, 'whiteUser', 'wxId varchar(255) PRIMARY KEY, wxName varchar(255)')
        self.createTable(userCursor, 'Admin', 'wxId varchar(255) PRIMARY KEY, roomId varchar(255)')
        closeDb(userConn, userCursor)
        # 初始化群聊数据库 白名单表 推送定时任务表
        userConn, userCursor = openDb(roomDb)
        self.createTable(userCursor, 'whiteRoom', 'roomId varchar(255) PRIMARY KEY, roomName varchar(255)')
        self.createTable(userCursor, 'pushRoom', 'taskName varchar(255), roomId varchar(255), roomName varchar(255), PRIMARY KEY (taskName, roomId)')
        closeDb(userConn, userCursor)
        logger.info(f'数据库初始化成功！！！')

class DbUserServer:
    def __init__(self):
        pass
    
    def addUser(self, wxId, wxName):
        """
        增加好友
        :param wxId: 微信ID
        :param roomId: 微信昵称
        :return:
        """
        conn, cursor = openDb(userDb)
        try:
            cursor.execute('INSERT INTO whiteUser VALUES (?, ?)', (wxId, wxName))
            conn.commit()
            closeDb(conn, cursor)
            return True
        except Exception as e:
            logger.error(f'增加好友出现错误: {e}')
            closeDb(conn, cursor)
            return False

    def delUser(self, wxId):
        conn, cursor = openDb(userDb)
        try:
            cursor.execute('DELETE FROM whiteUser WHERE wxId=?', (wxId, ))
            conn.commit()
            closeDb(conn, cursor)
            return True
        except Exception as e:
            logger.error(f'删除好友出现错误: {e}')
            closeDb(conn, cursor)
            return False

    def searchUser(self, wxId):
        conn, cursor = openDb(userDb)
        try:
            cursor.execute('SELECT wxId FROM whiteUser WHERE wxId=?', (wxId, ))
            result = cursor.fetchone()
            closeDb(conn, cursor)
            return True if result else False
        except Exception as e:
            logger.error(f'[-]: 查询好友出现错误, 错误信息: {e}')
            closeDb(conn, cursor)
            return False
    
    def showUser(self):
        conn, cursor = openDb(userDb)
        try:
            cursor.execute('SELECT wxId, wxName FROM whiteUser')
            result = cursor.fetchall()
            closeDb(conn, cursor)
            return result
        except Exception as e:
            logger.error(f'获取白名单好友出现错误: {e}')
            closeDb(conn, cursor)
            return []

    def addAdmin(self, wxId, roomId):
        """
        增加管理员
        :param wxId: 微信ID
        :param roomId: 群聊ID
        :return:
        """
        conn, cursor = openDb(userDb)
        try:
            cursor.execute('INSERT INTO Admin VALUES (?, ?)', (wxId, roomId))
            conn.commit()
            closeDb(conn, cursor)
            return True
        except Exception as e:
            logger.error(f'增加管理员出现错误: {e}')
            closeDb(conn, cursor)
            return False

    def delAdmin(self, wxId, roomId):
        conn, cursor = openDb(userDb)
        try:
            cursor.execute('DELETE FROM Admin WHERE wxId=? AND roomId=?', (wxId, roomId))
            conn.commit()
            closeDb(conn, cursor)
            return True
        except Exception as e:
            logger.error(f'删除管理员出现错误: {e}')
            closeDb(conn, cursor)
            return False

    def searchAdmin(self, wxId, roomId):
        conn, cursor = openDb(userDb)
        try:
            cursor.execute('SELECT wxId FROM Admin WHERE wxId=? AND roomId=?', (wxId, roomId))
            result = cursor.fetchone()
            closeDb(conn, cursor)
            if result:
                return True
            else:
                return False
        except Exception as e:
            logger.error(f'[-]: 查询管理员出现错误, 错误信息: {e}')
            closeDb(conn, cursor)
            return False

class DbRoomServer:
    def __init__(self):
        pass

    def addWhiteRoom(self, roomId, roomName):
        conn, cursor = openDb(roomDb)
        try:
            cursor.execute('INSERT INTO whiteRoom VALUES (?, ?)', (roomId, roomName))
            conn.commit()
            closeDb(conn, cursor)
            return True
        except Exception as e:
            logger.error(f'新增白名单群聊出现错误: {e}')
            closeDb(conn, cursor)
            return False

    def delWhiteRoom(self, roomId):
        conn, cursor = openDb(roomDb)
        try:
            cursor.execute('DELETE FROM whiteRoom WHERE roomId=?', (roomId,))
            conn.commit()
            closeDb(conn, cursor)
            return True
        except Exception as e:
            logger.error(f'删除白名单群聊出现错误, 错误信息: {e}')
            closeDb(conn, cursor)
            return False
    
    def searchWhiteRoom(self, roomId):
        conn, cursor = openDb(roomDb)
        try:
            cursor.execute('SELECT roomId FROM whiteRoom WHERE roomId=?', (roomId,))
            result = cursor.fetchone()
            closeDb(conn, cursor)
            return True if result else False
        except Exception as e:
            logger.error(f'[-]: 查询白名单群聊出现错误, 错误信息: {e}')
            closeDb(conn, cursor)
            return False

    def showWhiteRoom(self, ):
        conn, cursor = openDb(roomDb)
        try:
            cursor.execute('SELECT roomId, roomName FROM whiteRoom')
            result = cursor.fetchall()
            closeDb(conn, cursor)
            return result
        except Exception as e:
            logger.error(f'查看所有白名单群聊出现错误: {e}')
            closeDb(conn, cursor)
            return []

    def addPushRoom(self, taskName, roomId, roomName):
        conn, cursor = openDb(roomDb)
        try:
            cursor.execute('INSERT INTO pushRoom VALUES (?, ?, ?)', (taskName, roomId, roomName))
            conn.commit()
            closeDb(conn, cursor)
            return True
        except Exception as e:
            logger.error(f'新增推送任务出现错误: {e}')
            closeDb(conn, cursor)
            return False
    
    def delPushRoom(self, taskName, roomId, roomName):
        conn, cursor = openDb(roomDb)
        try:
            cursor.execute('DELETE FROM pushRoom WHERE taskName=? AND roomId=? AND roomName=?', (taskName, roomId, roomName))
            conn.commit()
            closeDb(conn, cursor)
            return True
        except Exception as e:
            logger.error(f'删除推送任务出现错误: {e}')
            closeDb(conn, cursor)
            return False
    
    def showPushRoom(self, taskName=None):
        conn, cursor = openDb(roomDb)
        try:
            if taskName:
                cursor.execute('SELECT roomId, roomName FROM pushRoom WHERE taskName=?', (taskName,))
            else:
                cursor.execute('SELECT * FROM pushRoom')
            result = cursor.fetchall()
            return result
        except Exception as e:
            logger.error(f'查看推送任务出现错误: {e}')
            closeDb(conn, cursor)
            return []

if __name__ == '__main__':
    Dis = DbInitServer()
    Dis.initDb()