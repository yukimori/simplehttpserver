#!/usr/bin/python
# -*- coding: utf-8 -*-

from BaseHTTPServer import BaseHTTPRequestHandler
import cgi
import json
import sys

class PostHandler(BaseHTTPRequestHandler):
    def do_POST(self):

        print "self.headers : " + str(self.headers)
        print "self.headers :['Content-type'] : " + self.headers['Content-Type']

        # POST されたフォームデータを解析する
        form = cgi.FieldStorage(
            fp=self.rfile, 
            headers=self.headers,
            environ={'REQUEST_METHOD':'POST',
                     'CONTENT_TYPE':self.headers['Content-Type'], #Content-typeがリクエストにないとエラーになってしまう
                     })

        print "form.value : " + str(form.value)

        #リクエストボディを取得してオブジェクト化する
        json_obj = json.loads(form.value)
        
        #レスポンス情報を作成する
        res = {}
        res["Client"] = str(self.client_address)
        res["User-agent"] = str(self.headers['user-agent'])
        res["Path"] = self.path
        res["result"] = 0
        res["request_body"] = json_obj

        #HTTPServerインスタンスへのアクセス
        #ハンドラからはserver変数にインスタンスが格納されている
        print self.server.server_name ; #アドレスが格納されている
        print self.server.server_port ; #ポートが格納されている

        # レスポンス開始
        self.send_response(200)
        self.end_headers()

        self.wfile.write(json.dumps(res))

        # self.wfile.write('Client : %s\n' % str(self.client_address))
        # self.wfile.write('User-agent: %s\n' % str(self.headers['user-agent']))
        # self.wfile.write('Path: %s\n' % self.path)
        # self.wfile.write('Form data:\n')

        # フォームに POST されたデータの情報を送り返す
        # for field in form.keys():
        #     field_item = form[field]
        #     if field_item.filename:
        #         # field はアップロードされたファイルを含みます
        #         file_data = field_item.file.read()
        #         file_len = len(file_data)
        #         del file_data
        #         self.wfile.write('\tUploaded %s as "%s" (%d bytes)\n' % \
        #                              (field, field_item.filename, file_len))
        #     else:
        #         # 通常のフォーム値
        #         self.wfile.write('\t%s=%s\n' % (field, form[field].value))
        # self.wfile.write(form.value)
        return

if __name__ == '__main__':

    #コマンドライン引数の取得
    argvs = sys.argv
    argc = len(argvs)

    if(argc != 3):
        print "Usage : %s host port" % argvs[0]
        quit()
    from BaseHTTPServer import HTTPServer
    server = HTTPServer((argvs[1], int(argvs[2])), PostHandler)
    print "Starting server, use <Ctrl-C> to stop"
    print "client example) curl -X POST -H \"Accept: application/json\" -H \"Content-type: application/json\" -d '{\"kye1\":\"value1\", \"key2\":\"value2\"}' http://%s:%s" % (argvs[1], argvs[2])
    server.serve_forever()
