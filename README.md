# Overview
This tool creates an audio file from a transcript

# Dependencies
## [OpenTTS](https://github.com/synesthesiam/opentts)
OpenTTS is a popular text to speech server. It's open-sourced and written in python. It's released under the MIT license.
## Docker/Podman
- [Docker](https://www.docker.com/)
- [Podman](https://podman.io/): podman is free, open-source, and an alternative to Docker

# Transcript file schema
```
{
	"utterances": [
		{
			"participant_id": "p1",
			"start_offset_millis": 0,
			"end_offset_millis": 0,
			"text": "How are you doing?"
		},
		{
			"participant_id": "p2",
			"start_offset_millis": 10000,
			"end_offset_millis": 10000,
			"text": "I am doing good"
		},
		{
			"participant_id": "p1",
			"start_offset_millis": 25000,
			"end_offset_millis": 25000,
			"text": "How can I help you?"
		}
	]
}
```

# How to run
- Download or clone [OpenTTS](https://github.com/synesthesiam/opentts)
- cd to `opentts` and run `docker run -it -p 5500:5500 synesthesiam/opentts:<LANGUAGE>`
- cd to `transcript-to-audio` and run `python main.py <transcript_file_path> <output_dir> <tmp_dir>`

