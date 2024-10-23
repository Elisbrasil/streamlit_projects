import streamlit as st


mensagens_fict = [
    {'nome_usuario': 'Adriano',
      'conteudo': 'Olá Juli'},
    {'nome_usuario': 'Juliano',
      'conteudo': 'Olá Adri'}, ]

def pagina_chat():
    st.title("💬 Teste de chat")
    st.divider()

    if not 'mensagens' in st.session_state: #Se não tiver a variável mensagens na sessão do usuário, ela é criada
        st.session_state['mensagens'] = mensagens_fict #Adiciona a variável mensagens na sessão do usuário

    mensagens = st.session_state['mensagens']  #Recupera a variável mensagens da sessão do usuário
    usuario_logado = "Adriano"

    for mensagem in mensagens: #Para cada mensagem na lista de mensagens
        nome_usuario = 'user' if mensagem['nome_usuario'] == usuario_logado else mensagem['nome_usuario']  #Recupera o nome do usuário da mensagem, se o nome do usuário for igual ao usuário logado, ele é substituído por 'user'
        avatar = None if mensagem['nome_usuario'] == usuario_logado else '😎'
        chat = st.chat_message(nome_usuario, avatar=avatar) #Cria uma caixa de chat com o nome do usuário e o avatar
        chat.markdown(mensagem['conteudo']) #Adiciona o conteúdo da mensagem na caixa de chat

def main():
    pagina_chat()


if __name__ == "__main__":
    main()