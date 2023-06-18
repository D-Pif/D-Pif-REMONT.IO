import argparse
import os
from moviepy.editor import VideoFileClip
import speech_recognition as sr

class Transcriber:
    def __init__(self, file_path, language):
        """
        Инициализация объекта Transcriber.

        Args:
            file_path (str): Путь к файлу.
            language (str): Язык (ru/en).
        """
        self.file_path = file_path
        self.language = language

    def transcribe_file(self):
        """
        Выполняет транскрибацию файла и сохраняет результат в текстовый документ.
        """
        file_extension = os.path.splitext(self.file_path)[1].lower()

        if file_extension in ['.wav', '.mp3']:
            transcript = self._transcribe_audio()
        elif file_extension in ['.mp4', '.avi']:
            self._convert_video()
            tempfile = "temp_audio.wav"
            transcript = self._transcribe_audio(tempfile)
            os.remove(tempfile)
        else:
            raise ValueError('Unsupported file type')

        output_file = 'transcript.txt'
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(transcript)

        print('Транскрибация завершена. Результат сохранен в файле', output_file)

    def _transcribe_audio(self, file_path=None):
        """
        Выполняет транскрибацию аудиофайла.

        Args:
            file_path (str): Путь к аудиофайлу. Если не указан, используется file_path из инициализации.

        Returns:
            str: Результат транскрибации.
        """
        if file_path is None:
            file_path = self.file_path

        recognizer = sr.Recognizer()
        audio_file = sr.AudioFile(file_path)

        with audio_file as source:
            audio = recognizer.record(source)

        if self.language == 'ru':
            transcript = recognizer.recognize_google(audio, language='ru-RU')
        elif self.language == 'en':
            transcript = recognizer.recognize_google(audio, language='en-US')
        else:
            raise ValueError('Unsupported language')

        return transcript

    def _convert_video(self):
        """
        Конвертирует видеофайл в аудиофайл формата WAV.

        Returns:
            str: Путь к временному аудиофайлу.
        """
        video = VideoFileClip(self.file_path)
        audio = video.audio
        temp_audio_path = "temp_audio.wav"
        audio.write_audiofile(temp_audio_path)
        return temp_audio_path


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Транскрипция аудио- и видеофайлов')
    parser.add_argument('file_path', type=str, help='Путь к файлу')
    parser.add_argument('language', type=str, help='Язык (ru/en)')

    args = parser.parse_args()

    transcriber = Transcriber(args.file_path, args.language)
    transcriber.transcribe_file()