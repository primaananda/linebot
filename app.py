from __future__ import unicode_literals

import errno
import os
import sys
import tempfile
import requests
from argparse import ArgumentParser

from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    LineBotApiError, InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
    SourceUser, SourceGroup, SourceRoom,
    TemplateSendMessage, ConfirmTemplate, MessageAction,
    ButtonsTemplate, ImageCarouselTemplate, ImageCarouselColumn, URIAction,
    PostbackAction, DatetimePickerAction,
    CameraAction, CameraRollAction, LocationAction,
    CarouselTemplate, CarouselColumn, PostbackEvent,
    StickerMessage, StickerSendMessage, LocationMessage, LocationSendMessage,
    ImageMessage, VideoMessage, AudioMessage, FileMessage,
    UnfollowEvent, FollowEvent, JoinEvent, LeaveEvent, BeaconEvent,
    FlexSendMessage, BubbleContainer, ImageComponent, BoxComponent,
    TextComponent, SpacerComponent, IconComponent, ButtonComponent,
    SeparatorComponent, QuickReply, QuickReplyButton
)

app = Flask(__name__)

line_bot_api = LineBotApi('exFmH2PrUuHfOvyb4iF/HZ59hFP0R0uIu0N9gPld1A2kgfPr/2lAHqxnCzsok79m2UxBOLe9UvIDN41keSCAA1NRfYpcPC9ZkUHvHd0vaRdUtbWSA0rwuzMT0rR9TS4qXZunW9gaWR5/BXDj4yvG1AdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('cba2b4b2e75c6d116878aa9b91825af4')

static_tmp_path = os.path.join(os.path.dirname(__file__), 'static', 'tmp')

# function for create tmp dir for download content
def make_static_tmp_dir():
    try:
        os.makedirs(static_tmp_path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(static_tmp_path):
            pass
        else:
            raise

@app.route("/callback", methods=['POST'])
def callback():
    # Get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # Get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except LineBotApiError as e:
        print("Got exception from LINE Messaging API: %s\n" % e.message)
        for m in e.error.details:
            print("  %s: %s" % (m.property, m.message))
        print("\n")
    except InvalidSignatureError:
        abort(400)

    return 'OK'



@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    text = (event.message.text).lower()

    if text == 'profile':
        if isinstance(event.source, SourceUser):
            profile = line_bot_api.get_profile(event.source.user_id)
            line_bot_api.reply_message(
                event.reply_token, [
                    TextSendMessage(text='Display name: ' + profile.display_name),
                    TextSendMessage(text='Status message: ' + profile.status_message),
                    TextSendMessage(text='Picture: ' + profile.picture_url)
                ]
            )
        else:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="Bot can't use profile API without user ID"))
    elif text == 'bye':
        if isinstance(event.source, SourceGroup):
            line_bot_api.reply_message(
                event.reply_token, TextSendMessage(text='Leaving group'))
            line_bot_api.leave_group(event.source.group_id)
        elif isinstance(event.source, SourceRoom):
            line_bot_api.reply_message(
                event.reply_token, TextSendMessage(text='Leaving group'))
            line_bot_api.leave_room(event.source.room_id)
        else:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="Bot can't leave from 1:1 chat"))
    elif text == 'confirm':
        confirm_template = ConfirmTemplate(text='Do it?', actions=[
            MessageAction(label='Yes', text='Yes!'),
            MessageAction(label='No', text='No!'),
        ])
        template_message = TemplateSendMessage(
            alt_text='Confirm alt text', template=confirm_template)
        line_bot_api.reply_message(event.reply_token, template_message)
    elif text == 'navigation':
        buttons_template = ButtonsTemplate(
            title='Navigation Bot vers.1', text='Hello, ada yang bisa saya bantu...?', actions=[
                MessageAction(label='Info Grapari', text='cari info Grapari'),
                URIAction(label='About Dev.', uri='http://line.me/ti/p/~primaananda_')
            ])
        template_message = TemplateSendMessage(
            alt_text='Buttons alt text', template=buttons_template)
        line_bot_api.reply_message(event.reply_token, template_message)
    elif text == 'cari info grapari' or text == 'cari grapari' or text == 'grapari':
        carousel_template = CarouselTemplate(columns=[
            CarouselColumn(text='Daftar grapari wilayah Denpasar', title='Denpasar', actions=[
                MessageAction(label='Grapari Teuku Umar', text='grapari teuku umar'),
                MessageAction(label='grapari renon', text='grapari renon')
            ]),
            CarouselColumn(text='Daftar grapari wilayah Bangli', title='Bangli', actions=[
                PostbackAction(label='Status Grapari', data='tidak terdapat Grapari di Bangli', text=' '),
                MessageAction(label=' ', text=' ')
            ]),
            CarouselColumn(text='Daftar grapari wilayah Buleleng', title='Buleleng', actions=[
                MessageAction(label='grapari Buleleng', text='grapari buleleng'),
                MessageAction(label=' ', text=' ')
            ]),
            CarouselColumn(text='Daftar grapari wilayah Gianyar', title='Gianyar', actions=[
                MessageAction(label='grapari Gianyar', text='grapari gianyar'),
                MessageAction(label=' ', text=' ')
            ]),
            CarouselColumn(text='Daftar grapari wilayah Jembrana', title='Jembrana', actions=[
                MessageAction(label='graPARI Negara', text='grapari negara'),
                MessageAction(label=' ', text=' ')
            ]),
            CarouselColumn(text='Daftar grapari wilayah Karangasem', title='Karangasem', actions=[
                MessageAction(label='graPARI Karangasem', text='grapari karangasem'),
                MessageAction(label=' ', text=' ')
            ]),
            CarouselColumn(text='Daftar grapari wilayah Klungkung', title='Klungkung', actions=[
                PostbackAction(label='Status Grapari', data='tidak terdapat Grapari di Klungkung', text=' '),
                MessageAction(label=' ', text=' ')
            ]),
            CarouselColumn(text='Daftar grapari wilayah Tabanan', title='Tabanan', actions=[
                MessageAction(label='Grapari Tabanan', text='grapari tabanan'),
                MessageAction(label=' ', text=' ')
            ]),
        ])
        template_message = TemplateSendMessage(
            alt_text='Carousel alt text', template=carousel_template)
        line_bot_api.reply_message(event.reply_token, template_message)
    elif text == 'alamat grapari renon':
        line_bot_api.reply_message(
            event.reply_token,[
                LocationSendMessage(
                title='My GraPARI Denpasar Renon',
                address='Jl. Raya Puputan No.33, Panjer, Denpasar Sel., Kota Denpasar, Bali 80234',
                latitude=-8.672262,
                longitude=115.228615
                )
            ])
    elif text=='alamat grapari teuku umar':
        line_bot_api.reply_message(
            event.reply_token,[
                LocationSendMessage(
                title='My GraPARI Denpasar Teuku Umar',
                address='Jl. Teuku Umar No.6, Dauh Puri Klod, Denpasar Bar., Kota Denpasar, Bali 80114',
                latitude=-8.669041,
                longitude=115.214185
                )
            ])
    elif text=='alamat grapari buleleng':
        line_bot_api.reply_message(
            event.reply_token,[
                LocationSendMessage(
                title='My GraPARI Buleleng',
                address='Jl. A. Yani No.72, Kaliuntu, Kec. Buleleng, Kabupaten Buleleng, Bali 81114',
                latitude=-8.111648,
                longitude=115.085734
                )
            ])
    elif text=='alamat grapari gianyar':
        line_bot_api.reply_message(
            event.reply_token,[
                LocationSendMessage(
                title='My GraPARI Gianyar',
                address='Jl. A. Yani No.72, Kaliuntu, Kec. Buleleng, Kabupaten Buleleng, Bali 81114',
                latitude=-8.111648,
                longitude=115.085734
                )
            ])
    elif text=='alamat grapari mbg':
        line_bot_api.reply_message(
            event.reply_token,[
                LocationSendMessage(
                title='My graPARI Mall Bali Galeria',
                address='JL. by Pass I Gusti Ngurah Rai , 80361 Denpasar , Bali, Kuta, Badung Regency, Bali 80361',
                latitude=-8.723316,
                longitude=115.184888
                )
            ])
    elif text=='alamat grapari karangasem':
        line_bot_api.reply_message(
            event.reply_token,[
                LocationSendMessage(
                title='My graPARI Karangasem',
                address='Jl. PB. Sudirman 98 C, Amlapura, Kec. Karangasem, Kab. Karangasem, Bali 80811',
                latitude=-8.451645,
                longitude=115.603835
                )
            ])
    elif text=='alamat grapari negara':
        line_bot_api.reply_message(
            event.reply_token,[
                LocationSendMessage(
                title='GraPARI Telkomsel Negara',
                address='Jl. Ngurah Rai, Pendem, Kec. Jembrana, Kabupaten Jembrana, Bali 82218',
                latitude=-8.360644,
                longitude=114.629995
                )
            ])
    elif text=='alamat grapari tabanan':
        line_bot_api.reply_message(
            event.reply_token,[
                LocationSendMessage(
                title='GraPARI Telkomsel Tabanan',
                address='Jl. Dr. Ir. Soekarno, Banjar Anyar, Kediri, Kabupaten Tabanan, Bali 82121',
                latitude=-8.552806,
                longitude=115.135258
                )
            ])
    elif text == 'grapari teuku umar':
        bubble = BubbleContainer(
            direction='ltr',
            hero=ImageComponent(
                url='https://i.imgur.com/G18bDUi.jpg',
                size='full',
                aspect_ratio='20:13',
                aspect_mode='cover',
                action=URIAction(uri='https://i.imgur.com/G18bDUi.jpg', label='label')
            ),
            body=BoxComponent(
                layout='vertical',
                contents=[
                    # title
                    TextComponent(text='My GraPARI Teuku Umar', weight='bold', size='xl'),
                    # info
                    BoxComponent(
                        layout='vertical',
                        margin='lg',
                        spacing='sm',
                        contents=[
                            BoxComponent(
                                layout='baseline',
                                spacing='sm',
                                contents=[
                                    TextComponent(
                                        text='Alamat',
                                        color='#aaaaaa',
                                        size='sm',
                                        flex=3
                                    ),
                                    TextComponent(
                                        text='Jl. Teuku Umar No.6, Dauh Puri Klod, Denpasar Bar., Kota Denpasar, Bali 80114',
                                        wrap=True,
                                        color='#666666',
                                        size='sm',
                                        flex=5
                                    )
                                ],
                            ),
                            BoxComponent(
                                layout='baseline',
                                spacing='sm',
                                contents=[
                                    TextComponent(
                                        text="Waktu Buka",
                                        color='#aaaaaa',
                                        size='sm',
                                        flex=3
                                    ),
                                    TextComponent(
                                        text="Senin, 08.00–17.00\nSelasa, 08.00–17.00\nRabu, 08.00–17.00\nKamis, 08.00–17.00\nJumat, 08.00–17.00\nSabtu, 08.00–12.00\nMinggu, Tutup",
                                        wrap=True,
                                        color='#666666',
                                        size='sm',
                                        flex=5,
                                    ),
                                ],
                            ),
                            BoxComponent(
                                layout='baseline',
                                spacing='sm',
                                contents=[
                                    TextComponent(
                                        text='No. Telp',
                                        color='#aaaaaa',
                                        size='sm',
                                        flex=3
                                    ),
                                    TextComponent(
                                        text="0811-3940-500",
                                        wrap=True,
                                        color='#666666',
                                        size='sm',
                                        flex=5,
                                    ),
                                ],
                            ),
                        ],
                    )
                ],
            ),
            footer=BoxComponent(
                layout='vertical',
                spacing='sm',
                contents=[
                    # callAction, separator, websiteAction
                    SpacerComponent(size='sm'),
                    # callAction
                    ButtonComponent(
                        style='primary',
                        color='#00b300',
                        height='sm',
                        action=URIAction(label='Call', uri='tel:08113940500'),
                    ),
                    # websiteAction
                    ButtonComponent(
                        style='secondary',
                        height='sm',
                        action=PostbackAction(label='Alamat GraPARI', data='alamat grapari teuku umar', text='alamat grapari teuku umar')
                    )
                ]
            ),
        )
        message = FlexSendMessage(alt_text="grapari teuku umar", contents=bubble)
        line_bot_api.reply_message(
            event.reply_token,
            message
        )
    elif text == 'carousel':
        carousel_template = CarouselTemplate(columns=[
            CarouselColumn(text='hoge1', title='fuga1', actions=[
                URIAction(label='Go to line.me', uri='https://line.me'),
                PostbackAction(label='ping', data='ping')
            ]),
            CarouselColumn(text='hoge2', title='fuga2', actions=[
                PostbackAction(label='ping with text', data='ping', text='ping'),
                MessageAction(label='Translate Rice', text='米')
            ]),
            CarouselColumn(text='hoge1', title='fuga1', actions=[
                URIAction(label='Go to line.me', uri='https://line.me'),
                PostbackAction(label='ping', data='ping')
            ]),
        ])
        template_message = TemplateSendMessage(
            alt_text='Carousel alt text', template=carousel_template)
        line_bot_api.reply_message(event.reply_token, template_message)
    elif text == 'image_carousel':
        image_carousel_template = ImageCarouselTemplate(columns=[
            ImageCarouselColumn(image_url='https://via.placeholder.com/1024x1024',
                                action=DatetimePickerAction(label='datetime',
                                                            data='datetime_postback',
                                                            mode='datetime')),
            ImageCarouselColumn(image_url='https://via.placeholder.com/1024x1024',
                                action=DatetimePickerAction(label='date',
                                                            data='date_postback',
                                                            mode='date'))
        ])
        template_message = TemplateSendMessage(
            alt_text='ImageCarousel alt text', template=image_carousel_template)
        line_bot_api.reply_message(event.reply_token, template_message)
    elif text == 'imagemap':
        pass
    elif text == 'flex':
        bubble = BubbleContainer(
            direction='ltr',
            hero=ImageComponent(
                url='https://example.com/cafe.jpg',
                size='full',
                aspect_ratio='20:13',
                aspect_mode='cover',
                action=URIAction(uri='http://example.com', label='label')
            ),
            body=BoxComponent(
                layout='vertical',
                contents=[
                    # title
                    TextComponent(text='Brown Cafe', weight='bold', size='xl'),
                    # review
                    BoxComponent(
                        layout='baseline',
                        margin='md',
                        contents=[
                            IconComponent(size='sm', url='https://example.com/gold_star.png'),
                            IconComponent(size='sm', url='https://example.com/grey_star.png'),
                            IconComponent(size='sm', url='https://example.com/gold_star.png'),
                            IconComponent(size='sm', url='https://example.com/gold_star.png'),
                            IconComponent(size='sm', url='https://example.com/grey_star.png'),
                            TextComponent(text='4.0', size='sm', color='#999999', margin='md',
                                          flex=0)
                        ]
                    ),
                    # info
                    BoxComponent(
                        layout='vertical',
                        margin='lg',
                        spacing='sm',
                        contents=[
                            BoxComponent(
                                layout='baseline',
                                spacing='sm',
                                contents=[
                                    TextComponent(
                                        text='Place',
                                        color='#aaaaaa',
                                        size='sm',
                                        flex=1
                                    ),
                                    TextComponent(
                                        text='Shinjuku, Tokyo',
                                        wrap=True,
                                        color='#666666',
                                        size='sm',
                                        flex=5
                                    )
                                ],
                            ),
                            BoxComponent(
                                layout='baseline',
                                spacing='sm',
                                contents=[
                                    TextComponent(
                                        text='Time',
                                        color='#aaaaaa',
                                        size='sm',
                                        flex=1
                                    ),
                                    TextComponent(
                                        text="10:00 - 23:00",
                                        wrap=True,
                                        color='#666666',
                                        size='sm',
                                        flex=5,
                                    ),
                                ],
                            ),
                        ],
                    )
                ],
            ),
            footer=BoxComponent(
                layout='vertical',
                spacing='sm',
                contents=[
                    # callAction, alamatAction
                    SpacerComponent(size='sm'),
                    # callAction
                    ButtonComponent(
                        style='link',
                        height='sm',
                        action=URIAction(label='CALL', uri='tel:000000'),
                    ),
                    # alamatAction
                    ButtonComponent(
                        style='link',
                        height='sm',
                        action=URIAction(label='WEBSITE', uri="https://example.com")
                    )
                ]
            ),
        )
        message = FlexSendMessage(alt_text="hello", contents=bubble)
        line_bot_api.reply_message(
            event.reply_token,
            message
        )
    elif text == 'quick_reply':
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(
                text='Quick reply',
                quick_reply=QuickReply(
                    items=[
                        QuickReplyButton(
                            action=PostbackAction(label="label1", data="data1")
                        ),
                        QuickReplyButton(
                            action=MessageAction(label="label2", text="text2")
                        ),
                        QuickReplyButton(
                            action=DatetimePickerAction(label="label3",
                                                        data="data3",
                                                        mode="date")
                        ),
                        QuickReplyButton(
                            action=CameraAction(label="label4")
                        ),
                        QuickReplyButton(
                            action=CameraRollAction(label="label5")
                        ),
                        QuickReplyButton(
                            action=LocationAction(label="label6")
                        ),
                    ])))
    elif text == '.help':
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(
                text='Berikut merupakan command yang terdapat pada BOT ini: \n1. info_grapari\n2. profile\n3. bye\n4. confirm\n5. buttons\n6. carousel\n7 image\n8 image carousel\n9 imagemap\n10 flex\n11 quick_reply\n12 info\n13 about\n14 ip',
                quick_reply=QuickReply(
                    items=[
                        QuickReplyButton(action=MessageAction(label="profile", text="profile")),
                        QuickReplyButton(action=MessageAction(label="bye", text="bye")),
                        QuickReplyButton(action=MessageAction(label="confirm", text="confirm")),
                        QuickReplyButton(action=MessageAction(label="buttons", text="buttons")),
                        QuickReplyButton(action=MessageAction(label="carousel", text="carousel")),
                        QuickReplyButton(action=MessageAction(label="image", text="image")),
                        QuickReplyButton(action=MessageAction(label="image carousel", text="image carousel")),
                        QuickReplyButton(action=MessageAction(label="imagemap", text="imagemap")),
                        QuickReplyButton(action=MessageAction(label="flex", text="flex")),
                        QuickReplyButton(action=MessageAction(label="quick_reply", text="quick_reply")),
                        QuickReplyButton(action=MessageAction(label="info", text="info")),
                        QuickReplyButton(action=MessageAction(label="about", text="about")),
                        QuickReplyButton(action=MessageAction(label="your ip", text="ip"))
                    ]
                )
            ))
    elif text == 'info':
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=''))
    elif text == 'about':
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text='Ini merupakan bot yang masih dalam proses pengembangan.'))
    elif text == 'ip':
        res = requests.get('https://ipinfo.io/')
        data = res.json()
        # your_ip = data['ip']
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=('alamat IP : ' + data['ip'] + '\nhostname : ' + data['hostname'] + '\nKota : ' + data['city'] + '\nNegara : ' + data['country'] + '\nLokasi : ' + data['loc'] + '\nOrganisasi : ' + data['org'])))
    else:
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text='Need help? click this button .help', quick_reply=QuickReply(
                    items=[
                        QuickReplyButton(action=MessageAction(label="help", text=".help"))])))

