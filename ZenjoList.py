import e32
import e32dbm
import e32db
import appuifw
import telephone


class BaseDados:
    def __init__(self,db_name):
        try:
            self.native_db = e32db.Dbms()
            self.native_db.open(db_name)
        except:
            self.native_db = e32db.Dbms()
            self.native_db.create(db_name)
            self.native_db.open(db_name)
            self.native_db.execute(self.__sql_create_empresa())
            self.native_db.execute(self.__sql_create_telefone())
            self.native_db.execute(self.__sql_create_email())
            self.native_db.execute(self.__sql_create_categoria())
            self.native_db.execute(self.__sql_create_categoria_empresa())
            self.native_db.execute(self.__sql_create_favoritos())

    def get_all_categoria(self):
        dbv = e32db.Db_view()
        dbv.prepare(self.native_db, self.__sql_all_categoria() )
        results = []
        for i in range(dbv.count_line()):
            dbv.get_line()
            descricao = dbv.col(1)
            codigo = dbv.col(2)
            results.append((descricao,codigo))
            dbv.next_line()
        return results

    def get_all_favoritos(self):
        dbv = e32db.Db_view()
        dbv.prepare(self.native_db, self.__sql_all_favoritos() )
        todos = []
        for i in range(dbv.count_line()):
            dbv.get_line()
            nome = unicode(self.get_name_favoritos(dbv.col(1)))
            numero = self.get_numero_telefone(dbv.col(1))
            todos.append((nome,numero))
            dbv.next_line()
        return todos

    def get_name_favoritos(self,codigo):
        dbv = e32db.Db_view()
        dbv.prepare(self.native_db, self.__sql_getName_empresa(codigo) )
        dbv.get_line()
        return "-> %s" % (dbv.col(1))

    def get_numero_telefone(self,codigo):
        dbv = e32db.Db_view()
        dbv.prepare(self.native_db, self.__sql_getNumero_telefone(codigo) )
        numeros = []
        for i in range(dbv.count_line()):
            dbv.get_line()
            numero = "0%s%s" % (str(dbv.col(2)),str(dbv.col(1)))
            numeros.append(unicode(numero))
            dbv.next_line()
        return numeros

    def get_all_categoria_empresa(self,cod_cat):
        dbv = e32db.Db_view()
        dbv.prepare(self.native_db, self.__sql_all_categoria_empresa(cod_cat) )
        codigos = []
        for i in range(dbv.count_line()):
            dbv.get_line()
            nome = unicode(self.get_name_empresa(dbv.col(1)))
            cod_emp = dbv.col(1)
            codigos.append((nome,cod_emp))
            dbv.next_line()
        return codigos

    def get_name_empresa(self,codigo):
        dbv = e32db.Db_view()
        dbv.prepare(self.native_db, self.__sql_getName_empresa(codigo) )
        dbv.get_line()
        return "%s" % (dbv.col(1))       

    def add_empresa(self,codigo,razao,cnpj):
        try:
            self.native_db.execute(self.__sql_add_empresa(codigo, razao, cnpj))
        except:
            print "erro: add_empresa(%d, '%s', '%s')\n" % (codigo, razao, cnpj)

    def add_telefone(self,codigo,numero,ddd):
        try:
            self.native_db.execute(self.__sql_add_telefone(codigo, numero, ddd))
        except:
            print "erro: add_telefone(%d, %d, %d)\n" % (codigo, numero, ddd)

    def add_email(self,cod_emp,email):
        try:
            self.native_db.execute(self.__sql_add_email(cod_emp, email))
        except:
            print "erro: add_email(%d, '%s')\n" % (cod_emp, email)

    def add_categoria(self,codigo,descricao):
        try:
            self.native_db.execute(self.__sql_add_categoria(codigo, descricao))
        except:
            print "erro: add_categoria(%d, '%s')\n" % (codigo, descricao)

    def add_categoria_empresa(self,cod_cat,cod_emp):
        try:
            self.native_db.execute(self.__sql_add_categoria_empresa(cod_cat, cod_emp))
        except:
            print "erro: add_categoria_empresa(%d, %d)\n" % (cod_cat, cod_emp)

    def add_favoritos(self,cod_emp):
        try:
            self.native_db.execute(self.__sql_add_favoritos(cod_emp))
        except:
            print "erro: add_favoritos(%d)\n" % (cod_emp)

    #SQL para Empresa
    def __sql_create_empresa(self):
        return u"CREATE TABLE empresa (codigo INTEGER, razao VARCHAR, cnpj VARCHAR)"

    def __sql_add_empresa(self,codigo,razao,cnpj):
        sql = "INSERT INTO empresa (codigo, razao, cnpj) VALUES (%d, '%s', '%s')" % (codigo, razao, cnpj)
        return unicode(sql)

    def __sql_getName_empresa(self,codigo):
        sql = "SELECT razao FROM empresa WHERE codigo = %d" % (codigo)
        return unicode(sql)
   
    #SQL para Telefone
    def __sql_create_telefone(self):
        return u"CREATE TABLE telefone(cod_emp INTEGER, numero INTEGER, ddd INTEGER)"

    def __sql_add_telefone(self,codigo,numero,ddd):
        sql = "INSERT INTO telefone (cod_emp, numero, ddd) VALUES (%d, %d, %d)" % (codigo, numero, ddd)
        return unicode(sql)

    def __sql_getNumero_telefone(self,codigo):
        sql = "SELECT numero, ddd FROM telefone WHERE cod_emp = %d" % (codigo)
        return unicode(sql)       

    #SQL para Email
    def __sql_create_email(self):
        return u"CREATE TABLE email(cod_emp INTEGER, email VARCHAR)"

    def __sql_add_email(self,codigo,email):
        sql = "INSERT INTO email (cod_emp, email) VALUES (%d, '%s')" % (codigo, email)
        return unicode(sql)

    #SQL para Categoria
    def __sql_create_categoria(self):
        return u"CREATE TABLE categoria(codigo INTEGER, descricao VARCHAR)"

    def __sql_add_categoria(self,codigo,descricao):
        sql = "INSERT INTO categoria (codigo, descricao) VALUES (%d, '%s')" % (codigo, descricao)
        return unicode(sql)

    def __sql_all_categoria(self):
        return u"SELECT descricao, codigo FROM categoria"

    #SQL para Categoria_Empresa
    def __sql_create_categoria_empresa(self):
        return u"CREATE TABLE categoria_empresa(cod_cat INTEGER, cod_emp INTEGER)"

    def __sql_add_categoria_empresa(self,cod_cat,cod_emp):
        sql = "INSERT INTO categoria_empresa (cod_cat, cod_emp) VALUES (%d, %d)" % (cod_cat, cod_emp)
        return unicode(sql)

    def __sql_all_categoria_empresa(self,cod_cat):
        sql = "SELECT cod_emp FROM categoria_empresa WHERE cod_cat = %d " % (cod_cat)
        return unicode(sql)

    #SQL para Favoritos
    def __sql_create_favoritos(self):
        return u"CREATE TABLE favoritos(cod_emp INTEGER, qtd_ligacao INTEGER)"

    def __sql_add_favoritos(self,cod_emp):
        sql = "INSERT INTO favoritos (cod_emp, qtd_ligacao) VALUES (%d, 0)" % (cod_emp)
        return unicode(sql)

    def __sql_all_favoritos(self):
        return u"SELECT cod_emp FROM favoritos"

