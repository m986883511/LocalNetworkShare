# coding=utf-8
current_file_path = __file__

help_string = """
软件名称：局域网文本共享软件

1、软件打开会自动启动web服务器，监听端口可以在{}中修改；

2、本软件会监听你的剪贴板并立即更新在文本区，但不会共享到局域网，除非您点击'设置文本区为共享内容'按钮，所以您不用担心隐私泄露；

3、您可以点击'获取共享内容'来获取共享内容；

4、其他局域网设备如手机电脑，访问下方提示的链接也可以获取进行文本共享；

已知问题：
1、web页面暂时不支持中文；
2、运行exe窗口程序的电脑不要打开web页面，否则其他设备访问就会卡掉，如果卡了重开软件；
（难道是受限于python自带的wsgiref羸弱的性能？）

软件作者: Double.Wang
作者链接: https://github.com/m986883511/LocalNetworkShare
""".format(current_file_path)

server = {
    'port': '19999',
    'host': '0.0.0.0'
}

# Pecan Application Configurations
app = {
    'root': 'copypaste.controllers.root.RootController',
    'modules': ['copypaste'],
    'static_root': '%(confdir)s/public',
    'template_path': '%(confdir)s/copypaste/templates',
    'debug': True,
    'errors': {
        404: '/error/404',
        '__force_dict__': True
    }
}

# logging = {
#     'root': {'level': 'INFO', 'handlers': ['console']},
#     'loggers': {
#         'copypaste': {'level': 'DEBUG', 'handlers': ['console'], 'propagate': False},
#         'pecan': {'level': 'DEBUG', 'handlers': ['console'], 'propagate': False},
#         'py.warnings': {'handlers': ['console']},
#         '__force_dict__': True
#     },
#     'handlers': {
#         'console': {
#             'level': 'DEBUG',
#             'class': 'logging.StreamHandler',
#             'formatter': 'color'
#         }
#     },
#     'formatters': {
#         'simple': {
#             'format': ('%(asctime)s %(levelname)-5.5s [%(name)s]'
#                        '[%(threadName)s] %(message)s')
#         },
#         'color': {
#             '()': 'pecan.log.ColorFormatter',
#             'format': ('%(asctime)s [%(padded_color_levelname)s] [%(name)s]'
#                        '[%(threadName)s] %(message)s'),
#             '__force_dict__': True
#         }
#     }
# }
