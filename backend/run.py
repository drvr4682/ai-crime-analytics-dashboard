import os
from app import app

if __name__ == "__main__":
    print("\n" + "="*55)
    print("  AI-Powered Crime Data Analysis System (Bootstrapped)")
    print("  Mode: Development")
    print("  URL:  http://127.0.0.1:5000")
    print("="*55 + "\n")
    app.run(debug=app.config["DEBUG"], port=5000)
