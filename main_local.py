import uvicorn


if __name__ == "__main__":
    uvicorn.run("app.main:app" ,host='0.0.0.0', port=5000, reload=True, debug=True, workers=3)
    # uvicorn.run("app.main:app" , host="0.0.0.0", port=8081, proxy_headers=True)
