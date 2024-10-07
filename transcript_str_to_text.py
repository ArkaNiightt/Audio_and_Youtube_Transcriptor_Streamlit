import re
import streamlit as st

# Função para limpar o conteúdo removendo índices e timestamps
def limpar_srt(conteudo):
    # Regex para capturar e remover timestamps
    padrao_timestamps = r"\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3}"
    
    # Remover os timestamps
    conteudo_limpo = re.sub(padrao_timestamps, '', conteudo)

    # Remover linhas que contêm apenas números isolados (os índices)
    conteudo_limpo = re.sub(r'^\d+\s*$', '', conteudo_limpo, flags=re.MULTILINE)
    
    # Remover quebras de linha múltiplas
    conteudo_limpo = re.sub(r'\n+', '\n', conteudo_limpo).strip()
    
    return conteudo_limpo

# Título da aplicação
st.title('Limpeza de Arquivo .srt')

# Upload do arquivo .srt
arquivo_entrada = st.file_uploader("Envie o arquivo .srt", type="srt")

if arquivo_entrada is not None:
    # Ler o conteúdo do arquivo .srt
    conteudo = arquivo_entrada.read().decode("utf-8")
    
    # Limpar o conteúdo do arquivo
    conteudo_limpo = limpar_srt(conteudo)
    
    # Exibir o conteúdo original e o conteúdo limpo
    st.subheader("Conteúdo Original")
    st.text_area("Conteúdo Original", conteudo, height=300)
    
    st.subheader("Conteúdo Limpo")
    st.text_area("Conteúdo Limpo", conteudo_limpo, height=300)
    
    # Opção para download do arquivo limpo
    st.download_button(
        label="Baixar arquivo limpo",
        data=conteudo_limpo,
        file_name="arquivo_limpo.txt",
        mime="text/plain"
    )
