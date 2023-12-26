
# custom function to get object or return none if not found

def get_object_or_none(model_name, **kwargs):
    try:
        obj = model_name.objects.get(**kwargs)
        return obj
    except model_name.DoesNotExist:
        return None


def get_timer(length: float, type: str = 'long'):
    h = length // 3600
    m = length % 3600 // 60
    s = length % 3600 % 60
    if type == 'short':
        return f"{h}h {f'0{m}' if m < 10 else m}m"

    if type == 'min':
        return f"{f'0{m}' if m < 10 else m}min"

    else:
        if h >= 1:
            return f"{h}:{f'0{m}' if m < 10 else m}:{f'0{round(s)}' if s < 10 else round(s)}"
        else:
            return f"{f'0{m}' if m < 10 else m}:{f'0{round(s)}' if s < 10 else round(s)}"
