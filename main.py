import sys
import json
import requests
import subprocess

# Constants
JSON_FILE_EXT = ".json"
TMP_DIR = "/tmp"


def text_to_speech(text, speaker_voice, index, tmp_dir):
    params = {
        "text": text,
        "voice": "glow-speak:" + speaker_voice,
        "lang": "en",
        "vocoder": "high",
        "denoiserStrength": "0.005",
        "speakerId": "",
        "ssml": "false",
        "ssmlNumbers": "true",
        "ssmlDates": "true",
        "ssmlCurrency": "true",
        "cache": "false"
    }
    response = requests.get('http://localhost:5500', params=params)
    output_file_path = "{}/file_{}.wav".format(tmp_dir, index)
    with open(output_file_path, "wb") as f:
        f.write(response.content)
    return output_file_path


def process_transcript(transcript, tmp_dir):
    audio_chunks = []
    utterances = transcript["utterances"]
    voices = ["glow-speak:en-us_mary_ann", "larynx:cmu_rms-glow_tts"]
    for index, utterance in enumerate(utterances):
        participant_id = utterance["participant_id"]
        voice_id = hash(participant_id) % len(voices)
        text = utterance["text"]
        output_file_path = text_to_speech(text, voices[voice_id], index, tmp_dir)
        audio_chunk = {
            "file_path": output_file_path,
            "start": utterance["start_offset_millis"],
            "end": utterance["end_offset_millis"]
        }
        audio_chunks.append(audio_chunk)
    return audio_chunks


def main():
    args = sys.argv[1:]
    transcript_file = args[0]
    output_dir = args[1]
    tmp_dir = args[2]
    if len(transcript_file) == 0:
        print("transcript file is not provided")
        return
    if not transcript_file.endswith(JSON_FILE_EXT):
        print("only json files are supported for now")
        return
    with open(transcript_file, 'r') as f:
        transcript = json.load(f)
        audio_chunks = process_transcript(transcript, tmp_dir)
        input_audio_files = ""
        ffmpeg_filter_complex = "-filter_complex \""
        mix = "[0]"
        for index, audio_chunk in enumerate(audio_chunks):
            if index == 0:
                continue
            input_audio_files += "-i {} ".format(audio_chunk["file_path"])
            ffmpeg_filter_complex += "{}adelay{}|{}[{}]".format(index, audio_chunk["start"], audio_chunk["end"], index)
            mix += "[{}]".format(index)
        ffmpeg_filter_complex += mix
        ffmpeg_filter_complex += "amix={}".format(len(audio_chunks))
        ffmpeg_filter_complex += "\" "
        output_file = "{}/output.wav".format(output_dir)
        ffmpeg_cmd = "ffmpeg {}{}{}".format(mix, ffmpeg_filter_complex, output_file)
        subprocess.call(ffmpeg_cmd, shell=True)


if __name__ == '__main__':
    main()
