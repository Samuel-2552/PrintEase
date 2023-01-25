from flask import Flask, render_template, request, redirect
import qrcode
<<<<<<< Updated upstream
import json
import redis
=======
import uuid

qr_codes={}

flag = 0

app = Flask(__name__) 
>>>>>>> Stashed changes

app = Flask(__name__)
r = redis.Redis(host='localhost', port=6379, db=0)

@app.route('/')
<<<<<<< Updated upstream
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
=======
def index():
    return render_template('index.html')

@app.route('/upload',methods=["POST","GET"])
def getData():
    if request.method == 'POST':
        result = request.files['file']
        color = request.form.get('color')
        side = request.form.get('side')
        quantity = request.form.get('quantity')
        #print(color, side, quantity)
        result.save(result.filename)
        #os.remove(result.filename)
        # Create a unique identifier
        unique_id = str(uuid.uuid4())

        # Create the data to be encoded in the QR code, including the unique identifier
        #data = color + side + quantity + " data recieved + unique code next " + unique_id
        # Create the QR code instance
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        data="http://192.168.28.59:5000/scan/" + unique_id
        # Add the data to the QR code
        qr.add_data(data)
        qr.make(fit=True)

        # Create an image from the QR code instance
        img = qr.make_image(fill_color="black", back_color="white")

        # Save the image
        img.save("static/qr.png")   
        # Add the identifier to the qr_codes dictionary
        qr_codes[unique_id] = True

    return render_template('payment.html', qr_code_id=unique_id, data = flag )

# @app.route('/check_qr_code/<qr_code_id>')
# def check_qr_code(qr_code_id):
#     if qr_code_id in qr_codes:
#         return jsonify({'valid': True})
#     else:
#         return jsonify({'valid': False})

@app.route("/scan/<qr_code_id>")
def scan_qr_code(qr_code_id):
    # Check if the scanned QR code's identifier exists in the qr_codes dictionary
    if qr_codes.get(qr_code_id):
        # remove the scanned qr code from the dictionary
        qr_codes.pop(qr_code_id)
        global flag
        flag = 1
        return render_template("completed.html", data=flag)
        # return redirect("www.google.com")
    else:
        return render_template("scanned.html")
<<<<<<< Updated upstream
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
