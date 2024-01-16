from flask import Flask, request, render_template
from kafka import KafkaProducer, KafkaConsumer

app = Flask(__name__)
producer = KafkaProducer(bootstrap_servers='localhost:9092')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        message = request.form.get('message')
        producer.send('meddelanden', bytes(message, 'utf-8'))
    return render_template('index.html')

@app.route('/messages')
def messages():
    consumer = KafkaConsumer('meddelanden', 
                             bootstrap_servers='localhost:9092',
                             auto_offset_reset='earliest', 
                             consumer_timeout_ms=100)

    messages = [msg.value.decode('utf-8') for msg in consumer]
    return render_template('messages.html', messages=messages)

if __name__ == '__main__':
    app.run(debug=True)
