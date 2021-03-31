from fastapi import Header, HTTPException

async def check_apikey(api_key:str=Header(None, convert_underscores=False)):
    key=""
    if api_key!=key:
        raise HTTPException(status_code=400, detail="X-Token header invalid")
