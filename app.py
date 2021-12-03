import os
import json
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

# 事前に Slack アプリをインストールし 'xoxb-' で始まるトークンを入手
app = App(token=os.environ["SLACK_BOT_TOKEN"])

# ここでミドルウェアとリスナーの追加を行います
@app.shortcut("func_request")
def open_modal(ack, body, client):
    # Acknowledge the action
    ack()
    print(body["channel"]["id"])

    with open('modal.json') as f:
        block = json.load(f)

    client.views_open(
      trigger_id=body["trigger_id"],
        view={
            "type": "modal",
            # View identifier
            "callback_id": "view_1",
            "title": {"type": "plain_text", "text": "HaaS機能要望"},
            "submit": {"type": "plain_text", "text": "Submit"},
            "blocks": block['blocks'],
            "private_metadata": body["channel"]["id"]
        }
    )

@app.view("view_1")
def handle_view_events(ack, body, client, logger):
    ack()
    user = body["user"]["id"]
    channel = body['view']['private_metadata']
    title = body['view']['state']['values']['title']['plain_text_input-action']['value']
    content = body['view']['state']['values']['content']['plain_text_input-action']['value']
    print(body['view']['state']['values'])
    msg = "<@" + user +">さんから機能要望を受け付けました。\n"
    msg += "*" + title + "*\n"
    msg += "```" + content + "```"
    client.chat_postMessage(channel=channel, text=msg)

if __name__ == "__main__":
    # export SLACK_APP_TOKEN=xapp-***
    # export SLACK_BOT_TOKEN=xoxb-***
    handler = SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"])
    handler.start()
