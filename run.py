try:
    from app.main import app
    print("Successfully imported app!")
except Exception as e:
    print(f"Import failed: {e}")
    import traceback
    traceback.print_exc()
    raise

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="debug")
    )
