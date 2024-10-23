import streamlit as st
import streamlit_authenticator as stauth
from dependencies import add_registro, consulta, consulta_geral, cria_tabela
from time import sleep



def main():
    try:
        consulta_geral()
    except:
        cria_tabela() #Cria a tabela caso não exista
        
    db_query = consulta_geral() #Realiza a consulta geral para pegar os dados da tabela

    registros = {'usernames':{}}
    for data in db_query:
        registros['usernames'][data[1]] = {'name': data[0], 'password': data[2]}

    COOKIE_EXPIRY_DAYS = 30 #Tempo de expiração do cookie
    authenticator = stauth.Authenticate( # Cria o objeto de autenticação
        registros, #Dados dos usuários
        'random_cookie_name', #Nome do cookie
        'random_signature_key', #Chave de assinatura do cookie
        COOKIE_EXPIRY_DAYS, #Tempo de expiração do cookie
    )

    if 'clicou_registrar' not in st.session_state: #Se o usuario não clicou em registrar
        st.session_state['clicou_registrar'] = False #Cria a variavel de estado do botão de registrar

    if st.session_state['clicou_registrar']== False: #Se o usuario não clicou em registrar
        login_form(authenticator= authenticator) #Cria o formulario de login
    else:
        usuario_form()  #Cria o formulario de usuario

def login_form(authenticator):
    name, authentication_status, username = authenticator.login('Login') # Cria o formulario de login
    if authentication_status: # Se o usuario estiver logado
        authenticator.logout('Logout', 'main') #Cria o botão de logout
        st.write(f'*{name} está logado!*')
        st.title('AREA DO DASHBOARD')
    elif authentication_status == False:
        st.error('Usuário ou senha incorretos')
    elif authentication_status == None: 
        st.warning('Insira um usuário e senha') 
        clicou_em_registrar = st.button("Registrar")
        if clicou_em_registrar:
            st.session_state['clicou_registrar'] = True
            st.rerun()

def confirmation_msg():
    hashed_password = stauth.Hasher([st.session_state.pswrd]).generate() # Cria a senha hasheada
    if st.session_state.pswrd != st.session_state.confirm_pswrd: # Se as senhas não conferirem
        st.warning('Senhas não conferem')
        sleep(3)
    elif consulta(st.session_state.user):  #se o usuario já existir
        st.warning('Nome de usuário já existe.')
        sleep(3)
    else:
        add_registro(st.session_state.nome,st.session_state.user, hashed_password[0]) # Adiciona o usuario a tabela
        st.success('Registro efetuado!')
        sleep(3)

def usuario_form():
    with st.form(key="test", clear_on_submit=True): # Cria o formulario de usuario
        nome = st.text_input("Nome", key="nome")
        username = st.text_input("Usuário", key="user")
        password = st.text_input("Password", key="pswrd", type="password")
        confirm_password = st.text_input("Confirm Password", key="confirm_pswrd", type="password")
        submit = st.form_submit_button(
            "Salvar", on_click=confirmation_msg,  # Chama a função de confirmação quando o botão é clicado
        )
    clicou_em_fazer_login = st.button("Fazer Login") # Cria o botão de fazer login
    if clicou_em_fazer_login:
        st.session_state['clicou_registrar'] = False  # Altera o estado do botão de registrar para False
        st.rerun()


if __name__ == '__main__':
    main()