class CategoriaView:
    def __init__(self,ListCellViewApp,db):
        self.app = ListCellViewApp
        self.db = db
        self.categoria_tudo = self.db.get_all_categoria()
        self.categoria_nome = [item[0] for item in self.categoria_tudo]
        self.categoria_codigo = [item[1] for item in self.categoria_tudo]
        self.lista_categoria = appuifw.Listbox(self.categoria_nome, self.handle_select)
        self.index = None
        self.flag = 0
        appuifw.app.body = self.lista_categoria
        self.body_old_categoria = appuifw.app.body
        self.body_new_categoria = appuifw.app.body
        self.menu_old_categoria = appuifw.app.menu
        self.menu_new_categoria = [(u"Select", self.handle_select)]

    def activate(self):
        appuifw.app.body = self.body_new_categoria
        appuifw.app.menu = self.menu_new_categoria

    def handle_select(self):
        '''n = self.get_name()
        appuifw.note(u"Selected: "+ n, 'info')'''
        if self.flag == 0:
            self.index = self.get_current_categoria()
            self.body_old_categoria = appuifw.app.body
            self.menu_old_categoria = appuifw.app.menu
            self.empresa_tudo = self.db.get_all_categoria_empresa(self.categoria_codigo[self.index])
            self.empresa_nome = [item[0] for item in self.empresa_tudo]
            self.empresa_codigo = [item[1] for item in self.empresa_tudo]
            self.lista_empresa = appuifw.Listbox(self.empresa_nome, self.handle_select)
            self.body_new_categoria = self.lista_empresa
            self.menu_new_categoria = [(u"Select", self.handle_select),(u"Add Favoritos",self.handle_add_favoritos),(u"Back", self.handle_back)]
            appuifw.app.body = self.body_new_categoria
            appuifw.app.menu = self.menu_new_categoria
            self.flag = 1
        elif self.flag == 1:
            self.index = self.get_current_empresa()
            self.body_old_categoria = appuifw.app.body
            self.menu_old_categoria = appuifw.app.menu
            self.telefones = self.db.get_numero_telefone(self.empresa_codigo[self.index])
            self.lista_telefone = appuifw.Listbox(self.telefones, self.handle_select)
            self.body_new_categoria = self.lista_telefone
            self.menu_new_categoria = [(u"Call", self.handle_call),(u"Back", self.handle_back)]
            appuifw.app.body = self.body_new_categoria
            appuifw.app.menu = self.menu_new_categoria
            self.flag = 2
                       
    def handle_back(self):
        if self.flag == 2:
            self.body_new_categoria = self.body_old_categoria
            self.menu_new_categoria = self.menu_old_categoria
            appuifw.app.body = self.body_new_categoria
            appuifw.app.menu = self.menu_new_categoria
            self.flag -= 1
        elif self.flag == 1:
            self.body_new_categoria = self.lista_categoria
            self.menu_new_categoria = [(u"Select", self.handle_select)]
            appuifw.app.body = self.body_new_categoria
            appuifw.app.menu = self.menu_new_categoria
            self.flag -= 1
           
    def handle_add_favoritos(self):
        self.index = self.get_current_empresa()
        cod_emp = self.empresa_codigo[self.index]
        empresa = self.empresa_nome[self.index]
        self.db.add_favoritos(cod_emp)
        appuifw.note("'"+ empresa + u"' add com sucesso!", 'info')       

    def handle_call(self):
        telefone = self.telefones[self.get_current_telefone()]
        telephone.dial(telefone)   

    def get_current_categoria(self):
        return self.lista_categoria.current()

    def get_current_empresa(self):
        return self.lista_empresa.current()

    def get_current_telefone(self):
        return self.lista_telefone.current()

    def get_name(self):
        i = self.get_current()
        return unicode(str(self.categoria_codigo[i]))