#TextSendMessage(text=event.message.text))


@handler.add(MessageEvent, message=LocationMessage)
def handle_location_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        LocationSendMessage(
            title=event.message.title, address=event.message.address,
            latitude=event.message.latitude, longitude=event.message.longitude
        )
    )


@handler.add(MessageEvent, message=StickerMessage)
def handle_sticker_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        StickerSendMessage(
            package_id=event.message.package_id,
            sticker_id=event.message.sticker_id)
    )


# Other Message Type
@handler.add(MessageEvent, message=(ImageMessage, VideoMessage, AudioMessage))
def handle_content_message(event):
    if isinstance(event.message, ImageMessage):
        ext = 'jpg'
    elif isinstance(event.message, VideoMessage):
        ext = 'mp4'
    elif isinstance(event.message, AudioMessage):
        ext = 'm4a'
    else:
        return

    message_content = line_bot_api.get_message_content(event.message.id)
    with tempfile.NamedTemporaryFile(dir=static_tmp_path, prefix=ext + '-', delete=False) as tf:
        for chunk in message_content.iter_content():
            tf.write(chunk)
        tempfile_path = tf.name

    dist_path = tempfile_path + '.' + ext
    dist_name = os.path.basename(dist_path)
    os.rename(tempfile_path, dist_path)

    line_bot_api.reply_message(
        event.reply_token, [
            TextSendMessage(text='Save content.'),
            TextSendMessage(text=request.host_url + os.path.join('static', 'tmp', dist_name))
        ])


