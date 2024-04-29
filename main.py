import whisper
from deep_translator import GoogleTranslator
import os


def translate(text, translated_lang):
    translated = GoogleTranslator(
        source='auto', target=translated_lang).translate(text)
    return translated


def separate_translate(text, translated_lang, result_folder_path):
    MAX_LENGTH = 4500
    chunks = [text[i:i+MAX_LENGTH] for i in range(0, len(text), MAX_LENGTH)]

    translated_chunks = []
    for chunk in chunks:
        translated_chunk = translate(chunk, translated_lang)
        translated_chunks.append(translated_chunk)

    translated_text = ''.join(translated_chunks)

    with open(f"{result_folder_path}/translated.txt", mode="w") as f:
        f.write(translated_text)

    return True


def yt_download(URL, result_folder_path):
    path = f"{result_folder_path}/target.mp4"
    os.system(f"yt-dlp -f best -v {URL} -o {path}")

    return True


def main():
    URL = input("Enter the YouTube URL to which you want to add subtitles:")
    translated_lang = input(
        "Please enter the subtitle language (language after translation):")
    result_folder_name = str(
        input("Specify the name of the folder in which to save the output results:"))

    result_folder_path = f"./result/{result_folder_name}"
    os.mkdir(result_folder_path)

    yt_download(URL, result_folder_path)

    model = whisper.load_model("medium")
    result = model.transcribe(f"{result_folder_path}/target.mp4")

    with open(f"{result_folder_path}/transcript.txt", mode="w") as f:
        f.write(result["text"])

    with open(f"{result_folder_path}/transcript.txt", 'r') as f:
        text = f.read()
    separate_translate(text, translated_lang, result_folder_path)

    return True


if __name__ == "__main__":
    main()
