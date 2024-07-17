import speechmatics
import sounddevice as sd
import queue
import pygame
import os


API_KEY = os.environ.get("API_KEY")
LANGUAGE = "en"
CONNECTION_URL = f"wss://eu2.rt.speechmatics.com/v2/{LANGUAGE}"
DEVICE_INDEX = -1
CHUNK_SIZE = 1024
QUEUE = queue.Queue()
SAMPLE_RATE = 44_100

class RawInputStreamWrapper:
    def __init__(self, wrapped: sd.RawInputStream):
        self.wrapped: sd.RawInputStream = wrapped

    def read(self, frames):
        return bytes(self.wrapped.read(frames)[0])


class SMTranscribe:
    def transcript_handler(self, message):
        if message.get('results', None):
            for results in message['results']:
                QUEUE.put(results['alternatives'][0]['content'])

    def run(self):
        # Define connection parameters
        if API_KEY is None:
            raise RuntimeError("API_KEY not set")

        conn = speechmatics.models.ConnectionSettings(
            url=CONNECTION_URL,
            auth_token=API_KEY,
        )
        self.ws = speechmatics.client.WebsocketClient(conn)
        self.ws.add_event_handler(
            event_name=speechmatics.models.ServerMessageType.AddPartialTranscript,
            event_handler=self.transcript_handler,
        )

        transcription_conf = speechmatics.models.TranscriptionConfig(
            language=LANGUAGE,
            enable_partials=True,
            max_delay=0.7,
            max_delay_mode="fixed",
            punctuation_overrides={
                "permitted_marks": [],
            },
        )

        settings = speechmatics.models.AudioSettings()
        settings.encoding = "pcm_f32le"
        settings.sample_rate = SAMPLE_RATE
        settings.chunk_size = CHUNK_SIZE

        print("Starting transcription")
        try:
            with sd.RawInputStream(channels=1, samplerate=44_100, dtype="float32") as stream:
                self.ws.run_synchronously(RawInputStreamWrapper(stream), transcription_conf, settings)
        except:
            print("Shutting down transcriber")


def display_text(word, screen, background_color, text_color):
    screen.fill(background_color)
    font = pygame.font.Font(None, 26)
    text_surface = font.render(word, True, text_color)
    screen.blit(text_surface, (20, 20))
    pygame.display.flip()
