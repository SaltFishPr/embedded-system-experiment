import wws_and_jl

if __name__ == "__main__":
    app = wws_and_jl.create_app()
    app.run(host="0.0.0.0", port=8000)
