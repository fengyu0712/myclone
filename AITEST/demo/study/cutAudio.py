# from pydub import AudioSegment
# from pydub.utils import make_chunks
import wave


path="E:\\唤醒小美音频\\001M26_01_40_0001.wav"

with wave.open(path,'rb') as f:
    # f = wave.open(path)
    print(f.getparams())
# myaudio = AudioSegment.from_file(path, "wav")
# chunk_length_ms = 1000  # 分块的毫秒数
# chunks = make_chunks(myaudio, chunk_length_ms)  # 将文件切割成1秒每块
#
# print(chunks)

# 保存切割的音频到文件

# for i, chunk in enumerate(chunks):
#     chunk_name = "chunk{0}.wav".format(i)
#     print
#     "exporting", chunk_name
#     chunk.export(chunk_name, format="wav")