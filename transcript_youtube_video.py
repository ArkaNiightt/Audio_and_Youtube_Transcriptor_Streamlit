import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi
import re

def extract_video_id(url_or_id):
    """
    Função para extrair o ID do vídeo de uma URL completa ou devolver o ID se já for fornecido.
    """
    video_id_match = re.search(r'(?:v=|\/)([0-9A-Za-z_-]{11}).*', url_or_id)
    if video_id_match:
        return video_id_match.group(1)
    return url_or_id

def get_transcript(video_id, language_code='pt'):
    try:
        # Obtém a transcrição do vídeo especificando o código da língua
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=[language_code])
        # Formata a transcrição para exibir no Streamlit
        formatted_transcript = '\n'.join([entry['text'] for entry in transcript])
        return formatted_transcript
    except Exception as e:
        return f"Erro ao recuperar a transcrição: {str(e)}"

# Configura o título do aplicativo
st.title("Transcrição de Vídeo do YouTube")

# Campo de entrada para o ID ou URL do vídeo
video_input = st.text_input("Insira o ID ou URL do vídeo do YouTube:")

# Botão para obter a transcrição
if st.button("Obter Transcrição"):
    if video_input:
        # Extrai o ID do vídeo (caso seja uma URL completa)
        video_id = extract_video_id(video_input)
        
        # Chama a função para obter a transcrição
        transcript = get_transcript(video_id)
        
        # Exibe a transcrição no app
        st.text_area("Transcrição", transcript, height=300)
        
        # Opção de download da transcrição
        if transcript and "Erro" not in transcript:
            st.download_button(label="Baixar Transcrição",
                               data=transcript,
                               file_name=f"transcricao_{video_id}.txt",
                               mime="text/plain")
    else:
        st.error("Por favor, insira um ID de vídeo válido.")
