import uvicorn
from trans_rss import app

uvicorn.run(app, host="0.0.0.0", port= 80)