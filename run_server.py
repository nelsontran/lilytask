#!/usr/bin/env python3

if __name__ == "__main__":
    from app import app as application
    application.secret_key = 'DEVELOPMENT'
    application.run(debug=True)
