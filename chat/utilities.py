def get_one_to_one_chat_media_upload_address(obj, filename: str):
    return f'chats/one_to_one/{obj.participant_1.user.username}_{obj.participant_2.user.username}/{filename}'
