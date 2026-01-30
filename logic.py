import sqlite3
from config import DATABASE as DB

skills = [ (_,) for _ in (['Python', 'SQL', 'API', 'Telegram'])]
statuses = [ (_,) for _ in (['На этапе проектирования', 'В процессе разработки', 'Разработан. Готов к использованию.', 'Обновлен', 'Завершен. Не поддерживается'])]

class DB_Manager:
    def __init__(self, database):
        self.database = database

    def create_tables(self):
        conn = sqlite3.connect(self.database)
        with conn:
            conn.execute('''CREATE TABLE projects (
                            project_id INTEGER PRIMARY KEY,
                            user_id INTEGER,
                            project_name TEXT NOT NULL,
                            description TEXT,
                            url TEXT,
                            status_id INTEGER,
                            FOREIGN KEY(status_id) REFERENCES status(status_id)
                        )''') 
            conn.execute('''CREATE TABLE skills (
                            skill_id INTEGER PRIMARY KEY,
                            skill_name TEXT
                        )''')
            conn.execute('''CREATE TABLE project_skills (
                            project_id INTEGER,
                            skill_id INTEGER,
                            FOREIGN KEY(project_id) REFERENCES projects(project_id),
                            FOREIGN KEY(skill_id) REFERENCES skills(skill_id)
                        )''')
            conn.execute('''CREATE TABLE status (
                            status_id INTEGER PRIMARY KEY,
                            status_name TEXT
                        )''')
            conn.commit()
        print("База данных успешно создана.")

    def __executemany(self, sql, data):
        conn = sqlite3.connect(self.database)
        with conn:
            conn.executemany(sql, data)
            conn.commit()

    def __select_data(self, sql, data = tuple()):
        conn = sqlite3.connect(self.database)
        with conn:
            cur = conn.cursor()
            cur.execute(sql, data)
            return cur.fetchall()
            

    def default_insert(self):
        sql = 'INSERT OR IGNORE INTO skills (skill_name) values(?)'
        data = skills
        self.__executemany(sql, data)
        sql = 'INSERT OR IGNORE INTO status (status_name) values(?)'
        data = statuses
        self.__executemany(sql, data)


    def insert_project(self, data):
        sql = 'INSERT OR IGNORE INTO projects (user_id, project_name, url, status_id) values(?, ?, ?, ?)'
        self.__executemany(sql, data)

    def insert_skill(self, user_id, project_name, skill):
        sql = 'SELECT project_id FROM projects WHERE project_name = ? AND user_id = ?'
        project_id = self.__select_data(sql, (project_name, user_id))[0][0]
        skill_id = self.__select_data('SELECT skill_id FROM skills WHERE skill_name = ?', (skill,))[0][0]
        data = [(project_id,skill_id)]
        sql = 'INSERT OR IGNORE INTO project_skills VALUES (?, ?)'
        self.__executemany(sql, data)

  
    def get_statuses(self):
        sql='SELECT status_name from status'
        return self.__select_data(sql)
        
    def get_status_id(self, status_name):
        sql = 'SELECT status_id FROM status WHERE status_name = ?'
        res = self.__select_data(sql, (status_name,))
        if res: return res[0][0]
        else: return None

    def get_projects(self, user_id):
        return self.__select_data(sql='SELECT * FROM projects WHERE user_id = ?', data = (user_id,))

    def get_project_id(self, project_name, user_id):
        return self.__select_data(sql='SELECT project_id FROM projects WHERE project_name = ? AND user_id = ?  ', data = (project_name, user_id,))[0][0]

    def get_skills(self):
        return self.__select_data(sql='SELECT * FROM skills')
    
    def get_project_skills(self, project_name):
        res = self.__select_data(sql='''SELECT skill_name FROM projects 
JOIN project_skills ON projects.project_id = project_skills.project_id 
JOIN skills ON skills.skill_id = project_skills.skill_id 
WHERE project_name = ?''', data = (project_name,) )
        return ', '.join([x[0] for x in res])
    
    def get_project_info(self, user_id, project_name):
        sql = """
SELECT project_name, description, url, status_name FROM projects 
JOIN status ON
status.status_id = projects.status_id
WHERE project_name=? AND user_id=?
"""
        return self.__select_data(sql=sql, data = (project_name, user_id))
    

    def update_projects(self, param, data):
        self.__executemany(f"UPDATE projects SET {param} = ? WHERE project_name = ? AND user_id = ?", [data]) # data ('atr', 'mew', 'name', 'user_id')


    def delete_project(self, user_id, project_id):
        sql = "DELETE FROM projects WHERE user_id = ? AND project_id = ? "
        self.__executemany(sql, [(user_id, project_id)])

    def delete_skill(self, project_id, skill_id):
        sql = "DELETE FROM skills WHERE skill_id = ? AND project_id = ? "
        self.__executemany(sql, [(skill_id, project_id)])

#----------------------------------HOME WORK----------------------------------------------------#

    def delete_status(self, status_id):
        sql = """"DELETE FROM status 
        WHERE status_id = ? """ # Запиши сюда правильный SQL запрос
        self.__executemany(sql, [(status_id,)])

    def update_skills(self, skill_name, skill_id):
        sql = f"""UPDATE skills SET skill_name = ? 
        WHERE skill_id = ?""" # Запиши сюда правильный SQL запрос
        self.__executemany(sql, [(skill_name, skill_id)])

    def add_skill(self, skill_name):
        sql = 'INSERT OR IGNORE INTO skills (skill_name) values(?)'
        self.__executemany(sql, [(skill_name,)])        

    def update_project_status(self, project_id, project_status_id):
        sql = "UPDATE projects SET project_status_id = ? WHERE project_id = ?"
        self.__executemany(sql, [(project_status_id, project_id)])

#----------------------------------class but home work----------------------------------------------------#
    def add_column(self, table_name, column_name, column_type):
        conn = sqlite3.connect(self.database)
        with conn:
            conn.execute(f"ALTER TABLE {table_name} ADD COLUMN {column_name} {column_type}")
            conn.commit()
            


if __name__ == '__main__':
    manager = DB_Manager(DB)
    #manager.create_tables()
    #manager.insert_project([(901213, 'Test Project','http://example.com', 1, 'This is a test project')])
    #manager.delete_project(901213, 1)
    manager.add_column('projects', 'project_img', 'TEXT')
    #manager.update_project_status(1, 3)
    manager.default_insert()