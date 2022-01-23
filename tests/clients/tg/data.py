GET_ME = {'ok': True,
          'result': {'id': 2065163148, 'is_bot': True, 'first_name': 'Metaclass', 'username': 'metaclassbot',
                     'can_join_groups': True, 'can_read_all_group_messages': False, 'supports_inline_queries': False}}

GET_UPDATES = {'ok': True, 'result': [{
    'update_id': 503972234,
    'message': {
        'message_id': 1,
        'from': {'id': 85364161, 'is_bot': False, 'first_name': 'Alexander', 'last_name': 'Opryshko',
                 'username': 'alexopryshko', 'language_code': 'en'},
        'chat': {'id': 85364161, 'first_name': 'Alexander', 'last_name': 'Opryshko', 'username': 'alexopryshko',
                 'type': 'private'},
        'date': 1634815235,
        'text': '/start',
        'entities': [{'offset': 0, 'length': 6, 'type': 'bot_command'}]
    }}
]}
GET_OFFSET_UPDATES = {'ok': True, 'result': []}

SEND_MESSAGE = {'ok': True, 'result': {
    'message_id': 13, 'from': {'id': 2065163148, 'is_bot': True, 'first_name': 'Metaclass', 'username': 'metaclassbot'},
    'chat': {'id': 85364161, 'first_name': 'Alexander', 'last_name': 'Opryshko', 'username': 'alexopryshko',
             'type': 'private'}, 'date': 1634901940, 'text': 'hello'
}}
