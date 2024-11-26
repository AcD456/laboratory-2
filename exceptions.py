class AudioPlayerError(Exception):
    """Базовый класс исключений для аудиоплеера"""
    pass

class FileLoadError(AudioPlayerError):
    """Ошибка загрузки файла"""
    pass

class PlaybackError(AudioPlayerError):
    """Ошибка воспроизведения аудио"""
    pass

class StopPlaybackError(AudioPlayerError):
    """Ошибка остановки аудио"""
    pass
