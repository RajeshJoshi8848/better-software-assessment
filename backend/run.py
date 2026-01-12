from app import create_app

print("Starting Flask app...")

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
