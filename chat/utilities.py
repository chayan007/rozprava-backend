def get_one_to_one_chat_media_upload_address(obj, filename: str):
    return f'chats/one_to_one/{obj.sender.user.username}_{obj.receiver.user.username}/{filename}'
