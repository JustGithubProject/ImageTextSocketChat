import tkinter as tk

from client import client


placeholder_text_host = "Host: "
placeholder_text_port = "Port: "

def on_entry_click_host(event):
    if entry_host.get() == placeholder_text_host:
        entry_host.delete(0, "end")
        entry_host.insert(0, "")
        entry_host.config(fg="black")


def on_focusout_host(event):
    if entry_host.get() == "":
        entry_host.insert(0, placeholder_text_host)
        entry_host.config(fg="grey")


def on_entry_click_port(event):
    if entry_port.get() == placeholder_text_port:
        entry_port.delete(0, "end")
        entry_port.insert(0, "")
        entry_port.config(fg="black")


def on_focusout_port(event):
    if entry_port.get() == "":
        entry_port.insert(0, placeholder_text_port)
        entry_port.config(fg="grey")


def on_entry_click_msg(event):
    if entry_port.get() == "Message: ":
        entry_port.delete(0, "end")
        entry_port.insert(0, "")
        entry_port.config(fg="black")


def on_focusout_msg(event):
    if entry_port.get() == "":
        entry_port.insert(0, "Message: ")
        entry_port.config(fg="grey")

# Instance of Tk
window = tk.Tk()

# Size of window
window.geometry("400x400")

# Title and background
window.title("Interface for client")
window.configure(background="white")


# Create an Entry widget for host
entry_host = tk.Entry(window, width=40)
entry_host.insert(0, placeholder_text_host)
entry_host.bind('<FocusIn>', on_entry_click_host)
entry_host.bind('<FocusOut>', on_focusout_host)
entry_host.config(fg='grey')
entry_host.pack(pady=10)


# Create an Entry widget for port
entry_port = tk.Entry(window, width=40)
entry_port.insert(0, placeholder_text_port)
entry_port.bind('<FocusIn>', on_entry_click_port)
entry_port.bind('<FocusOut>', on_focusout_port)
entry_port.config(fg='grey')
entry_port.pack(pady=10)


# Create an Entry widget for port
entry_msg = tk.Entry(window, width=40)
entry_msg.insert(0, placeholder_text_port)
entry_msg.bind('<FocusIn>', on_entry_click_port)
entry_msg.bind('<FocusOut>', on_focusout_port)
entry_msg.config(fg='grey')
entry_msg.pack(pady=10)


# Create an Entry widget for message


def connect_to_specified_host_and_port():
    host = entry_host.get()
    port = entry_port.get()
    if host == placeholder_text_host:
        host = ""
    if port == placeholder_text_port:
        port = ""

    if host and port:
        client(host, int(port), entry_msg)
    else:
        client(entry_msg=entry_msg)

# button to connect to host and port
button = tk.Button(window, text="Connect", command=connect_to_specified_host_and_port)
button.pack(pady=10)
window.mainloop()
