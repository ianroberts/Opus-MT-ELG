import json
import argparse
from tornado import web, ioloop, queues, gen, process

from server import ApiHandler, TranslatorWorker, initialize_workers, settings

class ElgApiHandler(ApiHandler):

    def post(self, src_lang, target_lang):
        self.prepare_args()
        lang_pair = "{}-{}".format(src_lang, target_lang)
        if lang_pair not in self.worker_pool:
            i18n_err_obj = { "code": "elg.request.property.unsupported",
                             "text": "Language pair {0} not supported",
                             "params": lang_pair}
            self.write({"failure": { "errors": [i18n_err_obj] }})
            return
        self.worker = self.worker_pool[lang_pair]
        # TODO there should be better error handling here, to catch any
        # exceptions raised by the worker and render them as a proper i18n
        # error response with a 500 HTTP response code
        translation = self.worker.translate(self.args['content'])
        self.write({"response": {"type": "texts", "texts": [{"content": translation}]}})


def make_app(args):
    services = {}
    with open(args.config, 'r') as configfile:
        services = json.load(configfile)
    worker_pool = initialize_workers(services)
    # Take the language pair from the URL, i.e. a POST to /elg/translate/en/fi
    # would do English to Finnish
    handlers = [
        (r"/elg/translate/([a-z]+)/([a-z]+)", ElgApiHandler,
         dict(api='translate', config=services, worker_pool=worker_pool)),
    ]
    application = web.Application(handlers, debug=False, **settings)
    return application

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Marian MT translation server.')
    parser.add_argument('-p', '--port', type=int, default=8888,
                        help='Port the server will listen on')
    parser.add_argument('-c', '--config', type=str, default="services.json",
                        help='MT server configurations')
    args = parser.parse_args()
    application = make_app(args)
    application.listen(args.port)
    ioloop.IOLoop.current().start()