@handler.add(MessageEvent, message=FileMessage)
def handle_file_message(event):
    message_content = line_bot_api.get_message_content(event.message.id)
    with tempfile.NamedTemporaryFile(dir=static_tmp_path, prefix='file-', delete=False) as tf:
        for chunk in message_content.iter_content():
            tf.write(chunk)
        tempfile_path = tf.name

    dist_path = tempfile_path + '-' + event.message.file_name
    dist_name = os.path.basename(dist_path)
    os.rename(tempfile_path, dist_path)

    line_bot_api.reply_message(
        event.reply_token, [
            TextSendMessage(text='Save file.'),
            TextSendMessage(text=request.host_url + os.path.join('static', 'tmp', dist_name))
        ])


@handler.add(FollowEvent)
def handle_follow(event):
    line_bot_api.reply_message(
        event.reply_token, TextSendMessage(text='Got follow event'))


@handler.add(UnfollowEvent)
def handle_unfollow():
    app.logger.info("Got Unfollow event")


@handler.add(JoinEvent)
def handle_join(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text='Joined this ' + event.source.type))


@handler.add(LeaveEvent)
def handle_leave():
    app.logger.info("Got leave event")


@handler.add(PostbackEvent)
def handle_postback(event):
    if event.postback.data == 'ping':
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text='pong'))
    elif event.postback.data == 'datetime_postback':
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=event.postback.params['datetime']))
    elif event.postback.data == 'date_postback':
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=event.postback.params['date']))
    elif event.postback.data == 'tidak terdapat Grapari di Bangli':
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text='Mohon Maaf Belum ada Grapari di Wilayah Bangli.'))
    elif event.postback.data == 'tidak terdapat Grapari di Klungkung':
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text='Mohon Maaf Belum ada Grapari di Wilayah Klungkung.'))


@handler.add(BeaconEvent)
def handle_beacon(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(
            text='Got beacon event. hwid={}, device_message(hex string)={}'.format(
                event.beacon.hwid, event.beacon.dm)))


if __name__ == "__main__":
    ##run mode
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

    #debug mode
    # arg_parser = ArgumentParser(
    #     usage='Usage: python ' + __file__ + ' [--port <port>] [--help]'
    # )
    # arg_parser.add_argument('-p', '--port', type=int, default=8000, help='port')
    # arg_parser.add_argument('-d', '--debug', default=False, help='debug')
    # options = arg_parser.parse_args()

    # # create tmp dir for download content
    # make_static_tmp_dir()

    # app.run(debug=options.debug, port=options.port)
