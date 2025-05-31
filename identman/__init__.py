from identman.app import create_app
from identman.blueprints import bp
from identman.identman.decryption import decrypt


IV_LENGTH = 12
SALT_LENGTH = 12

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)

