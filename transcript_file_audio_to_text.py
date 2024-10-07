import streamlit as st
from pydub import AudioSegment
import speech_recognition as sr
from io import BytesIO

# Função para converter MP3 para WAV em memória
def convert_mp3_to_wav(mp3_bytes):
    audio = AudioSegment.from_mp3(BytesIO(mp3_bytes))
    wav_buffer = BytesIO()
    audio.export(wav_buffer, format="wav")
    wav_buffer.seek(0)
    return wav_buffer

# Função para dividir o áudio em segmentos com sobreposição
def split_audio(audio_bytes, segment_duration_ms, overlap_ms):
    audio = AudioSegment.from_wav(BytesIO(audio_bytes))
    segments = []
    step = segment_duration_ms - overlap_ms  # Definir o passo com base na sobreposição
    for i in range(0, len(audio), step):
        segment = audio[i:i + segment_duration_ms]
        segments.append(segment)
    return segments

# Função para transcrever cada segmento usando um buffer em memória
def transcribe_segment(segment, recognizer):
    # Exportar o segmento para um buffer de memória (BytesIO)
    audio_buffer = BytesIO()
    segment.export(audio_buffer, format="wav")
    audio_buffer.seek(0)

    with sr.AudioFile(audio_buffer) as source:
        audio = recognizer.record(source)  # Ler o segmento de áudio
    
    try:
        # Usar o serviço de reconhecimento do Google
        text = recognizer.recognize_google(audio, language="pt-BR")
        return text
    except sr.UnknownValueError:
        return "[Inaudível]"
    except sr.RequestError as e:
        return f"[Erro: {e}]"

# Função para transcrever o áudio inteiro em linhas e remover duplicatas
def transcribe_audio_by_lines(wav_bytes, segment_duration_sec, overlap_sec):
    recognizer = sr.Recognizer()
    segment_duration_ms = segment_duration_sec * 1000  # Converter segundos para milissegundos
    overlap_ms = overlap_sec * 1000  # Sobreposição em milissegundos
    
    # Dividir o áudio em segmentos com sobreposição
    segments = split_audio(wav_bytes, segment_duration_ms, overlap_ms)
    
    # Transcrever cada segmento e armazenar como uma linha
    transcription_lines = []
    previous_transcription = ""  # Para armazenar o último segmento transcrito
    for i, segment in enumerate(segments):
        transcription = transcribe_segment(segment, recognizer)
        
        # Remover frases duplicadas comparando com a transcrição anterior
        if transcription != previous_transcription:
            transcription_lines.append(transcription)
            previous_transcription = transcription  # Atualiza para a próxima comparação
    
    return transcription_lines

# Interface do Streamlit
st.title("Transcrição de Áudio MP3 para Texto")

# Upload de arquivo MP3
uploaded_file = st.file_uploader("Faça upload de um arquivo MP3", type=["mp3"])

if uploaded_file:
    # Converter MP3 para WAV em memória
    wav_buffer = convert_mp3_to_wav(uploaded_file.read())
    
    # Transcrever o áudio em segmentos de 5 segundos com sobreposição de 1 segundo
    segment_duration_sec = 5  # Duração de cada segmento em segundos
    overlap_sec = 1  # Sobreposição de 1 segundo
    transcriptions = transcribe_audio_by_lines(wav_buffer.read(), segment_duration_sec, overlap_sec)

    # Exibir as transcrições no Streamlit
    st.subheader("Transcrição:")
    for line in transcriptions:
        st.write(line)

    # Botão para baixar a transcrição completa
    transcriptions_text = "\n".join(transcriptions)
    st.download_button("Baixar Transcrição", data=transcriptions_text, file_name="transcricao_segmentada.txt", mime="text/plain")
