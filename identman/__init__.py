from identman.blueprints import bp
from identman.identman.decryption import decrypt
from flask import Flask, Blueprint
from flask_cors import CORS

IV_LENGTH = 12
SALT_LENGTH = 12



if __name__ == "__main__":
    #base = "PkSM_-4mBLtcnyttfuZmYIPD6tMLW9uzNQg8eF2pJKIhkH46h3NUF7wI6hQ9Er6_lxdp9nDlUpMX5BBTEadfpynIZfrcRlNPDxRmOHyA6_4Y_zHwQ0N7OaifL8I-cU1NpcyZzd7bzV1N-bKFPv9uL6O3i7pVYb8pKI8hUVmT47icBeTNTYJvgdLgiZVl8Kr3M5nYknAF3xcqdrNepvsGZKWanEktuwN942_ZFw"
    #print(decrypt(b"Hallo", base))
    app = Flask(__name__)
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    app.register_blueprint(bp)
    app.run(debug=True)

