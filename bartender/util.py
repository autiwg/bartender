def map_kwargs(*args, **kwargs):
    return dict(zip(args, [kwargs] * len(args)))
