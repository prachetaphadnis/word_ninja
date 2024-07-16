import speechmatics
import sounddevice as sd
import queue
import pygame
import threading


API_KEY = "gn9nO1Bjx03leYBlTQfhkWC5hMXr0E2i"
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
                # print(results['alternatives'][0]['content'])
                QUEUE.put(results['alternatives'][0]['content'])

    def run(self):
        # Define connection parameters
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

        print("Starting transcription (type Ctrl-C to stop):")
        with sd.RawInputStream(
                channels=1, samplerate=44_100, dtype="float32"
            ) as stream:
            self.ws.run_synchronously(RawInputStreamWrapper(stream), transcription_conf, settings)


def display_text(word, screen, background_color, text_color):
    screen.fill(background_color)
    font = pygame.font.Font(None, 26)
    text_surface = font.render(word, True, text_color)
    screen.blit(text_surface, (20, 20))
    pygame.display.flip()


def main():
    pygame.init()
    background_color = (255, 255, 255)
    text_color = (0, 0, 0)
    screen = pygame.display.set_mode([500, 500])
    screen.fill(background_color)
    pygame.display.flip()

    transcriber = SMTranscribe()
    thread = threading.Thread(target=transcriber.run)
    thread.start()

    # Run until the user asks to quit
    running = True
    word = ""
    while running:
        # Did the user click the window close button?
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            try:
                word = QUEUE.get(block=False)
            except:
                word = word
            else:
                print(word)
                display_text(word, screen, background_color, text_color)


    # Done! Time to quit.
    pygame.quit()


if __name__ == "__main__":
    main()

 