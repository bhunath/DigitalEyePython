import win10toast

toaster = win10toast.ToastNotifier()


def show_window_notification(title, msg, icon=None, duration_time=3):
    toaster.show_toast(title, msg, threaded=True, icon_path=icon, duration=duration_time)
