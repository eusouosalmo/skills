---
name: cutting-raw-takes
description: Cuts the raw recordings of a talking-head Reel or Short into a rough cut, joining the clips in recording order, picking the take to keep for each line and dropping backstage talk and silences, with a takes table approved before anything is rendered. Use when the user hands over the raw clips of a video and wants them joined and cleaned of bad takes and pauses, ready to caption (corte bruto, juntar os brutos, tirar tomadas ruins, tirar silêncio).
compatibility: Needs ffmpeg and a Whisper with word timestamps (faster-whisper or whisper.cpp). Memory caps (scripts/run_capped.sh) use systemd-run or prlimit on Linux and WSL. Multiple-choice questions use the agent's question tool when it has one (AskUserQuestion in Claude Code).
metadata:
  status: beta
---

# Cutting raw takes

The author records a vertical talking-head video in one or more raw clips, says each line until it comes out right, talks to whoever is filming in between, and closes a take by saying "Corta". This skill turns those clips into the rough cut the author would have made by hand: every line once, in the take the author would pick, with no pause that drags. Write everything the author reads in pt-BR.

Each rule below comes with its reason. When a case falls outside the examples, decide by the reason.

## Memory

Run every process that decodes media or loads a model through `bash scripts/run_capped.sh <command>`, one at a time. It sizes the cap to the memory free on this machine and applies it only where a runaway process can take the system down (Linux and WSL); a process past the cap dies alone, where without it one ffmpeg can freeze a WSL VM. Render the cut piece by piece and join the pieces with the concat demuxer (`-c copy`): a single `filter_complex` with one trim per piece holds every piece in memory at once, and a 3-minute 4K clip with 63 pieces passed 11 GB.

## 1. Ask the output form

Before any heavy work, ask how the author wants the cut, as a multiple-choice question with the recommended option first and one line on how to use each:

1. **Vídeo do corte (recomendado para legendar no CapCut):** um mp4 com o corte pronto; importa no CapCut, gera a legenda automática e segue a edição.
2. **Arquivos soltos:** o mp4, o SRT do que ficou e a lista de cortes (`cortes.json`, arquivo, início e fim de cada trecho) para montar em qualquer editor.

The author decides what they will do with the cut next; producing a file they then have to convert wastes the render.

Done when the author picked a form (or, when they are away, the question is written down with the option taken).

## 2. Time the words and the silences

1. Order the clips by recording time (creation date or the timestamp in the file name) and keep that order: the author records the script in sequence, so the order of recording is the order of the video.
2. Transcribe each clip with word timestamps (language pt).
3. Find the speech edges with `silencedetect` (about -35 dB, 0.25 s) on each clip. Whisper stretches words over the pauses around them, so the silence detector, not the word times, says where speech starts and stops. Keep -35 dB for where speech starts: below about -40 dB the detector takes the breath before a phrase for speech, and the cut opens on a breath while the author is still raising the mic. Take where speech stops a second pass at about -50 dB, because a word's tail fades softer than its onset and -35 dB clips it.
4. Measure the level of every stretch of speech (the 90th percentile of its 10 ms RMS) and look at one frame from its middle. Many authors read the script to themselves, turned to the screen, before saying a line to the camera. With the mic away from the mouth that reading sits 10 to 20 dB below the takes (-33 to -45 dB against -18 to -27 in one recording), and the frame shows the author's back or profile. Quiet speech is the sign to check, not to keep: lowering the threshold to catch it lets the readings in. Lay the frames out as one contact sheet per clip (ImageMagick `montage`), each labelled with clip, start and level, so one look shows which stretches face the camera. Read the sheet together with the transcript: level, image and words agreeing is what tells a take from a reading, and a loud stretch facing the camera with no words in the transcript is a take Whisper missed, so transcribe it on its own.

Done when every clip has its words with times, its silence ranges, and a level and a frame for each stretch.

## 3. Build the takes table

Read the transcript as a script and split it into **lines** (one sentence or idea each). For every line said more than once, the attempts are its **takes**. Give each stretch of speech one status:

- **keep**: the take of a line that goes in the video.
- **take**: another attempt at a kept line: a false start, a take broken off, a partial repeat, the same line reworded.
- **backstage**: talk outside the script: to whoever is filming, about framing, light or the phone, frustration at a fumbled line, the spoken "Corta" and whatever leads into a new attempt ("não, deixa, vou gravar de novo"). Also a script line read aloud away from the camera (step 2.4), however complete and close to the script it is: the viewer sees the author's back.
- **warm-up**: what the author says before the first line of the script to get going ("bora trocar um papo sobre..."). The video opens on the hook, because the first one to three seconds decide whether the viewer stays.
- **ask**: a stretch that is in the script's voice but may be off topic. Content is the author's call, so it stays until they answer.

Pick the take to keep by these, in order:

1. To the camera: facing it, at the level of the other takes. A reading in step 2.4 is not a take.
2. Complete: the whole line, said through to its end.
3. In the author's spoken register: the form of address to the viewer they use in the rest of the recording and in the script (for eusouosalmo, "tu" and "teu", not "você" and "seu"; a "seu" about someone else, "no seu site" of a shop, is not address). The register is part of the author's voice, and a take in the other register reads as someone else, so it outranks a reworded word ("mensagem" for "senha") and a small slip the caption smooths over ("com ela com o texto").
4. Not glued to backstage talk. The last take is often the best, because the author repeats until it is right, but a take that starts right after "deixa, vou gravar de novo" can be worse than the first.

Keep whole takes. Joining the start of one take to the end of another inside a line puts a jump cut in the middle of a sentence with the face on screen, so offer it only as an alternative on a **dúvida** row. The exception is a line the author only got right to the camera in halves, saying the second half again on its own: that is a pickup the author planned, so join the two halves and say so in the reason.

A stretch can hold its own false start: the author begins the line, stops, and begins again with no pause long enough to split the stretch ("essa ligação... essa ligação do teu feed"). Cut the stretch at the restart. A transcript of the whole clip often hides the restart by merging both tries into one sentence, so transcribe each kept stretch on its own before showing the table.

Mark every line where the choice is close as **dúvida** and say what tells the takes apart.

Show the table in the chat, in order, one row per stretch: clip, start and end, status, the words, and the reason when the status is not **keep**. Then ask the author to approve or change it, with the **dúvida** and **ask** rows called out above the table. The table is the edit: changing a row costs a word, changing a render costs another render.

Done when the author approved the table (or, when they are away, the table and the questions are written down with the choices taken).

## 4. Cut

1. Cut each kept stretch at the speech edges the silence detector found, and bring every pause longer than about 0.35 s, inside a stretch or between two, down to about 0.2 s: about 0.1 s of silence on each side of the cut. That is a short breath between phrases, so the edit keeps moving without sounding clipped; the author cuts this tight by eye, and cutting every such pause lands closest to their length. When the author has a style file with their margins, use those.
2. Never cut inside a word and never reorder lines.
3. Render each piece on its own under the memory cap (H.264, crf 18, a 20 ms audio fade at each edge so the joins do not click), then join with the concat demuxer.
4. Transcribe the joined cut once more, in windows of about 30 s, and read it as a script: every line once, in order, with nothing from the backstage rows. A single pass over the whole cut drops short or quiet lines, so a line that seems to be missing gets its own window before it counts as missing. Then look at one frame per piece: every piece faces the camera.

Done when the re-read finds every kept line once and nothing else, and the files of the chosen form exist.

## 5. Hand back

Tell the author the final length against the raw length, where the files are, and the rows they may want to revisit (the **dúvida** and **ask** ones).
