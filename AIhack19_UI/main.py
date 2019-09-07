import os
import tkinter as tk
import time
from app import app
from flask import flash, request, redirect, render_template
from werkzeug.utils import secure_filename
from data_upload import dataprepocess
#import CRNN
#import torch
import numpy as np
import gui
ALLOWED_EXTENSIONS = set(['wav','mp3'])
#model = CRNN.CRNN()
#model.load_state_dict(torch.load("C:/Users/Gowtham Senthil/Desktop/LID/AIhack19_UI/TrialRunWeights.pth"))
    

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
	
@app.route('/')
def upload_form():
	return render_template('upload.html')

@app.route('/server', methods=['POST'])
def open_gui():
	flash("Live recorder started")
	# main = tk.Tk()
	# app = gui.App(main)
	gui.main()
	flash("Live recorder closed")
	return redirect('/')

@app.route('/', methods=['POST'])
def upload_file():
	if request.method == 'POST':
		# check if the post request has the file part
		if 'file' not in request.files:
			flash('No file part')
			return redirect(request.url)
		file = request.files['file']
		if file.filename == '':
			flash('No file selected for uploading')
			return redirect(request.url)
		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			flash('file loaded successfully')
			nn = 'uploads/'+filename
            
			Audio -> Image -> Probability
			imgs = dataprepocess(nn)
			noFrames = imgs.shape[0]
			imgs = torch.from_numpy(imgs)
			prob = model(imgs)
			prob = prob.tolist()
			if noFrames == 1:
			    ans = prob
			else:
			    ans = np.array(prob[0])
			    for i in range(1,noFrames):
			        ans = np.multiply(ans,np.array(prob[i]))
			    ans = list(ans)
			probabilites = [float(i)/sum(ans) for i in ans]
			#probabilites = [i*i for i in range(5)]
            # probabilites is the required ouput (List of 5 prob)
			flash(probabilites)
            
			return redirect('/')
		else:
			flash('Only \'.wav\' and \'.mp3\' files are allowed.')
			return redirect(request.url)

if __name__ == "__main__":
	app.debug = True
	app.run()