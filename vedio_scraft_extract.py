import os
from ffmpy3 import FFmpeg
from pydub.audio_segment import AudioSegment
from pymediainfo import MediaInfo
from aip import AipSpeech


def vedio_to_pcm(file):
    inputfile = file
    file_type = file.split('.')[-1]
    outputfile = inputfile.replace(file_type, 'pcm')
    ff = FFmpeg(executable='ffmpeg',
                global_options=['-y'],
                inputs={inputfile: None},
                outputs={outputfile: '-acodec pcm_s16le -f s16le -ac 1 -ar 16000'})
    ff.cmd
    ff.run()
    return outputfile

def vedio_to_wav(file):
    inputfile = file
    file_type = file.split('.')[-1]
    outputfile = inputfile.replace(file_type, 'wav')
    ff = FFmpeg(executable='ffmpeg',
                global_options=['-y'],
                inputs={inputfile: None},
                outputs={outputfile: None})
    ff.cmd
    ff.run()
    return outputfile

def wav_split(path):
    file = vedio_to_wav(path)
    main_wav_path=file
    path=os.path.dirname(file)+'/'
    sound_len=int(MediaInfo.parse(main_wav_path).to_data()['tracks'][0]['duration'])
    sound=AudioSegment.from_mp3(main_wav_path)
    part_file_list=list()
    min_ = sound_len/1000
    if min_ > 60:
        n=int(min_//60)
        print(type(n))
        if n*60<min_:
            n+=1
    for i in range(n):
        start_time=i*60*1000+1
        end_time=(i+1)*60*1000
        if end_time>sound_len*1000:
            end_time=sound_len*1000
        word=sound[start_time:end_time]
        part_file_name='part_sound_{}.wav'.format(i)
        word.export(part_file_name,format="wav")
        part_file_list.append(part_file_name)
    return part_file_list

def BAIDU_ASR(wavfile):
   
    pcm_file = vedio_to_pcm(wavfile)
    def get_file_content(file):
        with open(file,'rb') as fp:
            return fp.read()

    """ 你的 APPID AK SK """
    APP_ID = '17872933'
    API_KEY = 'mwYodxwWVfjSizLZevxPYGCG'
    SECRET_KEY = 'BFYyRhkMagHnam0aFuvsNg52n0bwWRME'
    client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)
    result = client.asr(get_file_content(pcm_file),'wav',16000,{'dev_pid':1537})
    return result

def perfect_path(path,list_):
    tmp_path = []
    for i in list_:
        tt = path+'\\'+ i
        tmp_path.append(tt)
    return tmp_path

if __name__ == "__main__":
    tmp = []
    #要提取文稿的视频路径
    path = 'D:\\期权'
    name_list = os.listdir(path)
    tmp_path = perfect_path(path,name_list)
    print(tmp_path)
    for i in tmp_path:
        print(i)
        waiting_list = wav_split(i)
        output = open(i+'.txt','w',encoding='gbk')
        for i in waiting_list:
            tmp = BAIDU_ASR(i)['result'][0]
            output.write(tmp)
        output.close()
        remove_pcm = []
        for i in waiting_list:
            remove_pcm.append(i.split('.')[0]+'.pcm')
            os.remove(i)
        for i in remove_pcm:
            os.remove(i)