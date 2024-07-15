import speechmatics
import sounddevice as sd

API_KEY = "gn9nO1Bjx03leYBlTQfhkWC5hMXr0E2i"
LANGUAGE = "en"
CONNECTION_URL = f"wss://eu2.rt.speechmatics.com/v2/{LANGUAGE}"
DEVICE_INDEX = -1
CHUNK_SIZE = 1024


SAMPLE_RATE = 44_100
class RawInputStreamWrapper:
    def __init__(self, wrapped: sd.RawInputStream):
        self.wrapped: sd.RawInputStream = wrapped

    def read(self, frames):
        return bytes(self.wrapped.read(frames)[0])


class SMTranscribe:
    def __init__(self) -> None:
        self.word = "DEFAULT"
    
    def transcript_handler(self, message):
        if message.get('results', None):
            self.word = message['results'][0]['alternatives'][0]['content']
            print(self.word, self.file)
    
    def run(self):
        # Define connection parameters
        conn = speechmatics.models.ConnectionSettings(
            url=CONNECTION_URL,
            auth_token=API_KEY,
        )
        self.ws = speechmatics.client.WebsocketClient(conn)
        self.ws.add_event_handler(
            event_name=speechmatics.models.ServerMessageType.AddTranscript,
            event_handler=self.transcript_handler,
        )

        transcription_conf = speechmatics.models.TranscriptionConfig(
            language=LANGUAGE,
            enable_partials=True,
            max_delay=1.6,
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

transcriber = SMTranscribe()
transcriber.run()