class FavoritosView:
    def __init__(self,ListCellViewApp,db):
        self.app = ListCellViewApp
        self.favoritos_tudo = db.get_all_favoritos()
        self.favoritos_nome = [item[0] for item in self.favoritos_tudo]
        self.favoritos_codigo = [item[1] for item in self.favoritos_tudo]
        self.lista_favoritos = appuifw.Listbox(self.favoritos_nome, self.handle_select)
        self.index = None
        appuifw.app.body = self.lista_favoritos
        self.body_old_favoritos = appuifw.app.body
        self.body_new_favoritos = appuifw.app.body
        self.menu_old_favoritos = appuifw.app.menu
        self.menu_new_favoritos = [(u"Select", self.handle_select)]

    def activate(self):
        appuifw.app.body = self.body_new_favoritos
        appuifw.app.menu = self.menu_new_favoritos

    def handle_select(self):
        self.index = self.get_current_empresa()
        self.body_old_favoritos = appuifw.app.body
        self.menu_old_favoritos = appuifw.app.menu
        self.telefones = [item for item in self.favoritos_codigo[self.index]]
        self.lista_numero_favorito = appuifw.Listbox( self.telefones , self.handle_select)
        self.body_new_favoritos = self.lista_numero_favorito
        self.menu_new_favoritos = [(u"Call", self.handle_call),(u"Back", self.handle_back)]
        appuifw.app.body = self.body_new_favoritos
        appuifw.app.menu = self.menu_new_favoritos

    def handle_back(self):
        self.body_new_favoritos = self.body_old_favoritos
        self.menu_new_favoritos = self.menu_old_favoritos
        appuifw.app.body = self.body_new_favoritos
        appuifw.app.menu = self.menu_new_favoritos

    def handle_call(self):
        telefone = self.telefones[self.get_current_telefone()]
        telephone.dial(telefone)

    def get_current_empresa(self):
        return self.lista_favoritos.current()

    def get_current_telefone(self):
        return self.lista_numero_favorito.current()

class ListCellViewApp:
    def __init__(self):
        self.lock = e32.Ao_lock()
        appuifw.app.exit_key_handler = self.exit_key_handler
        db = BaseDados(u"c:\\listcell.db")
       
        db.add_categoria(1,'Advogado')
        db.add_categoria(2,'Shopping')
       
        db.add_empresa(1,'Federalcred','301')
        db.add_telefone(1,30158800,83)
        db.add_categoria_empresa(1,1)
       
        db.add_empresa(2,'Casa','400')
        db.add_telefone(2,32375550,83)
        db.add_categoria_empresa(2,2)
        db.add_categoria_empresa(1,2)
       
        db.add_favoritos(1)
        db.add_favoritos(2)
       
        self.categoria_view = CategoriaView(self,db)
        self.favoritos_view = FavoritosView(self,db)       
        self.views = [self.favoritos_view, self.categoria_view]
        appuifw.app.set_tabs([u"Favoritos", u"Categoria"], self.handle_tab)

    def run(self):
        self.handle_tab(0)
        self.lock.wait()
        self.close()
 
    def handle_tab(self, index):
        self.views[index].activate()
 
    def exit_key_handler(self):
        self.lock.signal()
 
    def close(self):
        appuifw.app.exit_key_handler = None
        appuifw.app.set_tabs([u"Back..."], lambda x: None)        

if __name__ == '__main__':

    old_title = appuifw.app.title
    appuifw.app.title = u"ListCell"
    App = ListCellViewApp()
    App.run()
 
    appuifw.app.title = old_title
    appuifw.menu = None
   
    print "--eof ListCell"
