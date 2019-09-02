import os
import wave
#import magic
import matplotlib.image as mpimg 
import matplotlib.pyplot as plt 
import urllib.request
from app import app
from flask import Flask, flash, request, redirect, render_template
from werkzeug.utils import secure_filename
from data_upload import dataprepocess

ALLOWED_EXTENSIONS = set(['wav','mp3'])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
	
@app.route('/')
def upload_form():
	return render_template('upload.html')

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
			print(filename)
			flash('file loaded successfully')
			nn = 'uploads/'+filename
			
			print(nn)

			

			
			dataprepocess(nn)

		   #aud = pre_process(w)
		   #model.load('.../model/ai_predict.pkl')  or use the weights.
		   #val = model.predict(aud)
		   #if conditions
			# The AI stuff goes here.  
			return redirect('/')
		else:
			flash('Only \'.wav\' and \'.mp3\' files are allowed.')
			return redirect(request.url)

if __name__ == "__main__":
	app.debug = True
	app.run()