import unittest
from app import app
import os
import pandas as pd
import numpy as np

class TestApp(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        # Create a dummy uploads folder if it doesn't exist
        if not os.path.exists('uploads'):
            os.makedirs('uploads')

    def test_upload_and_analysis(self):
        # Create a dummy ECG CSV file
        time = np.linspace(0, 10, 3600)
        signal = np.sin(2 * np.pi * 1 * time) + np.sin(2 * np.pi * 10 * time)
        df = pd.DataFrame({'time': time, 'signal': signal})
        df.to_csv('test_ecg.csv', index=False)

        with open('test_ecg.csv', 'rb') as f:
            response = self.app.post('/upload', data={
                'file': (f, 'test_ecg.csv'),
                'sampling_rate': '360'
            }, content_type='multipart/form-data', follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Average Heart Rate', response.data)
        self.assertIn(b'360 Hz', response.data)

    def test_log_activity(self):
        with self.app as c:
            with c.session_transaction() as sess:
                sess['activities'] = []

            response = self.app.post('/activity_log', data={
                'activity': 'Running',
                'start_time': '2024-01-01T10:00',
                'end_time': '2024-01-01T11:00'
            }, follow_redirects=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Running', response.data)

if __name__ == '__main__':
    unittest.main()
