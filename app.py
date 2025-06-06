import os

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
@app.route('/')
def home():
    return "Forex Factory News API is running!"
@app.route('/')
def home():
    return "API is working!"
