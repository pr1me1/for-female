def avatar_upload_path(instance, filename):
    import time

    timestamp = int(time.time())
    extension = filename.split(".")[-1]

    return f"avatars/{instance.user.id}_avatar.{timestamp}.{extension}"
