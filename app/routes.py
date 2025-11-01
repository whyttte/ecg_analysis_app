from flask import render_template, request, redirect, url_for, session
from app import app
import os
import pandas as pd
import plotly.express as px
import plotly.io as pio
from app.analysis import analyze_ecg

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file:
            filename = file.filename
            filepath = os.path.join('uploads', filename)
            file.save(filepath)

            # Read the file and store data in session
            try:
                if filename.endswith('.csv'):
                    df = pd.read_csv(filepath)
                elif filename.endswith('.txt'):
                    df = pd.read_csv(filepath, delimiter='\\s+')
                elif filename.endswith(('.xls', '.xlsx')):
                    df = pd.read_excel(filepath)
                else:
                    return "Unsupported file type"

                session['filepath'] = filepath
                session['sampling_rate'] = int(request.form['sampling_rate'])
                return redirect(url_for('analysis'))
            except Exception as e:
                return str(e)

    return render_template('upload.html')

@app.route('/analysis')
def analysis():
    if 'filepath' in session:
        filepath = session['filepath']
        try:
            if filepath.endswith('.csv'):
                df = pd.read_csv(filepath)
            elif filepath.endswith('.txt'):
                df = pd.read_csv(filepath, delimiter='\\s+')
            elif filepath.endswith(('.xls', '.xlsx')):
                df = pd.read_excel(filepath)
            else:
                return "Unsupported file type"
        except Exception as e:
            return str(e)

        sampling_rate = session.get('sampling_rate', 360) # Default to 360 if not in session
        interpretation, peaks = analyze_ecg(df, sampling_rate)

        # Assume the first column is time and the second is the ECG signal
        time_col = df.columns[0]
        signal_col = df.columns[1]

        fig = px.line(df, x=time_col, y=signal_col, title='ECG Signal')
        fig.add_scatter(x=df[time_col][peaks], y=df[signal_col][peaks], mode='markers', name='R-peaks')
        plot_div = pio.to_html(fig, full_html=False)

        activities = session.get('activities', [])
        return render_template('analysis.html', plot_div=plot_div, interpretation=interpretation, activities=activities)
    else:
        return render_template('analysis.html', plot_div="", interpretation="No data uploaded yet.", activities=[])

@app.route('/activity_log', methods=['GET', 'POST'])
def activity_log():
    if 'activities' not in session:
        session['activities'] = []

    if request.method == 'POST':
        activity = {
            'activity': request.form['activity'],
            'start_time': request.form['start_time'],
            'end_time': request.form['end_time']
        }
        activities = session['activities']
        activities.append(activity)
        session['activities'] = activities
        return redirect(url_for('activity_log'))

    return render_template('activity_log.html', activities=session['activities'])
