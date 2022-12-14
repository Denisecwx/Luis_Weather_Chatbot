from flask import Flask, request, Response
from botbuilder.core import BotFrameworkAdapter, BotFrameworkAdapterSettings, ConversationState,MemoryStorage
from botbuilder.schema import Activity
import asyncio
from luis.luisApp import LuisConnect
import os
from logger.logger import Log


app = Flask(__name__)
loop = asyncio.get_event_loop()

bot_settings = BotFrameworkAdapterSettings("a4b78845-0abf-4255-90cf-c3d5cee768dc","VSP8Q~HXfMA5NUC5CO9xF2GwdpRf6enx4iWobafA")
# bot_settings = BotFrameworkAdapterSettings("","")
bot_adapter = BotFrameworkAdapter(bot_settings)

#CON_MEMORY = ConversationState(MemoryStorage())
luis_bot_dialog = LuisConnect()

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route("/api/messages", methods=["POST"])
def messages():
    if "application/json" in request.headers["content-type"]:
        log=Log()
        request_body = request.json
        user_says = Activity().deserialize(request_body)
        log.write_log(sessionID='session1',log_message="user says: "+str(user_says))
        authorization_header = (request.headers["Authorization"] if "Authorization" in request.headers else "")

        async def call_user_fun(turncontext):
            await luis_bot_dialog.on_turn(turncontext)

        task = loop.create_task(
            bot_adapter.process_activity(user_says, authorization_header, call_user_fun)
        )
        loop.run_until_complete(task)
        return ""
    else:
        return Response(status=406)  # status for Not Acceptable

if __name__ == '__main__':
    #app.run(port= 3978)
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
    #  app.run(port=process.env.PORT or 5000)
