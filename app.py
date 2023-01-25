from flask import Flask, render_template, request, redirect
import qrcode
import json
import redis

app = Flask(__name__)
r = redis.Redis(host='localhost', port=6379, db=0)

@app.route('/')
def default():
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data("http://192.168.28.59:5000")
    qr.make(fit=True)
    img = qr.make_image(fill_color='black', back_color='white')
    img_file = 'static/qr.png'
    img.save(img_file)
    return render_template('index.html', img_file=img_file)

@app.route('/update_state', methods=['POST'])
def update_state():
    state = request.form['state']
    r.set('device_state', state)
    return redirect('/redirect')

@app.route('/redirect')
def redirect_route():
    state = r.get('device_state').decode("utf-8")
    if state == "scan":
        return render_template('scan.html')
    elif state == "redirect":
        return render_template('redirect.html')

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
