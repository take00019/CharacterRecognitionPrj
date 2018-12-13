#!/usr/bin/python
	#coding:utf-8
import base64
import json
from requests import Request, Session

path = ".\\resources\\image.png"

def recognize_captcha(str_image_path):

        bin_captcha = open(str_image_path, 'rb').read()
        str_encode_file = base64.b64encode(bin_captcha).decode("utf-8")
        str_url = "https://vision.googleapis.com/v1/images:annotate?key="
        str_api_key = "XXXXXXXX"

        str_headers = {'Content-Type': 'application/json'}
        str_json_data = json.dumps({
            'requests': [{
                    'image': {
                        'content': str_encode_file
                    },
                    'features': [{
                            'type': 'TEXT_DETECTION',
                            'maxResults': 10
                    }]
            }]
        })

        # print("begin request")
        obj_session = Session()
        obj_request = Request("POST",
                              str_url + str_api_key,
                              data=str_json_data,
                              headers=str_headers
                              )
        obj_prepped = obj_session.prepare_request(obj_request)
        obj_response = obj_session.send(obj_prepped,
                                        verify=True,
                                        timeout=60
                                        )
        # print("end request")
        if obj_response.status_code == 200:
            #print (obj_response.text)
            return obj_response.text
        else:
            print("API error : status=" + str(obj_response.status_code))
            return "error"

if __name__ == '__main__':
    data = json.loads(recognize_captcha(path))
    data = data["responses"]
    # print(data)
    # 読み込み結果表示
    for i in data:
        print(i["fullTextAnnotation"]["text"])
