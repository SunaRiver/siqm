from scoring2 import scoring
import numpy as np
import tensorflow as tf
import time
from pickle import load
import urllib3
import pandas as pd

baseURL3 = 'http://api.thingspeak.com/update?api_key=ITD49AEM53BXFBWS'
http = urllib3.PoolManager()
while True:
	start = time.time()
	print("Calculating......................")
	print("Proses start.....................")
	new_model = tf.keras.models.load_model('model_ann_v5.h5')
	command = 'ffmpeg -i "http://raspberrypi:9981/stream/channel/354e01fbdb6e06f80b181f4635741b9c?ticket=4948b637d093b3b14ad98cf7b65d927017cb4426" -frames:v 5 -vf fps=2 image/output%d.jpg'
	score = scoring(command)
	#print(score)
	scaler = load(open('scaler.pkl','rb'))
	final_score = scaler.transform([[score["blok"], score["blur"], score["act"], score["temp"]]])
	#hasil_prediksi = np.ceil(new_model.predict(final_score))
	hasil_prediksi = new_model.predict(final_score)
	end = time.time()
	total_time = end-start
	print(f"Hasil Skor Prediksi = {hasil_prediksi}")
	print(f"======================= END SCORING ===========================")
	print(f"Waktu Proses = {total_time} detik \n \n")
	
	#Kirim ke Thingspeak
	data_scraping = pd.read_csv("/home/sr/data.csv")
	ss_skor = data_scraping['SS'].values
	snr_skor = data_scraping['SNR'].values
	f = http.request('GET', baseURL3 + "&field6=" + str(snr_skor[0]) + "&field7=" + str(ss_skor[0]) + "&field5=" + str(round(hasil_prediksi[0][0],2)))
