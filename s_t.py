import os
import streamlit as st
from bokeh.models.widgets import Button
from bokeh.models import CustomJS
from streamlit_bokeh_events import streamlit_bokeh_events
from PIL import Image
import time
import glob

from gtts import gTTS
from googletrans import Translator

# Estilo CSS para fuente cursiva
st.markdown("""
    <style>
    .italic-text {
        font-style: italic;
    }
    </style>
""", unsafe_allow_html=True)

# Título y subtítulo en cursiva
st.markdown('<h1 class="italic-text">TRADUCTOR.</h1>', unsafe_allow_html=True)
st.markdown('<h3 class="italic-text">Escucho lo que quieres traducir.</h3>', unsafe_allow_html=True)

image = Image.open('OIG7.jpg')
st.image(image, width=300)

# Sidebar con texto en cursiva
with st.sidebar:
    st.markdown('<h3 class="italic-text">Traductor.</h3>', unsafe_allow_html=True)
    st.markdown(
        '<p class="italic-text">Presiona el botón, cuando escuches la señal habla lo que quieres traducir, luego selecciona la configuración de lenguaje que necesites.</p>',
        unsafe_allow_html=True
    )

# Instrucción principal en cursiva
st.markdown('<p class="italic-text">Toca el botón y habla lo que quieres traducir</p>', unsafe_allow_html=True)

# Botón de voz
stt_button = Button(label=" Escuchar  🎤", width=300, height=50)

stt_button.js_on_event("button_click", CustomJS(code="""
    var recognition = new webkitSpeechRecognition();
    recognition.continuous = true;
    recognition.interimResults = true;

    recognition.onresult = function (e) {
        var value = "";
        for (var i = e.resultIndex; i < e.results.length; ++i) {
            if (e.results[i].isFinal) {
                value += e.results[i][0].transcript;
            }
        }
        if (value != "") {
            document.dispatchEvent(new CustomEvent("GET_TEXT", {detail: value}));
        }
    }
    recognition.start();
"""))

# Procesamiento del reconocimiento de voz
result = streamlit_bokeh_events(
    stt_button,
    events="GET_TEXT",
    key="listen",
    refresh_on_update=False,
    override_height=75,
    debounce_time=0
)

if result:
    if "GET_TEXT" in result:
        st.write(result.get("GET_TEXT"))

    try:
        os.mkdir("temp")
    except:
        pass

    st.markdown('<h2 class="italic-text">Texto a Audio</h2>', unsafe_allow_html=True)
    translator = Translator()

    text = str(result.get("GET_TEXT"))

    in_lang = st.selectbox(
        "Selecciona el lenguaje de Entrada",
        ("Inglés", "Español", "Árabe", "Coreano", "Danés", "Japonés"),
    )

    if in_lang == "Inglés":
        input_language = "en"
    elif in_lang == "Español":
        input_language = "es"
    elif in_lang == "Árabe":
        input_language = "ar"
    elif in_lang == "Coreano":
        input_language = "ko"
    elif in_lang == "Danés":
        input_language = "da"
    elif in_lang == "Japonés":
        input_language = "ja"

    out_lang = st.selectbox(
        "Selecciona el lenguaje de salida",
        ("Inglés", "Español", "Árabe", "Coreano", "Danés", "Japonés"),
    )

    if out_lang == "Inglés":
        output_language = "en"
    elif out_lang == "Español":
        output_language = "es"
    elif out_lang == "Árabe":
        output_language = "ar"
    elif out_lang == "Coreano":
        output_language = "ko"
    elif out_lang == "Danés":
        output_language = "da"
    elif out_lang == "Japonés":
        output_language = "ja"

    english_accent = st.selectbox(
        "Selecciona el acento",
        (
            "Defecto",
            "Español",
            "Reino Unido",
            "Estados Unidos",
            "Canada",
            "Australia",
            "Irlanda",
            "Sudáfrica",
        ),
    )

    if english_accent == "Defecto":
        tld = "com"
    elif english_accent == "Español":
        tld = "com.mx"
    elif english_accent == "Reino Unido":
        tld = "co.uk"
    elif english_accent == "Estados Unidos":
        tld = "com"
    elif english_accent == "Canada":
        tld = "ca"
    elif english_accent == "Australia":
        tld = "com.au"
    elif english_accent == "Irlanda":
        tld = "ie"
    elif english_accent == "Sudáfrica":
        tld = "co.za"

    # Función de traducción y generación de audio
    def text_to_speech(input_language, output_language, text, tld):
        translation = translator.translate(text, src=input_language, dest=output_language)
        trans_text = translation.text
        tts = gTTS(trans_text, lang=output_language, tld=tld, slow=False)
        try:
            my_file_name = text[0:20]
        except:
            my_file_name = "audio"
        tts.save(f"temp/{my_file_name}.mp3")
        return my_file_name, trans_text

    display_output_text = st.checkbox("Mostrar el texto")

    if st.button("convertir"):
        result, output_text = text_to_speech(input_language, output_language, text, tld)
        audio_file = open(f"temp/{result}.mp3", "rb")
        audio_bytes = audio_file.read()
        st.markdown('<h3 class="italic-text">Tu audio:</h3>', unsafe_allow_html=True)
        st.audio(audio_bytes, format="audio/mp3", start_time=0)

        if display_output_text:
            st.markdown('<h3 class="italic-text">Texto de salida:</h3>', unsafe_allow_html=True)
            st.markdown(f'<p class="italic-text">{output_text}</p>', unsafe_allow_html=True)

    # Limpieza de archivos temporales
    def remove_files(n):
        mp3_files = glob.glob("temp/*mp3")
        if len(mp3_files) != 0:
            now = time.time()
            n_days = n * 86400
            for f in mp3_files:
                if os.stat(f).st_mtime < now - n_days:
                    os.remove(f)
                    print("Deleted ", f)

    remove_files(7)


        
    
